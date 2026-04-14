"""语音转文本Agent - 支持FunAudioLLM/SenseVoiceSmall和长音频分片处理"""

import asyncio
import os
from pathlib import Path
from typing import Any, List, Optional, Tuple

import aiofiles
import aiohttp
from loguru import logger

from utils import check_ffmpeg, compress_audio, extract_audio, save_text_to_file


class ExtractAgent:
    """语音转文本Agent，支持FunAudioLLM/SenseVoiceSmall和长音频分片处理"""

    # 音频分片配置
    MAX_AUDIO_DURATION = 600  # 最大音频片段时长（秒），10分钟
    OVERLAP_DURATION = 2.0  # 片段重叠时长（秒），避免切割单词

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("SILI_FLOW_API_KEY")
        if not self.api_key:
            raise Exception("未设置 SILI_FLOW_API_KEY 环境变量")

        self.base_url = "https://api.siliconflow.cn/v1/audio/transcriptions"
        self.model = "FunAudioLLM/SenseVoiceSmall"

        # 检查ffmpeg是否可用
        check_ffmpeg()

    async def extract_text(
        self, video_path: Path, save_to_file: bool = True
    ) -> Tuple[str, Optional[Path]]:
        """从视频中提取文本，支持长音频分片处理

        Args:
            video_path: 视频文件路径
            save_to_file: 是否保存到txt文件

        Returns:
            (文本内容, txt文件路径) 如果save_to_file=False，txt文件路径为None
        """
        # 提取音频
        audio_path = await extract_audio(video_path)
        text = await self._transcribe_audio(audio_path)

        # 清理临时音频文件
        try:
            audio_path.unlink()
        except Exception:
            pass

        # 保存到txt文件
        txt_path = None
        if save_to_file and text:
            logger.info(f"保存文本到{save_to_file}")
            txt_path = await save_text_to_file(video_path, text)

        return text, txt_path

    async def _transcribe_audio(self, audio_path: Path) -> str:
        """调用硅基流动API进行语音转文字"""
        file_size = audio_path.stat().st_size
        max_size = 25 * 1024 * 1024  # 25MB

        if file_size > max_size:
            audio_path = await compress_audio(audio_path)

        async with aiofiles.open(audio_path, "rb") as f:
            audio_data = await f.read()

        data = aiohttp.FormData()
        data.add_field("file", audio_data, filename=audio_path.name)
        data.add_field("model", self.model)
        data.add_field("language", "zh")

        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.base_url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                data=data,
                timeout=aiohttp.ClientTimeout(total=300),  # 5分钟超时
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"API调用失败: {response.status} - {error_text}")

                result = await response.json()
                text = result.get("text", "")

                if not text:
                    logger.warning("API返回空文本")
                    # 尝试从其他字段获取文本
                    if "segments" in result:
                        segments = result["segments"]
                        text = " ".join([seg.get("text", "") for seg in segments])

                return text

    async def batch_extract(
        self,
        video_paths: List[Path],
        max_concurrent: int = 3,
        save_to_file: bool = True,
    ) -> tuple[BaseException | Any]:
        """批量提取文本，控制并发数

        Args:
            video_paths: 视频文件路径列表
            max_concurrent: 最大并发数
            save_to_file: 是否保存到txt文件

        Returns:
            [(文本内容, txt文件路径), ...] 的列表
        """
        semaphore = asyncio.Semaphore(max_concurrent)

        async def extract_with_semaphore(video_path: Path):
            async with semaphore:
                return await self.extract_text(video_path, save_to_file=save_to_file)

        tasks = [extract_with_semaphore(path) for path in video_paths]
        return await asyncio.gather(*tasks, return_exceptions=True)

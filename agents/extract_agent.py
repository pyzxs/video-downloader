"""语音转文本Agent - 支持FunAudioLLM/SenseVoiceSmall和长音频分片处理"""

import os
import asyncio
import aiohttp
import aiofiles
import tempfile
import math
from pathlib import Path
from typing import Optional, List, Tuple
from loguru import logger
import subprocess


async def _extract_audio(video_path: Path, output_path: Path = None) -> Path:
    """从视频中提取音频（使用 ffmpeg）"""
    if output_path is None:
        # 使用临时文件
        temp_dir = tempfile.gettempdir()
        output_path = Path(temp_dir) / f"audio_{video_path.stem}.mp3"

    # 使用 ffmpeg 提取音频
    cmd = [
        "ffmpeg",
        "-i",
        str(video_path),
        "-vn",  # 不处理视频
        "-acodec",
        "libmp3lame",  # 使用 MP3 编码
        "-q:a",
        "0",  # 最高质量
        "-ar",
        "16000",  # 采样率16kHz，适合语音识别
        "-ac",
        "1",  # 单声道
        "-y",  # 覆盖输出文件
        str(output_path),
    ]

    process = await asyncio.create_subprocess_exec(
        *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        error_msg = stderr.decode() if stderr else "未知错误"
        raise Exception(f"ffmpeg提取音频失败: {error_msg}")

    return output_path


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
        self._check_ffmpeg()

    def _check_ffmpeg(self):
        """检查ffmpeg是否可用"""
        try:
            subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
            logger.info("ffmpeg可用")
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise Exception("ffmpeg未安装或不可用，请先安装ffmpeg")

    async def extract_text(
        self, video_path: Path, show_progress: bool = True, save_to_file: bool = True
    ) -> Tuple[str, Optional[Path]]:
        """从视频中提取文本，支持长音频分片处理

        Args:
            video_path: 视频文件路径
            show_progress: 是否显示进度
            save_to_file: 是否保存到txt文件

        Returns:
            (文本内容, txt文件路径) 如果save_to_file=False，txt文件路径为None
        """
        if show_progress:
            print("正在提取音频...")

        # 提取音频
        audio_path = await _extract_audio(video_path)

        # 获取音频时长
        duration = await self._get_audio_duration(audio_path)

        if show_progress:
            print(f"音频时长: {duration:.1f}秒")

        # 根据时长决定是否分片
        if duration > self.MAX_AUDIO_DURATION:
            if show_progress:
                print(f"音频过长，进行分片处理...")
                print(f"  分片大小: {self.MAX_AUDIO_DURATION}秒")
                print(f"  重叠时长: {self.OVERLAP_DURATION}秒")

            # 分片处理
            text = await self._process_long_audio(audio_path, duration, show_progress)
        else:
            # 直接处理
            if show_progress:
                print("正在识别语音...")

            text = await self._transcribe_audio(audio_path)

        # 清理临时音频文件
        try:
            audio_path.unlink()
        except:
            pass

        if show_progress:
            print("语音识别完成")
            if text:
                print(f"识别文本长度: {len(text)}字符")

        # 保存到txt文件
        txt_path = None
        if save_to_file and text:
            txt_path = await self._save_text_to_file(video_path, text, show_progress)

        return text, txt_path

    async def _save_text_to_file(
        self, video_path: Path, text: str, show_progress: bool = True
    ) -> Path:
        """保存文本到同名txt文件

        Args:
            video_path: 视频文件路径
            text: 要保存的文本内容
            show_progress: 是否显示进度

        Returns:
            txt文件路径
        """
        # 生成txt文件路径（与视频文件同名，后缀为.txt）
        txt_path = video_path.with_suffix(".txt")

        # 保存文本
        async with aiofiles.open(txt_path, "w", encoding="utf-8") as f:
            await f.write(text)

        if show_progress:
            print(f"文本已保存到: {txt_path}")

        logger.info(f"文本已保存到: {txt_path}")
        return txt_path

    async def _get_audio_duration(self, audio_path: Path) -> float:
        """获取音频时长（秒）"""
        cmd = [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(audio_path),
        ]

        process = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            error_msg = stderr.decode() if stderr else "未知错误"
            raise Exception(f"获取音频时长失败: {error_msg}")

        return float(stdout.decode().strip())

    async def _split_audio(
        self, audio_path: Path, duration: float
    ) -> List[Tuple[Path, float, float]]:
        """将长音频分割成多个片段

        Args:
            audio_path: 原始音频文件路径
            duration: 音频总时长

        Returns:
            List of (segment_path, start_time, end_time)
        """
        segments = []
        temp_dir = Path(tempfile.gettempdir())

        # 计算需要多少个片段
        num_segments = math.ceil(duration / self.MAX_AUDIO_DURATION)

        for i in range(num_segments):
            # 计算片段起止时间（带重叠）
            start_time = max(0, i * self.MAX_AUDIO_DURATION - self.OVERLAP_DURATION)
            end_time = min(duration, (i + 1) * self.MAX_AUDIO_DURATION + self.OVERLAP_DURATION)

            # 计算实际片段时长
            segment_duration = end_time - start_time

            # 创建临时文件路径
            segment_path = temp_dir / f"segment_{audio_path.stem}_{i:03d}.mp3"

            # 使用ffmpeg切割音频
            cmd = [
                "ffmpeg",
                "-i",
                str(audio_path),
                "-ss",
                str(start_time),  # 开始时间
                "-t",
                str(segment_duration),  # 持续时间
                "-acodec",
                "copy",  # 直接复制编码，提高速度
                "-y",
                str(segment_path),
            ]

            process = await asyncio.create_subprocess_exec(
                *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                # 清理已创建的片段
                for seg_path, _, _ in segments:
                    try:
                        seg_path.unlink()
                    except:
                        pass
                raise Exception(f"音频分片失败 (片段 {i}): {stderr.decode()}")

            segments.append((segment_path, start_time, end_time))

        return segments

    async def _process_long_audio(
        self, audio_path: Path, duration: float, show_progress: bool = True
    ) -> str:
        """处理长音频：分片、识别、合并"""
        # 1. 分片
        segments = await self._split_audio(audio_path, duration)

        if show_progress:
            print(f"共分割成 {len(segments)} 个片段")

        # 2. 并行识别每个片段
        tasks = []
        for i, (segment_path, start_time, end_time) in enumerate(segments):
            if show_progress:
                print(f"   处理片段 {i + 1}/{len(segments)}: {start_time:.1f}s - {end_time:.1f}s")

            task = self._transcribe_audio_segment(segment_path, i, show_progress)
            tasks.append(task)

        # 等待所有任务完成
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # 3. 合并结果
        merged_text = self._merge_transcriptions(results, segments)

        # 4. 清理临时片段文件
        for segment_path, _, _ in segments:
            try:
                segment_path.unlink()
            except:
                pass

        return merged_text

    async def _transcribe_audio_segment(
        self, segment_path: Path, segment_index: int, show_progress: bool = True
    ) -> dict:
        """转录单个音频片段"""
        try:
            text = await self._transcribe_audio(segment_path)

            if show_progress:
                print(f"   片段 {segment_index + 1} 识别完成: {len(text)}字符")

            return {"segment_index": segment_index, "text": text, "success": True, "error": None}
        except Exception as e:
            logger.error(f"片段 {segment_index} 识别失败: {e}")

            if show_progress:
                print(f"   片段 {segment_index + 1} 识别失败: {str(e)[:50]}...")

            return {"segment_index": segment_index, "text": "", "success": False, "error": str(e)}

    def _merge_transcriptions(
        self, results: List[dict], segments: List[Tuple[Path, float, float]]
    ) -> str:
        """合并多个片段的转录结果

        策略：
        1. 按时间顺序排序
        2. 处理重叠部分的文本
        3. 合并成连贯的文本
        """
        # 过滤成功的转录
        successful_results = [r for r in results if isinstance(r, dict) and r.get("success")]

        if not successful_results:
            return "所有片段识别失败"

        # 按片段索引排序
        successful_results.sort(key=lambda x: x["segment_index"])

        # 简单的合并策略：直接拼接
        # 在实际应用中，可以添加更智能的重叠处理
        merged_parts = []

        for i, result in enumerate(successful_results):
            text = result["text"].strip()
            if text:
                # 如果是第一个片段，直接添加
                if i == 0:
                    merged_parts.append(text)
                else:
                    # 添加换行分隔
                    merged_parts.append(f"{text}")

        return "\n".join(merged_parts)

    async def _transcribe_audio(self, audio_path: Path) -> str:
        """调用硅基流动API进行语音转文字"""
        # 检查文件大小（API可能有大小限制）
        file_size = audio_path.stat().st_size
        max_size = 25 * 1024 * 1024  # 25MB

        if file_size > max_size:
            # 如果文件太大，重新编码为更小的文件
            audio_path = await self._compress_audio(audio_path)

        async with aiofiles.open(audio_path, "rb") as f:
            audio_data = await f.read()

        data = aiohttp.FormData()
        data.add_field("file", audio_data, filename=audio_path.name)
        data.add_field("model", self.model)
        # 添加语言参数，提高中文识别准确率
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

    async def _compress_audio(self, audio_path: Path) -> Path:
        """压缩音频文件以减小大小"""
        temp_dir = Path(tempfile.gettempdir())
        compressed_path = temp_dir / f"compressed_{audio_path.stem}.mp3"

        cmd = [
            "ffmpeg",
            "-i",
            str(audio_path),
            "-acodec",
            "libmp3lame",
            "-b:a",
            "64k",  # 降低比特率
            "-ar",
            "16000",
            "-ac",
            "1",
            "-y",
            str(compressed_path),
        ]

        process = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            raise Exception(f"音频压缩失败: {stderr.decode()}")

        return compressed_path

    async def batch_extract(
        self, video_paths: List[Path], max_concurrent: int = 3, save_to_file: bool = True
    ) -> List[Tuple[str, Optional[Path]]]:
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
                return await self.extract_text(
                    video_path, show_progress=False, save_to_file=save_to_file
                )

        tasks = [extract_with_semaphore(path) for path in video_paths]
        return await asyncio.gather(*tasks, return_exceptions=True)


# 兼容性包装器，保持原有接口
async def extract_audio(video_path: Path, output_path: Path = None) -> Path:
    """兼容原有接口：从视频中提取音频"""
    agent = ExtractAgent()
    return await _extract_audio(video_path, output_path)


async def get_audio_duration(audio_path: Path) -> float:
    """兼容原有接口：获取音频时长"""
    agent = ExtractAgent()
    return await agent._get_audio_duration(audio_path)

"""文件处理工具"""

import asyncio
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict

import aiofiles
from loguru import logger


def check_ffmpeg():
    """检查ffmpeg是否可用"""
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        logger.info("ffmpeg可用")
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise Exception("ffmpeg未安装或不可用，请先安装ffmpeg")


async def extract_audio(video_path: Path, output_path: Path = None) -> Path:
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


async def save_text_to_file(video_path: Path, text: str) -> Path:
    """保存文本到同名txt文件

    Args:
        video_path: 视频文件路径
        text: 要保存的文本内容

    Returns:
        txt文件路径
    """
    # 生成txt文件路径（与视频文件同名，后缀为.txt）
    txt_path = video_path.with_suffix(".txt")

    # 保存文本
    async with aiofiles.open(txt_path, "w", encoding="utf-8") as f:
        await f.write(text)

    logger.info(f"文本已保存到: {txt_path}")
    return txt_path


async def compress_audio(audio_path: Path) -> Path:
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


def save_markdown(content: str, output_path: Path, metadata: Dict[str, Any] = None) -> Path:
    """保存为Markdown文件"""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    header = f"""#{metadata.get("title", "文案内容")}"""
    content = header + content

    output_path.write_text(content, encoding="utf-8")
    return output_path


def save_json(data: Any, output_path: Path) -> Path:
    """保存为JSON文件"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return output_path

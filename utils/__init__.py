"""工具函数模块"""

# 注意：audio.py中的函数已移动到agents.extract_agent.py
# 为了保持兼容性，从extract_agent导入
from agents.extract_agent import extract_audio, get_audio_duration
from .file import save_markdown, save_json

__all__ = [
    "extract_audio",
    "get_audio_duration",
    "save_markdown",
    "save_json",
]

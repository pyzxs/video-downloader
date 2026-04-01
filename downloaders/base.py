"""基础下载器抽象类"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional


@dataclass
class VideoInfo:
    """视频信息数据类"""

    video_id: str
    title: str
    url: str
    platform: str
    author: Optional[str] = None
    duration: Optional[int] = None
    thumbnail: Optional[str] = None
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class BaseDownloader(ABC):
    """下载器基类"""

    def __init__(self, output_dir: Path = Path("./output")):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    async def get_video_info(self, url: str) -> VideoInfo:
        """获取视频信息"""
        pass

    @abstractmethod
    async def download_video(
        self, video_info: VideoInfo, show_progress: bool = True
    ) -> Path:
        """下载视频"""
        pass

    @classmethod
    @abstractmethod
    def match_url(cls, url: str) -> bool:
        """判断是否支持该URL"""
        pass

    def _sanitize_filename(self, name: str) -> str:
        """清理文件名中的非法字符"""
        import re

        # 移除非法字符
        name = re.sub(r'[\\/:*?"<>|]', "_", name)
        # 限制长度
        return name[:200]

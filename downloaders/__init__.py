"""视频下载器模块"""

from .base import BaseDownloader, VideoInfo
from .douyin import DouyinDownloader
from .kuaishou import KuaishouDownloader
from .xiaohongshu import XiaohongshuDownloader
from .bilibili import BilibiliDownloader
from .youtube import YouTubeDownloader
from .other import OtherDownloader

__all__ = [
    "BaseDownloader",
    "VideoInfo",
    "DouyinDownloader",
    "KuaishouDownloader",
    "XiaohongshuDownloader",
    "BilibiliDownloader",
    "YouTubeDownloader",
    "OtherDownloader",
]

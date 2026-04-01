"""下载助手Agent - 协调各个下载器"""

from pathlib import Path
from typing import List, Optional, Type

from downloaders.base import BaseDownloader, VideoInfo
from downloaders.bilibili import BilibiliDownloader
from downloaders.douyin import DouyinDownloader
from downloaders.kuaishou import KuaishouDownloader
from downloaders.other import OtherDownloader
from downloaders.xiaohongshu import XiaohongshuDownloader
from downloaders.youtube import YouTubeDownloader


class DownloadAgent:
    """下载助手Agent，负责协调各个平台的下载器"""

    def __init__(
        self, output_dir: Path = Path("./output"), proxy: Optional[str] = None
    ):
        self.output_dir = output_dir
        self.proxy = proxy
        self.downloaders: List[Type[BaseDownloader]] = [
            DouyinDownloader,
            KuaishouDownloader,
            XiaohongshuDownloader,
            BilibiliDownloader,
            YouTubeDownloader,
            OtherDownloader,  # 兜底下载器，放在最后
        ]

    def _get_downloader(self, url: str) -> Optional[BaseDownloader]:
        """根据URL获取合适的下载器"""
        for downloader_class in self.downloaders:
            if downloader_class.match_url(url):
                downloader = downloader_class(self.output_dir)
                # 传递代理设置给支持代理的下载器
                if self.proxy:
                    if isinstance(downloader, YouTubeDownloader):
                        downloader.proxy = self.proxy
                        downloader.ydl_opts["proxy"] = self.proxy
                    elif isinstance(downloader, OtherDownloader):
                        downloader.proxy = self.proxy
                        downloader.ydl_opts["proxy"] = self.proxy
                return downloader
        return None

    async def get_video_info(self, url: str) -> VideoInfo:
        """获取视频信息"""
        downloader = self._get_downloader(url)
        if not downloader:
            raise Exception(f"不支持的URL: {url}")

        print(
            f"[OK] 识别到平台: {downloader.__class__.__name__.replace('Downloader', '')}"
        )
        return await downloader.get_video_info(url)

    async def download_video(
        self, url: str, show_progress: bool = True
    ) -> tuple[VideoInfo, Path]:
        """下载视频"""
        downloader = self._get_downloader(url)
        if not downloader:
            raise Exception(f"不支持的URL: {url}")

        print(
            f"[OK] 识别到平台: {downloader.__class__.__name__.replace('Downloader', '')}"
        )

        video_info = await downloader.get_video_info(url)
        print(f"[OK] 视频标题: {video_info.title}")

        video_path = await downloader.download_video(video_info, show_progress)

        return video_info, video_path

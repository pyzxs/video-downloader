#!/usr/bin/env python3
"""多平台视频下载和文案提取工具主入口"""

import argparse
import asyncio
import os
import sys
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# 导入本地模块
from agents.download_agent import DownloadAgent
from agents.extract_agent import ExtractAgent

# 自动加载 .env 文件
load_dotenv()


class VideoProcessor:
    """视频处理器"""

    def __init__(
        self,
        output_dir: Path = Path("/tmp/video-downloader" or os.environ.get("OUTPUT_DIR")),
        proxy: Optional[str] = None,
    ):
        self.output_dir = output_dir
        self.download_agent = DownloadAgent(output_dir, proxy)
        self.extract_agent = None
        self.segment_agent = None

    async def process(
        self,
        url: str,
        extract_text: bool = True,
        save_video: bool = True,
        api_key: Optional[str] = None,
    ) -> dict:
        """处理视频"""
        # 1. 下载视频
        print("\n" + "=" * 50)
        print("步骤 1/3: 下载视频")
        print("=" * 50)

        video_info, video_path = await self.download_agent.download_video(url)

        result = {
            "video_info": video_info,
            "video_path": video_path,
        }

        # 2. 提取文案（如果需要）
        if extract_text:
            print("\n" + "=" * 50)
            print("步骤 2/3: 提取文案")
            print("=" * 50)

            if not self.extract_agent:
                self.extract_agent = ExtractAgent(api_key)

            text, txt_path = await self.extract_agent.extract_text(video_path)
            result["text"] = text
            result["txt_path"] = txt_path  # 添加txt文件路径到结果

            # 保存文案
            result["output_path"] = txt_path

        if not save_video and video_path.exists():
            video_path.unlink()
            print(f"\n[OK] 临时视频文件已删除: {video_path}")

        return result


def main() -> int:
    """主入口函数"""
    parser = argparse.ArgumentParser(
        description="多平台视频下载和文案提取工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 获取视频信息
  video-downloader info "https://v.douyin.com/xxxxx"

  # 仅下载视频
  video-downloader download "https://v.douyin.com/xxxxx" -o ./videos

  # 提取文案
  video-downloader extract "https://v.douyin.com/xxxxx" -o ./output

  # 提取文案并保留视频
  video-downloader extract "https://v.douyin.com/xxxxx" --save-video

  # 完整处理（下载+提取）
  video-downloader process "https://v.douyin.com/xxxxx" -o ./output

支持平台:
  抖音、快手、B站、YouTube
        """,
    )

    parser.add_argument(
        "command",
        choices=["info", "download", "extract", "process"],
        help="命令: info(获取信息), download(下载视频), extract(提取文案), process(完整处理)",
    )
    parser.add_argument("url", help="视频分享链接")
    parser.add_argument("-o", "--output", default="./output", help="输出目录 (默认: ./output)")
    parser.add_argument(
        "--save-video",
        action="store_true",
        help="保存视频文件（仅extract/process命令）",
    )
    parser.add_argument(
        "--api-key", help="硅基流动API密钥（也可通过环境变量 SILI_FLOW_API_KEY 设置）"
    )
    parser.add_argument(
        "--proxy",
        help="代理服务器地址（例如: http://127.0.0.1:7890 或 socks5://127.0.0.1:7891）",
    )

    args = parser.parse_args()

    # 设置API密钥环境变量
    if args.api_key:
        os.environ["SILI_FLOW_API_KEY"] = args.api_key

    # 设置代理环境变量
    if args.proxy:
        os.environ["YOUTUBE_PROXY"] = args.proxy

    # 执行命令
    async def run() -> int:
        output_dir = Path(args.output)
        processor = VideoProcessor(output_dir, proxy=args.proxy)

        try:
            match args.command:
                case "info":
                    # 获取视频信息
                    video_info = await processor.download_agent.get_video_info(args.url)
                    print("\n" + "=" * 50)
                    print("视频信息:")
                    print("=" * 50)
                    print(f"平台: {video_info.platform}")
                    print(f"视频ID: {video_info.video_id}")
                    print(f"标题: {video_info.title}")
                    print(f"作者: {video_info.author or '未知'}")
                    print(f"时长: {video_info.duration or '未知'}秒")
                    print(f"下载链接: {video_info.url}")
                    if video_info.description:
                        print(f"\n描述:\n{video_info.description[:200]}...")
                    print("=" * 50)

                case "download":
                    # 仅下载视频
                    (
                        video_info,
                        video_path,
                    ) = await processor.download_agent.download_video(args.url)
                    print(f"\n[OK] 视频已保存: {video_path}")

                case "extract":
                    # 提取文案
                    result = await processor.process(
                        args.url,
                        extract_text=True,
                        save_video=args.save_video,
                    )

                    print("\n" + "=" * 50)
                    print("提取完成!")
                    print("=" * 50)
                    print(f"平台: {result['video_info'].platform}")
                    print(f"视频ID: {result['video_info'].video_id}")
                    print(f"标题: {result['video_info'].title}")
                    print(f"保存位置: {result['output_path']}")
                    print("=" * 50)

                    # 显示文案预览
                    text = result.get("segmented_text", result.get("text", ""))
                    if text:
                        print("\n文案预览:\n")
                        preview = text[:500]
                        if len(text) > 500:
                            preview += "..."
                        print(preview)
                        print("\n" + "=" * 50)

                case "process":
                    # 完整处理
                    result = await processor.process(
                        args.url,
                        extract_text=True,
                        save_video=args.save_video,
                    )

                    print("\n" + "=" * 50)
                    print("处理完成!")
                    print("=" * 50)
                    print(f"平台: {result['video_info'].platform}")
                    print(f"视频ID: {result['video_info'].video_id}")
                    print(f"标题: {result['video_info'].title}")
                    if args.save_video:
                        print(f"视频文件: {result['video_path']}")
                    print(f"文案文件: {result['output_path']}")
                    print("=" * 50)

                    # 显示文案预览
                    text = result.get("segmented_text", result.get("text", ""))
                    if text:
                        print("\n文案预览:\n")
                        preview = text[:500]
                        if len(text) > 500:
                            preview += "..."
                        print(preview)
                        print("\n" + "=" * 50)

                case _:
                    print(f"未知命令: {args.command}")
                    return 1

        except Exception as e:
            print(f"\n[ERROR] 错误: {e}", file=sys.stderr)
            import traceback

            traceback.print_exc()
            return 1

        return 0

    return asyncio.run(run())


if __name__ == "__main__":
    sys.exit(main())

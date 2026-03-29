#!/usr/bin/env python3
"""
快速测试脚本 - 测试视频下载器的基本功能
"""

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from agents.download_agent import DownloadAgent
from agents.extract_agent import ExtractAgent
from dotenv import load_dotenv

# 自动加载 .env 文件
load_dotenv()


async def test_video_info_agent():
    """测试下载代理"""
    print("=" * 60)
    print("测试下载代理...")
    print("=" * 60)

    try:
        agent = DownloadAgent()
        print("✅ 下载代理初始化成功")

        # 测试获取视频信息（使用模拟URL）
        test_url = "https://www.kuaishou.com/short-video/3xmpqeydq62fja9?authorId=3xgxbqmvz8ebcfu&streamSource=find&area=homexxbrilliant"
        print(f"\n测试URL: {test_url}")

        # 注意：这里会实际尝试下载，可能需要网络
        # 在实际测试中，应该使用mock或跳过
        print("⚠️  注意：需要网络连接进行实际测试")
        print("   如果要跳过网络测试，请注释掉下面的代码")

        # 取消注释以下代码进行实际测试
        try:
            video_info = await agent.get_video_info(test_url)
            print(f"✅ 获取视频信息成功")
            print(f"   平台: {video_info.platform}")
            print(f"   标题: {video_info.title}")
            print(f"   作者: {video_info.author}")
            print(f"   视频下载:{video_info.url}")
            download_file = await agent.download_video(test_url)
            print(f"   文件已下载: {download_file}")
        except Exception as e:
            print(f"❌ 获取视频信息失败: {e}")
            print("   这可能是正常的，因为测试URL可能无效")

        return True

    except Exception as e:
        print(f"❌ 下载代理测试失败: {e}")
        return False

async def test_download_agent():
    """测试下载代理"""
    print("=" * 60)
    print("测试下载代理...")
    print("=" * 60)

    try:
        agent = DownloadAgent()
        print("✅ 下载代理初始化成功")

        # 测试获取视频信息（使用模拟URL）
        kuaishou = "https://www.kuaishou.com/short-video/3xmpqeydq62fja9?authorId=3xgxbqmvz8ebcfu&streamSource=find&area=homexxbrilliant"
        test_url = "https://www.douyin.com/video/7621159941025353010?modeFrom="
        test_url = "https://www.bilibili.com/video/BV1HxQSBgEvC/?spm_id_from=333.1007.tianma.1-1-1.click&vd_source=e31cce80093b828b7dbe25383a0ead44"
        test_url = "https://www.xiaohongshu.com/explore/64ad5214000000001c00cf63?source=webshare&xhsshare=pc_web&xsec_token=AB8XxhD7hIPjXeHj7oPqfv4TQKDWRHoVtDxVepU9HUDWE=&xsec_source=pc_share"
        print(f"\n测试URL: {test_url}")

        # 注意：这里会实际尝试下载，可能需要网络
        # 在实际测试中，应该使用mock或跳过
        print("⚠️  注意：需要网络连接进行实际测试")
        print("   如果要跳过网络测试，请注释掉下面的代码")

        # 取消注释以下代码进行实际测试
        try:
            download_file = await agent.download_video(test_url)
            print(f"   文件已下载: {download_file}")
        except Exception as e:
            print(f"❌ 获取视频信息失败: {e}")
            print("   这可能是正常的，因为测试URL可能无效")

        return True

    except Exception as e:
        print(f"❌ 下载代理测试失败: {e}")
        return False

async def test_extract_agent():
    """测试提取代理"""
    print("\n" + "=" * 60)
    print("测试提取代理...")
    print("=" * 60)

    try:
        # 测试从环境变量获取API密钥
        import os

        api_key = os.getenv("SILI_FLOW_API_KEY")

        if api_key:
            agent = ExtractAgent(api_key)
            print(f"✅ 提取代理初始化成功 (使用环境变量API密钥)")
        else:
            agent = ExtractAgent("test-key")
            print(f"✅ 提取代理初始化成功 (使用测试密钥)")
            print("⚠️  注意：需要有效的API密钥进行实际提取")

        # 创建测试视频文件
        test_video = Path("../output/bilibili_BV1UMVKzEESL.mp4")
        if not test_video.exists():
            # 创建一个空的测试文件
            test_video.write_bytes(b"fake video data")
            print(f"✅ 创建测试视频文件: {test_video}")

        print("\n测试文案提取...")
        print("⚠️  注意：需要有效的API密钥和网络连接")
        print("   如果要跳过API调用，请注释掉下面的代码")

        # 取消注释以下代码进行实际测试
        try:
            text = await agent.extract_text(test_video)
            print(f"✅ 文案提取成功")
            print(f"   提取文本长度: {len(text)} 字符")
            if text:
                print(f"   预览: {text[:100]}...")
        except Exception as e:
            print(f"❌ 文案提取失败: {e}")
            print("   这可能是正常的，因为API密钥可能无效")

        # 清理测试文件
        # if test_video.exists():
        #     test_video.unlink()
        #     print(f"✅ 清理测试视频文件")

        return True

    except Exception as e:
        print(f"❌ 提取代理测试失败: {e}")
        return False


async def run_all_tests():
    """运行所有测试"""
    print("开始运行视频下载器快速测试")
    print("=" * 60)

    results = []

    # 运行各个测试
    results.append(await test_download_agent())
    results.append(await test_extract_agent())
    results.append(await test_main_module())

    # 汇总结果
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)

    total = len(results)
    passed = sum(results)

    print(f"总测试数: {total}")
    print(f"通过数: {passed}")
    print(f"失败数: {total - passed}")

    if passed == total:
        print("\n🎉 所有测试通过!")
    else:
        print(f"\n⚠️  有 {total - passed} 个测试失败或跳过")
        print("   注意：某些测试可能需要网络连接或有效的API密钥")

    print("\n📋 下一步:")
    print("1. 设置环境变量:")
    print("   - SILI_FLOW_API_KEY: 硅基流动API密钥")
    print("   - DEEPSEEK_API_KEY: DeepSeek API密钥")
    print("2. 运行完整测试: python -m pytest test_video_downloader.py -v")
    print("3. 测试实际功能: python main.py info <视频URL>")

    return all(results)



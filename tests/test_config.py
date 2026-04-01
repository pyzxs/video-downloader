#!/usr/bin/env python3
"""
测试配置文件
用于设置测试环境和参数
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


# 测试配置
class TestConfig:
    """测试配置类"""

    # 目录配置
    TEST_OUTPUT_DIR = Path("./test_output")
    TEST_DATA_DIR = Path("./test_data")

    # API密钥配置（从环境变量获取）
    SILI_FLOW_API_KEY = os.getenv("SILI_FLOW_API_KEY", "test_sili_flow_key")
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "test_deepseek_key")

    # 测试URLs（模拟）
    TEST_URLS = {
        "douyin": "https://v.douyin.com/test_douyin_123",
        "kuaishou": "https://v.kuaishou.com/test_kuaishou_456",
        "xiaohongshu": "https://www.xiaohongshu.com/test_xhs_789",
        "bilibili": "https://www.bilibili.com/video/BV1test123",
        "youtube": "https://www.youtube.com/watch?v=test_youtube_456",
    }

    # 测试视频信息
    TEST_VIDEO_INFO = {
        "douyin": {
            "id": "test_douyin_123",
            "title": "抖音测试视频标题",
            "uploader": "抖音测试作者",
            "duration": 120,
            "description": "这是一个抖音测试视频的描述",
            "extractor": "douyin",
        },
        "kuaishou": {
            "id": "test_kuaishou_456",
            "title": "快手测试视频标题",
            "uploader": "快手测试作者",
            "duration": 90,
            "description": "这是一个快手测试视频的描述",
            "extractor": "kuaishou",
        },
    }

    # 测试文本
    TEST_TEXTS = {
        "short": "这是一个简短的测试文本。",
        "medium": """这是一个中等长度的测试文本。
包含多个句子和段落。
用于测试文案提取和分段功能。
每个段落讨论不同的主题。""",
        "long": """这是一个较长的测试文本，用于全面测试功能。

第一部分：介绍
这是文本的第一部分，介绍测试的目的和背景。
测试视频下载器的文案提取和语义分段功能。

第二部分：详细内容
这是第二部分，包含更详细的内容。
讨论视频处理的技术细节和实现方法。
包括下载、提取、分段等步骤。

第三部分：总结
这是最后一部分，总结测试结果。
评估功能的性能和准确性。
提出改进建议和下一步计划。""",
    }

    # 测试文件配置
    TEST_FILES = {
        "small_video": {
            "path": TEST_DATA_DIR / "small_test_video.mp4",
            "size_kb": 100,  # 模拟的小视频文件大小
        },
        "large_video": {
            "path": TEST_DATA_DIR / "large_test_video.mp4",
            "size_kb": 10240,  # 模拟的大视频文件大小
        },
    }

    # 测试标记
    SKIP_NETWORK_TESTS = os.getenv("SKIP_NETWORK_TESTS", "false").lower() == "true"
    SKIP_API_TESTS = os.getenv("SKIP_API_TESTS", "false").lower() == "true"
    RUN_INTEGRATION_TESTS = (
        os.getenv("RUN_INTEGRATION_TESTS", "false").lower() == "true"
    )

    @classmethod
    def setup_test_environment(cls):
        """设置测试环境"""
        # 创建测试目录
        cls.TEST_OUTPUT_DIR.mkdir(exist_ok=True)
        cls.TEST_DATA_DIR.mkdir(exist_ok=True)

        # 创建测试文件
        for file_info in cls.TEST_FILES.values():
            if not file_info["path"].exists():
                # 创建模拟文件
                file_info["path"].write_bytes(b"0" * (file_info["size_kb"] * 1024))
                print(f"创建测试文件: {file_info['path']}")

    @classmethod
    def cleanup_test_environment(cls):
        """清理测试环境"""
        import shutil

        # 删除测试输出目录
        if cls.TEST_OUTPUT_DIR.exists():
            shutil.rmtree(cls.TEST_OUTPUT_DIR)
            print(f"清理测试输出目录: {cls.TEST_OUTPUT_DIR}")

        # 删除测试数据目录
        if cls.TEST_DATA_DIR.exists():
            shutil.rmtree(cls.TEST_DATA_DIR)
            print(f"清理测试数据目录: {cls.TEST_DATA_DIR}")

    @classmethod
    def get_test_url(cls, platform="douyin"):
        """获取测试URL"""
        return cls.TEST_URLS.get(platform, cls.TEST_URLS["douyin"])

    @classmethod
    def get_test_video_info(cls, platform="douyin"):
        """获取测试视频信息"""
        return cls.TEST_VIDEO_INFO.get(platform, cls.TEST_VIDEO_INFO["douyin"])

    @classmethod
    def get_test_text(cls, length="medium"):
        """获取测试文本"""
        return cls.TEST_TEXTS.get(length, cls.TEST_TEXTS["medium"])


# 导出配置实例
config = TestConfig()

if __name__ == "__main__":
    # 测试配置
    print("测试配置信息:")
    print(f"测试输出目录: {config.TEST_OUTPUT_DIR}")
    print(f"测试数据目录: {config.TEST_DATA_DIR}")
    print(f"跳过网络测试: {config.SKIP_NETWORK_TESTS}")
    print(f"跳过API测试: {config.SKIP_API_TESTS}")
    print(f"运行集成测试: {config.RUN_INTEGRATION_TESTS}")
    print(f"测试URLs: {list(config.TEST_URLS.keys())}")

    # 设置测试环境
    config.setup_test_environment()

    print("\n测试环境设置完成!")
    print("使用示例:")
    print(f"  测试URL: {config.get_test_url('douyin')}")
    print(f"  测试文本: {config.get_test_text('short')[:50]}...")

#!/usr/bin/env python3
"""检查项目依赖是否完整"""

import sys

# 项目所需的依赖包
REQUIRED_DEPS = [
    "aiohttp",
    "aiofiles",
    "yt-dlp",
    "openai",
    "click",
    "python-dotenv",
    "loguru",
]

# 可选依赖（用于特定功能）
OPTIONAL_DEPS = [
    "moviepy",  # 音频处理（可能不需要）
    "numpy",  # moviepy的依赖
]


def check_package(package_name):
    """检查包是否可导入"""
    # 特殊处理一些包的导入名称
    import_map = {
        "python-dotenv": "dotenv",
        "yt-dlp": "yt_dlp",
    }

    import_name = import_map.get(package_name, package_name.replace("-", "_"))

    try:
        __import__(import_name)
        return True
    except ImportError:
        return False


def main():
    print("=" * 60)
    print("视频下载器项目依赖检查")
    print("=" * 60)

    print(f"\nPython版本: {sys.version}")
    print(f"Python路径: {sys.executable}")

    print("\n" + "=" * 60)
    print("必需依赖检查:")
    print("=" * 60)

    missing_required = []
    for dep in REQUIRED_DEPS:
        if check_package(dep):
            print(f"[OK] {dep}")
        else:
            print(f"[MISSING] {dep} - 缺失")
            missing_required.append(dep)

    print("\n" + "=" * 60)
    print("可选依赖检查:")
    print("=" * 60)

    missing_optional = []
    for dep in OPTIONAL_DEPS:
        if check_package(dep):
            print(f"[OK] {dep}")
        else:
            print(f"[MISSING] {dep} - 缺失")
            missing_optional.append(dep)

    print("\n" + "=" * 60)
    print("项目模块导入检查:")
    print("=" * 60)

    # 检查项目模块
    project_modules = [
        "downloaders.youtube",
        "downloaders.bilibili",
        "downloaders.douyin",
        "downloaders.kuaishou",
        "downloaders.xiaohongshu",
        "agents.download_agent",
        "agents.extract_agent",
        "agents.segment_agent",
        "utils.file",
    ]

    missing_modules = []
    for module in project_modules:
        try:
            __import__(module)
            print(f"[OK] {module}")
        except ImportError as e:
            print(f"[ERROR] {module} - 导入失败: {e}")
            missing_modules.append(module)

    print("\n" + "=" * 60)
    print("检查结果汇总:")
    print("=" * 60)

    if missing_required:
        print(f"\n[CRITICAL] 缺失必需依赖 ({len(missing_required)}个):")
        for dep in missing_required:
            print(f"  - {dep}")
    else:
        print("\n[SUCCESS] 所有必需依赖已安装")

    if missing_optional:
        print(f"\n[WARNING] 缺失可选依赖 ({len(missing_optional)}个):")
        for dep in missing_optional:
            print(f"  - {dep}")

    if missing_modules:
        print(f"\n[WARNING] 项目模块导入问题 ({len(missing_modules)}个):")
        for module in missing_modules:
            print(f"  - {module}")

    print("\n" + "=" * 60)
    print("建议操作:")
    print("=" * 60)

    if missing_required:
        print("\n1. 安装缺失的必需依赖:")
        print(f"   uv pip install {' '.join(missing_required)}")

    if missing_optional and "moviepy" in missing_optional:
        print("\n2. moviepy可能不是必需的:")
        print("   检查utils/audio.py是否直接使用ffmpeg")
        print("   如果是，可以考虑从pyproject.toml中移除moviepy依赖")

    print("\n3. 测试CLI是否工作:")
    print("   python main.py --help")

    return 0 if not missing_required else 1


if __name__ == "__main__":
    sys.exit(main())

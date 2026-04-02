---
name: jl-video-downloader
description: 多平台视频下载和文案提取工具。支持抖音、快手、小红书、B站、YouTube等平台的视频下载和语音转文字功能。当用户需要下载视频、提取视频文案或批量处理视频时激活此技能。
allowed-tools: Bash, Python
triggers:
  - "下载视频"
  - "提取文案"
  - "文案提取"
  - "视频下载"
  - "视频信息"
  - "抖音下载"
  - "B站下载"
  - "YouTube下载"
  - "视频转文字"
  - "语音转文字"
---

# JL Video Downloader OpenClaw Skill

多平台视频下载和文案提取工具，支持抖音、快手、小红书、B站、YouTube等主流视频平台。

## 快速开始

### 1. 环境检查
```bash
# 检查Python版本（需要 >= 3.12）
python --version

# 检查ffmpeg（必需）
ffmpeg --version

# 检查uv工具
uv --version
```

### 2. 安装工具
```bash
# 使用uv安装（推荐）
uv tool install jl-video-downloader

# 使用清华镜像源安装
uv tool install jl-video-downloader --index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 或使用阿里云镜像
uv tool install jl-video-downloader --index-url https://mirrors.aliyun.com/pypi/simple/

# 或使用中科大镜像
uv tool install jl-video-downloader --index-url https://pypi.mirrors.ustc.edu.cn/simple/
```

### 3. 配置环境变量
```bash
# API密钥配置（文案提取必需）
export SILI_FLOW_API_KEY="sk-your-siliflow-api-key"
export DEEPSEEK_API_KEY="sk-your-deepseek-api-key"

# 代理配置（可选，用于访问YouTube等）
export YOUTUBE_PROXY="http://127.0.0.1:7897"
export GLOBAL_PROXY="http://127.0.0.1:7897"

# 输出目录配置
export OUTPUT_DIR="$HOME/videos"
```

## 基本用法

### 查看帮助
```bash
uvx jl-video-downloader --help
```

### 获取视频信息
```bash
uvx jl-video-downloader info <视频URL>
```

### 下载视频
```bash
uvx jl-video-downloader download <视频URL>

# 指定输出目录
uvx jl-video-downloader download <视频URL> -o ./my_videos

# 使用代理
uvx jl-video-downloader download <视频URL> --proxy http://127.0.0.1:7897
```

### 提取文案
```bash
uvx jl-video-downloader extract <视频URL>

# 提取文案并保存视频
uvx jl-video-downloader extract <视频URL> --save-video

# 禁用语义分段
uvx jl-video-downloader extract <视频URL> --no-segment

# 指定API密钥
uvx jl-video-downloader extract <视频URL> --api-key "sk-xxx" --deepseek-key "sk-yyy"
```

### 完整处理（下载+提取）
```bash
uvx jl-video-downloader process <视频URL>
```

### 批量处理
```bash
# 创建URL列表文件
echo "https://v.douyin.com/url1" > urls.txt
echo "https://www.bilibili.com/video/BV1xxx" >> urls.txt

# 批量处理
uvx jl-video-downloader batch urls.txt
```

## 支持的平台

| 平台 | 支持状态 | 备注 |
|------|----------|------|
| 抖音 (Douyin) | ✅ 支持 | 需要处理反爬机制 |
| 快手 (Kuaishou) | ✅ 支持 |  |
| 小红书 (Xiaohongshu) | ✅ 支持 |  |
| B站 (Bilibili) | ✅ 支持 | 支持BV号、短链接等格式 |
| YouTube | ✅ 支持 | 可能需要代理 |
| 其他平台 | ✅ 支持 | 通过yt-dlp支持 |

## 平台特定示例

### 抖音 (Douyin)
```bash
# 短链接格式
uvx jl-video-downloader process "https://v.douyin.com/xxxxx"

# 完整链接格式
uvx jl-video-downloader process "https://www.douyin.com/video/7301234567890123456"
```

### B站 (Bilibili)
```bash
# BV号格式
uvx jl-video-downloader process "https://www.bilibili.com/video/BV1GJ41187Q7"

# 短链接格式
uvx jl-video-downloader process "https://b23.tv/xxxxx"

# 带有时间戳
uvx jl-video-downloader process "https://www.bilibili.com/video/BV1xxx?t=60"
```

### YouTube
```bash
# 需要代理（如果在中国）
uvx jl-video-downloader process "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --proxy http://127.0.0.1:7897

# 播放列表
uvx jl-video-downloader process "https://www.youtube.com/playlist?list=xxxx"
```

### 快手 (Kuaishou)
```bash
uvx jl-video-downloader process "https://v.kuaishou.com/xxxxx"
```

### 小红书 (Xiaohongshu)
```bash
uvx jl-video-downloader process "https://www.xiaohongshu.com/explore/xxxxx"
```

## 高级配置

### 持久化环境变量
创建配置文件 `~/.jl-video-downloader/env`：
```bash
# API密钥
SILI_FLOW_API_KEY="sk-your-siliflow-key"
DEEPSEEK_API_KEY="sk-your-deepseek-key"

# 代理设置
YOUTUBE_PROXY="http://127.0.0.1:7897"
GLOBAL_PROXY="http://127.0.0.1:7897"

# 输出设置
OUTPUT_DIR="$HOME/Downloads/videos"
VIDEO_FILENAME_TEMPLATE="{platform}_{date}_{title}"

# 下载设置
DOWNLOAD_TIMEOUT=600
MAX_RETRIES=5
CONCURRENT_DOWNLOADS=3

# 日志设置
LOG_LEVEL="INFO"
LOG_FILE="$HOME/.jl-video-downloader/video-dl.log"
```

加载配置：
```bash
# 创建加载脚本
cat > ~/.jl-video-downloader/load_env.sh << 'EOF'
#!/bin/bash
if [ -f ~/.jl-video-downloader/env ]; then
    while IFS='=' read -r key value; do
        if [[ ! $key =~ ^# ]] && [[ -n $key ]]; then
            export "$key"="$value"
        fi
    done < ~/.jl-video-downloader/env
fi
EOF

chmod +x ~/.jl-video-downloader/load_env.sh
source ~/.jl-video-downloader/load_env.sh
```

### 添加到shell配置
```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
echo 'source ~/.jl-video-downloader/load_env.sh' >> ~/.bashrc
```

## 故障排除

### 常见问题

#### 1. "uv: command not found"
```bash
# 安装uv工具
curl -LsSf https://astral.sh/uv/install.sh | sh
# 或
pip install uv
```

#### 2. "ffmpeg: command not found"
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# CentOS/RHEL
sudo yum install ffmpeg
```

#### 3. API密钥错误
```bash
# 检查环境变量
echo $SILI_FLOW_API_KEY
echo $DEEPSEEK_API_KEY

# 重新配置
echo 'export SILI_FLOW_API_KEY="sk-your-key"' >> ~/.jl-video-downloader/env
source ~/.jl-video-downloader/load_env.sh
```

#### 4. 代理连接失败
```bash
# 测试代理
curl --proxy http://127.0.0.1:7897 https://www.google.com

# 更新代理配置
echo 'export YOUTUBE_PROXY="http://127.0.0.1:7897"' >> ~/.jl-video-downloader/env
source ~/.jl-video-downloader/load_env.sh
```

#### 5. 下载速度慢
```bash
# 使用代理
uvx jl-video-downloader download <URL> --proxy http://127.0.0.1:7897

# 调整超时时间
export DOWNLOAD_TIMEOUT=600
```

### 调试模式
```bash
# 查看详细日志
export LOG_LEVEL="DEBUG"
uvx jl-video-downloader process <URL>

# 查看Python错误
python -c "import main; main.main()" --help
```

## 在OpenClaw工作流中的使用

### 示例工作流
```bash
#!/bin/bash
# openclaw_video_workflow.sh

# 1. 检查并安装工具
if ! command -v uv &> /dev/null; then
    pip install uv
fi

if ! uv tool list | grep -q "jl-video-downloader"; then
    uv tool install jl-video-downloader
fi

# 2. 加载配置
if [ -f ~/.jl-video-downloader/load_env.sh ]; then
    source ~/.jl-video-downloader/load_env.sh
fi

# 3. 处理视频
URL="$1"
OUTPUT_DIR="${2:-./output}"

echo "开始处理视频: $URL"
echo "输出目录: $OUTPUT_DIR"

# 完整处理
uvx jl-video-downloader process "$URL" -o "$OUTPUT_DIR"

# 4. 输出结果
echo "视频处理完成"
echo "输出文件:"
ls -la "$OUTPUT_DIR/"
```

### 与其他技能集成
```bash
# 在browser技能后使用
browser extract "获取页面中的视频链接" | while read url; do
    uvx jl-video-downloader download "$url" -o ./videos
done

# 与data-scraper技能结合
scraper extract "video_urls" | uvx jl-video-downloader batch
```

## 性能优化

### 并发下载
```bash
# 调整并发数
export CONCURRENT_DOWNLOADS=5

# 使用parallel工具进行批量并发
cat urls.txt | parallel -j 5 "uvx jl-video-downloader download {}"
```

### 缓存配置
```bash
# 设置缓存目录
export VIDEO_DOWNLOADER_CACHE_DIR="$HOME/.cache/jl-video-downloader"

# 清理缓存
rm -rf ~/.cache/jl-video-downloader/*
```

## 更新和维护

### 更新工具
```bash
# 更新uv
uv self update

# 更新jl-video-downloader
uv tool upgrade jl-video-downloader
```

### 重新安装
```bash
# 卸载
uv tool uninstall jl-video-downloader

# 重新安装
uv tool install jl-video-downloader
```

### 备份配置
```bash
# 备份配置
cp -r ~/.jl-video-downloader ~/.jl-video-downloader.backup

# 恢复配置
cp -r ~/.jl-video-downloader.backup ~/.jl-video-downloader
```

## 许可证

MIT License

## 支持与反馈

如有问题或建议，请通过以下方式反馈：
1. 项目GitHub Issues
2. OpenClaw社区
3. 开发者邮箱

---

**使用提示**: 首次使用前请确保配置好API密钥和ffmpeg工具。对于YouTube视频，可能需要配置代理服务器。
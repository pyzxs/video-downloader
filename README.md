# JL Video Downloader

多平台视频下载和文案提取工具 - 支持抖音、快手、小红书、B站、YouTube等主流视频平台。

## 功能特性

- **多平台支持**: 抖音、快手、小红书、B站、YouTube等主流平台
- **文案提取**: 语音转文字，支持长音频分片处理
- **批量处理**: 支持批量下载和文案提取
- **进度显示**: 实时进度条显示下载状态
- **异步下载**: 提高下载效率
- **智能分段**: 自动语义分段，提高可读性
- **代理支持**: 支持HTTP/SOCKS5代理

## 作为OpenClaw Skill使用

本项目已配置为OpenClaw技能，可以直接在OpenClaw中使用。

### Skill信息
- **名称**: jl-video-downloader
- **描述**: 多平台视频下载和文案提取工具
- **技能文件**: [SKILL.md](SKILL.md) - 完整的OpenClaw技能文档

### 快速开始
```bash
# 1. 安装uv工具（如果未安装）
pip install uv

# 2. 安装jl-video-downloader
uv tool install jl-video-downloader

# 3. 配置环境变量
export SILI_FLOW_API_KEY="sk-your-key"
export DEEPSEEK_API_KEY="sk-your-key"

# 4. 使用
uvx jl-video-downloader --help
```

## 安装

### 使用uv安装（推荐）
```bash
# 从PyPI安装
uv tool install jl-video-downloader

# 或从本地项目安装
uv tool install /path/to/video-downloader
```

### 使用pip安装
```bash
pip install jl-video-downloader
```

### 从源码安装
```bash
# 克隆仓库
git clone <repository-url>
cd video-downloader

# 安装依赖
uv sync

# 安装为可执行包
uv pip install -e .
```

## 配置

### 环境变量配置
```bash
# API密钥配置（文案提取必需）
export SILI_FLOW_API_KEY="sk-your-siliflow-api-key"
export DEEPSEEK_API_KEY="sk-your-deepseek-api-key"

# 代理配置（可选，用于访问YouTube等）
export YOUTUBE_PROXY="http://127.0.0.1:7897"
export GLOBAL_PROXY="http://127.0.0.1:7897"

# 输出目录配置
export OUTPUT_DIR="$HOME/videos"

# 下载配置
export DOWNLOAD_TIMEOUT=300
export MAX_RETRIES=3
```

### 持久化配置
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
```

加载配置脚本：
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

## 使用方法

### 基本命令
```bash
# 查看帮助
uvx jl-video-downloader --help

# 获取视频信息
uvx jl-video-downloader info <视频URL>

# 下载视频
uvx jl-video-downloader download <视频URL>

# 提取文案
uvx jl-video-downloader extract <视频URL>

# 完整处理（下载+提取）
uvx jl-video-downloader process <视频URL>

# 批量处理
uvx jl-video-downloader batch <URL列表文件>
```

### 常用选项
```bash
# 指定输出目录
uvx jl-video-downloader download <URL> -o ./my_videos

# 使用代理
uvx jl-video-downloader download <URL> --proxy http://127.0.0.1:7897

# 提取文案并保存视频
uvx jl-video-downloader extract <URL> --save-video

# 禁用语义分段
uvx jl-video-downloader extract <URL> --no-segment
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

## 平台示例

### 抖音
```bash
uvx jl-video-downloader process "https://v.douyin.com/xxxxx"
uvx jl-video-downloader process "https://www.douyin.com/video/7301234567890123456"
```

### B站
```bash
uvx jl-video-downloader process "https://www.bilibili.com/video/BV1GJ41187Q7"
uvx jl-video-downloader process "https://b23.tv/xxxxx"
```

### YouTube
```bash
uvx jl-video-downloader process "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --proxy http://127.0.0.1:7897
```

### 快手
```bash
uvx jl-video-downloader process "https://v.kuaishou.com/xxxxx"
```

### 小红书
```bash
uvx jl-video-downloader process "https://www.xiaohongshu.com/explore/xxxxx"
```

## 批量处理

### 创建URL列表
```bash
cat > urls.txt << EOF
https://v.douyin.com/url1
https://www.bilibili.com/video/BV1xxx
https://www.youtube.com/watch?v=video1
EOF
```

### 批量下载
```bash
uvx jl-video-downloader batch urls.txt -o ./batch_output
```

### 并发处理
```bash
# 使用GNU parallel
cat urls.txt | parallel -j 3 "uvx jl-video-downloader process {} -o ./concurrent_output"
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

## 开发

### 项目结构
```
video-downloader/
├── agents/           # 代理模块
│   ├── download_agent.py    # 下载代理
│   └── extract_agent.py     # 文案提取代理
├── downloaders/      # 平台下载器
│   ├── base.py      # 基础下载器
│   ├── douyin.py    # 抖音下载器
│   ├── bilibili.py  # B站下载器
│   └── ...
├── utils/           # 工具函数
├── tests/           # 测试文件
├── main.py          # 主入口
├── pyproject.toml   # 项目配置
└── SKILL.md         # OpenClaw技能定义
```

### 运行测试
```bash
# 安装开发依赖
uv sync --group dev

# 运行测试
pytest

# 代码格式化
ruff format .

# 代码检查
ruff check .
```

### 添加新的平台支持
1. 在`downloaders/`目录下创建新的下载器类
2. 继承`BaseDownloader`基类
3. 实现`get_video_info()`和`download_video()`方法
4. 在`DownloadAgent`中注册新的下载器

## 许可证

MIT License

## 支持

- 项目GitHub: [链接]
- OpenClaw社区: [链接]
- 问题反馈: 通过GitHub Issues

---

**提示**: 首次使用前请确保配置好API密钥和ffmpeg工具。对于YouTube视频，可能需要配置代理服务器。
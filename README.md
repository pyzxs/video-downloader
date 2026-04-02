# Video Downloader

多平台视频下载和文案提取工具 - 支持抖音、快手、小红书、B站、YouTube等。

## 功能特性

- 支持多个视频平台下载
- 自动提取视频文案（语音转文字）
- 批量下载支持
- 进度条显示
- 异步下载，提高效率
- OpenClaw技能集成

### 使用示例
```bash
# 下载视频
jl-video-downloader download "https://v.douyin.com/xxxxx"

# 提取文案
jl-video-downloader extract "https://www.bilibili.com/video/BV1xxx"

# 完整处理
jl-video-downloader process "https://www.youtube.com/watch?v=xxxx"
```



## 配置

### 环境变量

```bash
export SILI_FLOW_API_KEY="sk-xxxxxxxxxxxxxxxx"
export DEEPSEEK_API_KEY="sk-xxxxxxxxxxxxxxxx"

# 代理配置（可选）
export YOUTUBE_PROXY="http://127.0.0.1:7897"
export GLOBAL_PROXY="http://127.0.0.1:7897"

# 输出目录
export OUTPUT_DIR="/tmp/output"
```

### 使用uv安装

```bash
uv tool install jl-video-downloader
```

## 使用方法

```bash
# 查看帮助
jl-video-downloader --help

# 下载单个视频
jl-video-downloader download <视频URL>

# 批量下载
jl-video-downloader batch <包含URL的文件>

# 提取视频文案
jl-video-downloader extract <视频URL>
```

## 支持的平台

- 抖音 (Douyin)
- 快手 (Kuaishou)
- 小红书 (Xiaohongshu)
- B站 (Bilibili)
- YouTube
- 其他支持 yt-dlp


# Video Downloader

多平台视频下载和文案提取工具 - 支持抖音、快手、小红书、B站、YouTube等。

## 功能特性

- 支持多个视频平台下载
- 自动提取视频文案（语音转文字）
- 批量下载支持
- 进度条显示
- 异步下载，提高效率

## 安装

### 使用 uv (推荐)

```bash
# 克隆仓库
git clone <repository-url>
cd video-downloader

# 安装依赖
uv sync

# 安装为可执行包
uv pip install -e .
```

### 使用 pip

```bash
pip install -e .
```

## 使用方法

```bash
# 查看帮助
video-dl --help

# 下载单个视频
video-dl download <视频URL>

# 批量下载
video-dl batch <包含URL的文件>

# 提取视频文案
video-dl extract <视频URL>
```

## 支持的平台

- 抖音 (Douyin)
- 快手 (Kuaishou)
- 小红书 (Xiaohongshu)
- B站 (Bilibili)
- YouTube
- 其他支持 yt-dlp 的平台

## 配置

复制 `.env.example` 到 `.env` 并填写必要的 API 密钥：

```bash
cp .env.example .env
```

## 开发

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

## 许可证

MIT License
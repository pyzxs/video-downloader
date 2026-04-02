---
name: video-downloader
description: 多平台视频下载和文案提取工具。支持抖音、快手、小红书、B站、YouTube等平台的视频下载和语音转文字功能。通过uv工具安装，使用uvx直接运行。
allowed-tools: Bash, Python
triggers:
  - "下载视频"
  - "提取文案"
  - "文案提取"
  - "视频下载"
  - "视频信息"
  - 
---

## 使用方法

### 基本命令
```bash
# 查看帮助
uvx video-downloader --help

# 下载单个视频
uvx video-downloader download <视频URL>

# 提取视频文案
uvx video-downloader extract <视频URL>

# 完整处理（下载+提取）
uvx video-downloader process <视频URL>
```


## 支持的平台

| 平台 | 支持状态 | 备注 |
|------|----------|------|
| 抖音 (Douyin) | ✅ 支持 | 需要处理反爬机制 |
| 快手 (Kuaishou) | ✅ 支持 |  |
| 小红书 (Xiaohongshu) | ✅ 支持 |  |
| B站 (Bilibili) | ✅ 支持 |  |
| YouTube | ✅ 支持 | 可能需要代理 |
| 其他平台 | ✅ 支持 | 通过yt-dlp支持 |

## 配置说明

### 必要环境变量
```bash
# API密钥配置
export SILI_FLOW_API_KEY="sk-xxxxxxxxxxxxxxxx"
export DEEPSEEK_API_KEY="sk-xxxxxxxxxxxxxxxx"

# 代理配置（可选）
export YOUTUBE_PROXY="http://127.0.0.1:7897"
export GLOBAL_PROXY="http://127.0.0.1:7897"

# 输出目录
export OUTPUT_DIR="$HOME/videos"
```

## 在OpenClaw中的使用

### 激活条件
当用户需要以下功能时激活此技能：
- 下载视频文件
- 提取视频文案（语音转文字）
- 批量处理视频链接
- 支持多平台视频处理

### 使用示例
```bash
# 示例1：下载抖音视频
uvx video-downloader download "https://v.douyin.com/xxxxx"

# 示例2：提取B站视频文案
uvx video-downloader extract "https://www.bilibili.com/video/BV1xxx"

# 示例3：批量处理
echo "https://v.douyin.com/xxxxx" > urls.txt
echo "https://www.bilibili.com/video/BV1xxx" >> urls.txt
uvx video-downloader batch urls.txt
```

## 故障排除

### 常见问题

1. **uvx命令找不到**
   ```bash
   # 安装uv
   pip install uv
   ```

2. **API密钥错误**
   ```bash
   # 检查环境变量
   echo $SILI_FLOW_API_KEY
   echo $DEEPSEEK_API_KEY
   
   ```

3. **代理连接失败**
   ```bash
   # 测试代理
   curl --proxy http://127.0.0.1:7897 https://www.google.com
   
   # 更新代理配置
   echo 'export YOUTUBE_PROXY="http://127.0.0.1:7897"' >> ~/.video-downloader/env
   source /etc/profile.d/video-downloader-en.sh
   ```

## 更新和维护

### 更新工具
```bash
# 更新uv工具
uv self update

# 更新video-downloader
uv tool upgrade video-downloader
```

### 卸载
```bash
# 卸载video-downloader
uv tool uninstall video-downloader

## 许可证

MIT License

## 支持与反馈

如有问题或建议，请通过OpenClaw项目渠道反馈。

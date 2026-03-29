# 视频下载器测试指南

本文档介绍如何测试视频下载器项目。

## 测试文件说明

### 1. 主要测试文件

- **`test_video_downloader.py`** - 完整的测试套件，包含单元测试和集成测试
- **`quick_test.py`** - 快速测试脚本，验证基本功能
- **`test_config.py`** - 测试配置文件，管理测试参数和环境
- **`run_tests.bat`** - Windows批处理脚本，一键运行测试
- **`TESTING.md`** - 本文档

### 2. 测试覆盖范围

测试覆盖以下模块：

- **下载代理** (`agents/download_agent.py`)
  - 视频信息获取
  - 视频下载功能
  - 平台识别

- **提取代理** (`agents/extract_agent.py`)
  - API密钥管理
  - 文案提取功能
  - 错误处理

- **分段代理** (`agents/segment_agent.py`)
  - 语义分段功能
  - 文本处理

- **主模块** (`main.py`)
  - 命令行参数解析
  - 完整处理流程
  - 文件保存功能

## 运行测试

### 方法1：使用批处理脚本（推荐）

```bash
# Windows
run_tests.bat

# 然后选择测试类型：
# 1. 快速测试 - 基本功能验证
# 2. 单元测试 - 详细测试（使用mock）
# 3. 集成测试 - 需要网络和API密钥
# 4. 所有测试 - 运行全部测试
# 5. 清理测试环境
```

### 方法2：直接运行Python脚本

```bash
# 快速测试
python quick_test.py

# 单元测试
python -m pytest test_video_downloader.py::TestVideoDownloader -v

# 集成测试（需要网络）
python -m pytest test_video_downloader.py::TestIntegration -v -m integration

# 所有测试
python -m pytest test_video_downloader.py -v
```

### 方法3：使用pytest直接运行

```bash
# 运行所有测试
pytest test_video_downloader.py -v

# 运行特定测试类
pytest test_video_downloader.py::TestVideoDownloader -v

# 运行特定测试方法
pytest test_video_downloader.py::TestVideoDownloader::test_download_agent_init -v

# 生成测试报告
pytest test_video_downloader.py -v --html=report.html
```

## 测试环境配置

### 1. 环境变量

某些测试需要API密钥，可以通过环境变量设置：

```bash
# Windows
set SILI_FLOW_API_KEY=your_sili_flow_key
set DEEPSEEK_API_KEY=your_deepseek_key

# 或者创建 .env 文件
SILI_FLOW_API_KEY=your_sili_flow_key
DEEPSEEK_API_KEY=your_deepseek_key
```

### 2. 跳过特定测试

```bash
# 跳过网络测试
set SKIP_NETWORK_TESTS=true

# 跳过API测试
set SKIP_API_TESTS=true

# 运行集成测试
set RUN_INTEGRATION_TESTS=true
```

## 测试类型说明

### 1. 单元测试

使用mock对象模拟外部依赖，不依赖网络或API：

- ✅ 测试初始化
- ✅ 测试方法调用
- ✅ 测试错误处理
- ✅ 测试数据验证

### 2. 集成测试

需要实际网络连接和API密钥：

- 🌐 测试实际视频下载
- 🔑 测试API调用
- 📁 测试文件系统操作
- 🔗 测试端到端流程

### 3. 快速测试

轻量级测试，快速验证基本功能：

- ⚡ 快速反馈
- 🔍 基本功能验证
- 📋 环境检查
- 🛠️ 问题诊断

## 测试用例说明

### 下载代理测试

```python
# 测试初始化
test_download_agent_init()

# 测试获取视频信息
test_download_agent_get_video_info()

# 测试视频下载
test_download_agent_download_video()
```

### 提取代理测试

```python
# 测试API密钥管理
test_extract_agent_init()

# 测试文案提取
test_extract_agent_extract_text()

# 测试错误处理
test_extract_agent_error_handling()
```

### 分段代理测试

```python
# 测试分段功能
test_segment_agent_segment()

# 测试长文本处理
test_segment_agent_long_text()

# 测试空文本处理
test_segment_agent_empty_text()
```

### 主模块测试

```python
# 测试命令行解析
test_main_command_line()

# 测试完整流程
test_video_processor_process_full()

# 测试文件保存
test_save_transcript()
```

## 常见问题

### 1. 测试失败：网络连接问题

```bash
# 设置跳过网络测试
set SKIP_NETWORK_TESTS=true
```

### 2. 测试失败：API密钥无效

```bash
# 设置跳过API测试
set SKIP_API_TESTS=true

# 或设置有效的API密钥
set SILI_FLOW_API_KEY=valid_key
set DEEPSEEK_API_KEY=valid_key
```

### 3. 测试失败：依赖缺失

```bash
# 安装测试依赖
pip install pytest pytest-asyncio aiohttp

# 安装项目依赖
pip install -e .
```

### 4. 测试失败：权限问题

```bash
# 确保有文件读写权限
# 检查输出目录是否可写
```

## 测试最佳实践

### 1. 本地开发

```bash
# 1. 运行快速测试验证基本功能
python quick_test.py

# 2. 修改代码后运行相关单元测试
pytest test_video_downloader.py::TestVideoDownloader -v

# 3. 提交前运行所有测试
run_tests.bat
```

### 2. 持续集成

```bash
# 安装依赖
pip install -r requirements.txt
pip install pytest pytest-asyncio

# 运行测试
pytest test_video_downloader.py -v

# 生成测试报告
pytest test_video_downloader.py --junitxml=test-results.xml
```

### 3. 测试覆盖率

```bash
# 安装覆盖率工具
pip install pytest-cov

# 运行测试并计算覆盖率
pytest test_video_downloader.py --cov=. --cov-report=html

# 查看覆盖率报告
open htmlcov/index.html
```

## 扩展测试

### 添加新测试

1. 在 `test_video_downloader.py` 中添加新的测试方法
2. 使用 `@pytest.mark.asyncio` 装饰异步测试
3. 使用 `@pytest.mark.integration` 标记集成测试
4. 使用mock对象模拟外部依赖

### 测试数据管理

1. 在 `test_config.py` 中添加测试数据
2. 使用 `TestConfig` 类管理测试参数
3. 使用 `setup_test_environment()` 设置测试环境
4. 使用 `cleanup_test_environment()` 清理测试环境

## 故障排除

### 查看详细错误信息

```bash
# 显示详细错误跟踪
pytest test_video_downloader.py -v --tb=long

# 显示所有输出
pytest test_video_downloader.py -v -s
```

### 调试测试

```python
# 在测试中添加调试输出
import logging
logging.basicConfig(level=logging.DEBUG)

# 使用pdb调试
import pdb; pdb.set_trace()
```

### 检查测试环境

```bash
# 检查Python版本
python --version

# 检查依赖
pip list | findstr pytest

# 检查环境变量
echo %SILI_FLOW_API_KEY%
```

## 联系方式

如有测试相关问题，请参考项目文档或联系开发者。
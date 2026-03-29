"""文件处理工具"""

import json
from pathlib import Path
from datetime import datetime
from typing import Any, Dict


def save_markdown(content: str, output_path: Path, metadata: Dict[str, Any] = None) -> Path:
    """保存为Markdown文件"""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if metadata:
        # 添加元数据头部
        header = f"""# {metadata.get("title", "文案内容")}
        | 属性 | 值 |
        |------|-----|
        | 视频ID | `{metadata.get("video_id", "")}` |
        | 平台 | {metadata.get("platform", "")} |
        | 作者 | {metadata.get("author", "")} |
        | 提取时间 | {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} |
        | 下载链接 | [点击下载]({metadata.get("video_url", "")}) |
        
        ---
        
        """
        content = header + content

    output_path.write_text(content, encoding="utf-8")
    return output_path


def save_json(data: Any, output_path: Path) -> Path:
    """保存为JSON文件"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return output_path

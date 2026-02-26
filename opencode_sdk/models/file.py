"""文件数据模型。"""

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field

from .common import Range


# ============================================================================
# 文件模型
# ============================================================================


class FileNode(BaseModel):
    """文件或目录节点。"""

    name: str = Field(..., description="文件或目录名称")
    path: str = Field(..., description="相对路径")
    absolute: str = Field(..., description="绝对路径")
    type: Literal["file", "directory"] = Field(..., description="节点类型")
    ignored: bool = Field(..., description="是否被 .gitignore 忽略")


class FilePatchHunk(BaseModel):
    """文件补丁块。"""

    old_start: int = Field(..., alias="oldStart", description="旧文件起始行")
    old_lines: int = Field(..., alias="oldLines", description="旧文件行数")
    new_start: int = Field(..., alias="newStart", description="新文件起始行")
    new_lines: int = Field(..., alias="newLines", description="新文件行数")
    lines: List[str] = Field(..., description="补丁行")

    class Config:
        populate_by_name = True


class FilePatch(BaseModel):
    """文件补丁信息。"""

    old_file_name: str = Field(..., alias="oldFileName", description="旧文件名")
    new_file_name: str = Field(..., alias="newFileName", description="新文件名")
    old_header: Optional[str] = Field(None, alias="oldHeader", description="旧文件头")
    new_header: Optional[str] = Field(None, alias="newHeader", description="新文件头")
    hunks: List[FilePatchHunk] = Field(..., description="补丁块列表")
    index: Optional[str] = Field(None, description="索引")

    class Config:
        populate_by_name = True


class FileContent(BaseModel):
    """文件内容。"""

    type: Literal["text"] = "text"
    content: str = Field(..., description="文件内容")
    diff: Optional[str] = Field(None, description="差异内容")
    patch: Optional[FilePatch] = Field(None, description="补丁信息")
    encoding: Optional[Literal["base64"]] = Field(None, description="内容编码")
    mime_type: Optional[str] = Field(None, alias="mimeType", description="MIME 类型")

    class Config:
        populate_by_name = True


class File(BaseModel):
    """文件变更信息。"""

    path: str = Field(..., description="文件路径")
    added: int = Field(..., description="新增行数")
    removed: int = Field(..., description="删除行数")
    status: Literal["added", "deleted", "modified"] = Field(..., description="文件状态")


# ============================================================================
# 符号模型
# ============================================================================


class Symbol(BaseModel):
    """代码符号。"""

    name: str = Field(..., description="符号名称")
    kind: int = Field(..., description="符号类型")
    location: Dict[str, Any] = Field(..., description="符号位置（uri、range）")

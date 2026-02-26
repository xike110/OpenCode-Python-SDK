"""OpenCode SDK 的工具函数。"""

from typing import Any, Dict, Optional


def remove_none_values(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    从字典中移除 None 值。

    Args:
        data: 要清理的字典

    Returns:
        不包含 None 值的字典
    """
    return {k: v for k, v in data.items() if v is not None}


def merge_dicts(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    """
    合并多个字典。

    Args:
        *dicts: 要合并的字典

    Returns:
        合并后的字典
    """
    result: Dict[str, Any] = {}
    for d in dicts:
        if d:
            result.update(d)
    return result

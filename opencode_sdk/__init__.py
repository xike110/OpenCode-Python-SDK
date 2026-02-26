"""
OpenCode Python SDK

OpenCode AI CLI 的 Python 客户端库。
"""

from .client import OpencodeClient, create_opencode_client
from .exceptions import (
    APIError,
    BadRequestError,
    MessageAbortedError,
    NotFoundError,
    OpencodeException,
    ProviderAuthError,
    UnknownError,
)
from .version import __version__

__all__ = [
    # 客户端
    "OpencodeClient",
    "create_opencode_client",
    # 异常
    "OpencodeException",
    "ProviderAuthError",
    "APIError",
    "NotFoundError",
    "BadRequestError",
    "MessageAbortedError",
    "UnknownError",
    # 版本
    "__version__",
]

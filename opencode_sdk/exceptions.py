"""OpenCode SDK 的异常类。"""

from typing import Any, Dict, Optional


class OpencodeException(Exception):
    """所有 OpenCode SDK 错误的基础异常类。"""

    def __init__(self, message: str, data: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.message = message
        self.data = data or {}


class ProviderAuthError(OpencodeException):
    """提供商认证错误。"""

    def __init__(self, provider_id: str, message: str) -> None:
        super().__init__(
            f"提供商 '{provider_id}' 认证失败: {message}",
            {"providerID": provider_id, "message": message},
        )
        self.provider_id = provider_id


class UnknownError(OpencodeException):
    """未知错误。"""

    pass


class MessageOutputLengthError(OpencodeException):
    """消息输出长度超限。"""

    pass


class MessageAbortedError(OpencodeException):
    """消息被中止。"""

    pass


class APIError(OpencodeException):
    """API 请求错误。"""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        is_retryable: bool = False,
        response_headers: Optional[Dict[str, str]] = None,
        response_body: Optional[str] = None,
    ) -> None:
        super().__init__(
            message,
            {
                "message": message,
                "statusCode": status_code,
                "isRetryable": is_retryable,
                "responseHeaders": response_headers,
                "responseBody": response_body,
            },
        )
        self.status_code = status_code
        self.is_retryable = is_retryable
        self.response_headers = response_headers or {}
        self.response_body = response_body


class NotFoundError(OpencodeException):
    """资源未找到错误。"""

    def __init__(self, message: str = "资源未找到") -> None:
        super().__init__(message, {"message": message})


class BadRequestError(OpencodeException):
    """错误的请求。"""

    def __init__(self, message: str, errors: Optional[list] = None) -> None:
        super().__init__(
            message,
            {
                "success": False,
                "errors": errors or [],
            },
        )
        self.errors = errors or []


class TimeoutError(OpencodeException):
    """请求超时错误。"""

    pass


class ConnectionError(OpencodeException):
    """连接错误。"""

    pass

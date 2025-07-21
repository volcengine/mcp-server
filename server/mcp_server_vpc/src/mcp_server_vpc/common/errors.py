from mcp_server_vpc.common.logs import logger


class VPCError(Exception):
    """VPC操作错误"""

    def __init__(self, message: str, exc: Exception = None):
        """
        初始化VPC错误

        Args:
            message: 错误信息
            exc: 原始异常
        """
        if exc:
            message = f"{message}: {exc}"
        super().__init__(message)
        self.__cause__ = exc
        logger.error(message)

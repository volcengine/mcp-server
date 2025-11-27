# coding:utf-8
from .base_trait import BaseTrait


class BaseService(BaseTrait):
    def __init__(
        self,
        region="",
        ak=None,
        sk=None,
        session_token=None,
    ):
        super().__init__(
            {"ak": ak, "sk": sk, "region": region, "session_token": session_token}
        )

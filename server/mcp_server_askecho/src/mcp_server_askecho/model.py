from dataclasses import dataclass
from typing import Optional


@dataclass
class Error:
    message: str
    type: str
    code: str

    def to_dict(self):
        return {
            "message": self.message,
            "type": self.type,
            "code": self.code
        }


@dataclass
class ResponseError:
    error: Error

    def to_dict(self):
        return {
            "error": self.error.to_dict(),
        }


@dataclass
class Message:
    role: str
    content: str

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            role=d.get("role", ""),
            content=d.get("content", "")
        )


@dataclass
class OriginChatCompletionRequest:
    bot_id: str
    stream: bool
    messages: list[Message]
    user_id: Optional[str] = ""

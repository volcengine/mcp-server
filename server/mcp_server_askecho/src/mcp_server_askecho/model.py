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
class CoverImage:
    url: str
    width: int
    height: int

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            url=d.get("url", ""),
            width=d.get("width", 0),
            height=d.get("height", 0),
        )

    def to_dict(self):
        return {
            "url": self.url,
            "width": self.width,
            "height": self.height,
        }


@dataclass
class Reference:
    id: str
    source_type: str
    site_name: str
    title: str
    publish_time: int
    url: str
    cover_image: CoverImage

    @classmethod
    def from_dict(cls, d: dict):
        cover_image = CoverImage.from_dict(d) if d.get("cover_image") else None
        return cls(
            id=d.get("id", ""),
            source_type=d.get("source_type", ""),
            site_name=d.get("site_name", ""),
            title=d.get("title", ""),
            publish_time=d.get("publish_time", 0),
            url=d.get("url", ""),
            cover_image=cover_image,
        )

    def to_dict(self):
        return {
            "id": self.id,
            "source_type": self.source_type,
            "site_name": self.site_name,
            "title": self.title,
            "publish_time": self.publish_time,
            "url": self.url,
            "cover_image": self.cover_image.to_dict() if self.cover_image else None,
        }


@dataclass
class ChatCompletionToolResponse:
    log_id: str
    content: str
    references: list[Reference]

    def to_dict(self):
        return {
            "log_id": self.log_id,
            "content": self.content,
            "references": [r.to_dict() for r in self.references],
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

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            bot_id=d.get("bot_id", ""),
            stream=d.get("stream", False),
            messages=[Message.from_dict(m) for m in d.get("messages", [])],
            user_id=d.get("user_id", "")
        )


@dataclass
class Choice:
    message: Message

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            message=Message.from_dict(d.get("message", {})),
        )


@dataclass
class OriginChatCompletionResponse:
    id: str
    choices: list[Choice]
    references: list[Reference]

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            id=d.get("id", ""),
            choices=[Choice.from_dict(c) for c in d.get("choices", [])],
            references=[Reference.from_dict(r) for r in d.get("references", [])],
        )

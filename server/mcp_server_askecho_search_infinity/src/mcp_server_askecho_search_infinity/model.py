from dataclasses import dataclass
from typing import Optional, List


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
class WebSearchRequest:
    Query: str
    SearchType: str = "web"
    Count: int = 10
    Filter: Optional[dict] = None
    NeedSummary: bool = True
    TimeRange: str = ""

    def __post_init__(self):
        if self.Filter is None:
            self.Filter = {
                "NeedContent": True,
                "NeedUrl": True,
                "Sites": ""
            }


@dataclass
class SearchResult:
    Id: str
    SortId: int
    Title: str
    Snippet: str
    SiteName: Optional[str] = None
    Url: Optional[str] = None
    Summary: Optional[str] = None
    Content: Optional[str] = None
    PublishTime: Optional[str] = None
    LogoUrl: Optional[str] = None
    RankScore: Optional[float] = None


@dataclass
class WebSearchResponse:
    results: List[SearchResult]
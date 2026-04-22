import datetime
import re
from dataclasses import dataclass
from typing import Optional, List

TIME_RANGE_SHORTCUTS = {"OneDay", "OneWeek", "OneMonth", "OneYear"}
DATE_RANGE_PATTERN = re.compile(r"^(\d{4}-\d{2}-\d{2})\.\.(\d{4}-\d{2}-\d{2})$")
SUPPORTED_SEARCH_TYPES = {"web", "image"}


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
    NeedSummary: Optional[bool] = None
    TimeRange: Optional[str] = None

    def to_payload(self):
        payload = {
            "Query": self.Query,
            "SearchType": self.SearchType,
            "Count": self.Count,
        }
        if self.SearchType == "web":
            payload["NeedSummary"] = True
            if self.Filter:
                payload["Filter"] = self.Filter
            if self.TimeRange:
                payload["TimeRange"] = self.TimeRange
        return payload


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


def validate_time_range(time_range: Optional[str]) -> Optional[str]:
    if not time_range:
        return None
    if time_range in TIME_RANGE_SHORTCUTS:
        return time_range

    match = DATE_RANGE_PATTERN.match(time_range)
    if not match:
        raise ValueError(
            "TimeRange 需为 OneDay/OneWeek/OneMonth/OneYear，或日期区间 YYYY-MM-DD..YYYY-MM-DD。"
        )

    start_text, end_text = match.groups()
    try:
        start_date = datetime.date.fromisoformat(start_text)
        end_date = datetime.date.fromisoformat(end_text)
    except ValueError as exc:
        raise ValueError("TimeRange 中的日期需为有效的 YYYY-MM-DD。") from exc

    if start_date > end_date:
        raise ValueError("TimeRange 的开始日期不能晚于结束日期。")

    return time_range


def build_web_search_request(
        query: str,
        count: int = 10,
        search_type: str = "web",
        time_range: Optional[str] = None,
        auth_level: int = 0,
) -> WebSearchRequest:
    normalized_query = (query or "").strip()
    if not normalized_query:
        raise ValueError("Query 不能为空。")
    if len(normalized_query) > 100:
        raise ValueError("Query 长度需为 1~100 个字符。")

    if search_type not in SUPPORTED_SEARCH_TYPES:
        raise ValueError("SearchType 仅支持 web 或 image。")

    if count < 1:
        raise ValueError("Count 需大于等于 1。")
    max_count = 50 if search_type == "web" else 5
    if count > max_count:
        raise ValueError(f"{search_type} 类型最多返回 {max_count} 条。")

    if auth_level not in {0, 1}:
        raise ValueError("AuthLevel 仅支持 0 或 1。")

    normalized_time_range = validate_time_range(time_range) if search_type == "web" else None
    filters = {"AuthInfoLevel": auth_level} if search_type == "web" and auth_level > 0 else None

    return WebSearchRequest(
        Query=normalized_query,
        SearchType=search_type,
        Count=count,
        Filter=filters,
        NeedSummary=True if search_type == "web" else None,
        TimeRange=normalized_time_range,
    )

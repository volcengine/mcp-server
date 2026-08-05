import datetime
import re
from dataclasses import dataclass
from typing import Optional, List

TIME_RANGE_SHORTCUTS = {"OneDay", "OneWeek", "OneMonth", "OneYear"}
DATE_RANGE_PATTERN = re.compile(r"^(\d{4}-\d{2}-\d{2})\.\.(\d{4}-\d{2}-\d{2})$")
SUPPORTED_SEARCH_TYPES = {"web", "image"}
SUPPORTED_INDUSTRIES = {"finance", "game", "gov"}
SUPPORTED_CONTENT_FORMATS = {"text", "markdown"}
MAX_SITE_COUNT = 20
MAX_BLOCK_HOST_COUNT = 5


@dataclass
class WebSearchRequest:
    Query: str
    SearchType: str = "web"
    Count: int = 10
    Filter: Optional[dict] = None
    TimeRange: Optional[str] = None
    QueryControl: Optional[dict] = None
    ContentFormats: Optional[str] = None

    def to_payload(self):
        payload = {
            "Query": self.Query,
            "SearchType": self.SearchType,
            "Count": self.Count,
        }
        if self.Filter:
            payload["Filter"] = self.Filter
        if self.TimeRange:
            payload["TimeRange"] = self.TimeRange
        if self.QueryControl:
            payload["QueryControl"] = self.QueryControl
        if self.ContentFormats:
            payload["ContentFormats"] = self.ContentFormats
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


def validate_host_list(value: Optional[str], field_name: str, max_count: int) -> Optional[str]:
    if value is None:
        return None

    normalized_value = value.strip()
    if not normalized_value:
        return None

    items = [item.strip() for item in normalized_value.split("|")]
    if not items or any(not item for item in items):
        raise ValueError(f"{field_name} 需为以 | 分隔的非空域名列表。")
    if len(items) > max_count:
        raise ValueError(f"{field_name} 最多支持 {max_count} 个域名。")
    return "|".join(items)


def build_web_search_request(
        query: str,
        count: Optional[int] = None,
        search_type: str = "web",
        time_range: Optional[str] = None,
        auth_level: int = 0,
        need_content: Optional[bool] = None,
        need_url: Optional[bool] = None,
        sites: Optional[str] = None,
        block_hosts: Optional[str] = None,
        industry: Optional[str] = None,
        query_rewrite: Optional[bool] = None,
        content_formats: Optional[str] = None,
) -> WebSearchRequest:
    normalized_query = (query or "").strip()
    if not normalized_query:
        raise ValueError("Query 不能为空。")
    if len(normalized_query) > 100:
        raise ValueError("Query 长度需为 1~100 个字符。")

    normalized_search_type = (search_type or "").strip().lower()
    if normalized_search_type not in SUPPORTED_SEARCH_TYPES:
        raise ValueError("SearchType 仅支持 web 或 image。")

    if count is None:
        count = 10 if normalized_search_type == "web" else 5
    if count < 1:
        raise ValueError("Count 需大于等于 1。")
    max_count = 50 if normalized_search_type == "web" else 5
    if count > max_count:
        raise ValueError(f"{normalized_search_type} 类型最多返回 {max_count} 条。")

    if auth_level not in {0, 1}:
        raise ValueError("AuthLevel 仅支持 0 或 1。")

    normalized_industry = industry.strip().lower() if industry else None
    if normalized_industry and normalized_industry not in SUPPORTED_INDUSTRIES:
        raise ValueError("Industry 仅支持 finance、game 或 gov。")

    normalized_content_formats = content_formats.strip().lower() if content_formats else None
    if normalized_content_formats and normalized_content_formats not in SUPPORTED_CONTENT_FORMATS:
        raise ValueError("ContentFormats 仅支持 text 或 markdown。")

    if normalized_search_type == "image":
        web_only_args = {
            "TimeRange": time_range,
            "AuthLevel": auth_level if auth_level else None,
            "NeedContent": need_content,
            "NeedUrl": need_url,
            "Sites": sites,
            "BlockHosts": block_hosts,
            "Industry": normalized_industry,
            "ContentFormats": normalized_content_formats,
        }
        unsupported_fields = [name for name, value in web_only_args.items() if value is not None]
        if unsupported_fields:
            raise ValueError(f"{', '.join(unsupported_fields)} 仅支持 web 搜索。")
        return WebSearchRequest(
            Query=normalized_query,
            SearchType=normalized_search_type,
            Count=count,
            QueryControl={"QueryRewrite": query_rewrite} if query_rewrite is not None else None,
        )

    filters = {}
    if auth_level > 0:
        filters["AuthInfoLevel"] = auth_level
    if need_content is not None:
        filters["NeedContent"] = need_content
    if need_url is not None:
        filters["NeedUrl"] = need_url

    normalized_sites = validate_host_list(sites, "Sites", MAX_SITE_COUNT)
    if normalized_sites:
        filters["Sites"] = normalized_sites
    normalized_block_hosts = validate_host_list(block_hosts, "BlockHosts", MAX_BLOCK_HOST_COUNT)
    if normalized_block_hosts:
        filters["BlockHosts"] = normalized_block_hosts
    if normalized_industry:
        filters["Industry"] = normalized_industry

    return WebSearchRequest(
        Query=normalized_query,
        SearchType=normalized_search_type,
        Count=count,
        Filter=filters or None,
        TimeRange=validate_time_range(time_range),
        QueryControl={"QueryRewrite": query_rewrite} if query_rewrite is not None else None,
        ContentFormats=normalized_content_formats,
    )

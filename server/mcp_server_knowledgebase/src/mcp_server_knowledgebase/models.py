"""MCP response fields and small upstream value conversions."""
import json
from typing import Annotated, Literal, Optional, Union

from pydantic import BaseModel, Field, JsonValue, StringConstraints, field_validator
from pydantic.json_schema import SkipJsonSchema

NonBlank = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
Timestamp = Union[int, float, str]


class DocFilter(BaseModel):
    op: Literal["must", "must_not"] = Field(description='Use must to include matches or must_not to exclude them.')
    field: NonBlank = Field(description='Document field to filter, such as doc_id.')
    conds: list[JsonValue] = Field(min_length=1, description='Non-empty list of JSON values to match.')


class AddDocumentResult(BaseModel):
    collection_name: str = Field(description='Knowledge base collection name.')
    doc_id: str = Field(description='Document ID; can be used with get_doc.')
    resource_id: Optional[str] = Field(default=None, description='Knowledge base resource ID.')


class DocumentStatus(BaseModel):
    process_status: Optional[int] = Field(default=None, description='Processing status: 0 completed, 1 failed, 2 or 3 queued, 5 deleting, 6 processing.')
    failed_code: Optional[Union[int, str]] = Field(default=None, description='Failure code returned by Viking, when available.')


class MediaChapter(BaseModel):
    title: Optional[str] = Field(default=None, description='Chapter title.')
    content: Optional[str] = Field(default=None, description='Content text.')
    start_time: Optional[Timestamp] = Field(default=None, description='Chapter start time in the format and units returned by Viking.')
    end_time: Optional[Timestamp] = Field(default=None, description='Chapter end time in the format and units returned by Viking.')
    element_content: JsonValue = Field(default=None, description='Structured chapter content returned by Viking.')


class MediaOutline(BaseModel):
    title: Optional[str] = Field(default=None, description='Media outline title.')
    summary: Optional[str] = Field(default=None, description='Media outline summary.')
    chapters: Optional[list[MediaChapter]] = Field(default=None, description='Media chapters.')


class DocumentSummary(BaseModel):
    doc_id: Optional[str] = Field(default=None, description='Document ID; can be used with get_doc.')
    doc_name: Optional[str] = Field(default=None, description='Document name.')
    title: Optional[str] = Field(default=None, description='Document title.')
    doc_type: Optional[str] = Field(default=None, description='Document format, such as pdf or markdown.')
    status: Optional[DocumentStatus] = Field(default=None, description='Document processing status.')
    point_num: Optional[int] = Field(default=None, description='Number of document chunks.')
    brief_summary: Optional[str] = Field(default=None, description='Brief document summary.')
    create_time: Optional[int] = Field(default=None, description='Creation timestamp returned by Viking.')
    update_time: Optional[int] = Field(default=None, description='Last update timestamp returned by Viking.')


class DocumentInfo(DocumentSummary):
    collection_name: Optional[str] = Field(default=None, description='Knowledge base collection name.')
    add_type: Optional[str] = Field(default=None, description='Document import method, such as url.')
    doc_summary: Optional[str] = Field(default=None, description='Document summary.')
    meta: JsonValue = Field(default=None, description='Document metadata; valid JSON strings are parsed into JSON values.')
    video_outline: Optional[MediaOutline] = Field(default=None, description='Video outline and chapters, when available.')
    audio_outline: Optional[MediaOutline] = Field(default=None, description='Audio outline and chapters, when available.')

    @field_validator("meta", mode="before")
    @classmethod
    def parse_meta(cls, value):
        if isinstance(value, str):
            try:
                return json.loads(value)
            except (ValueError, RecursionError):
                pass
        return value


class ListDocumentsResult(BaseModel):
    collection_name: str = Field(description='Knowledge base collection name.')
    total_num: Optional[int] = Field(default=None, description='Total number of documents reported by Viking; null if unavailable.')
    count: int = Field(description='Number of documents in this page.')
    doc_list: list[DocumentSummary] = Field(description='Document summaries in this page.')
    has_more: bool = Field(description='Whether more documents are available.')
    next_token: Optional[str] = Field(default=None, description='Cursor for the next page; pass to list_docs. Empty or null at the end.')


class CollectionSummary(BaseModel):
    collection_name: str = Field(description='Knowledge base collection name.')
    description: str = Field(description='Collection description.')
    resource_id: Optional[str] = Field(default=None, description='Knowledge base resource ID.')
    create_time: Optional[int] = Field(default=None, description='Creation timestamp returned by Viking.')
    update_time: Optional[int] = Field(default=None, description='Last update timestamp returned by Viking.')


class CollectionInfoResult(CollectionSummary):
    status: int = Field(description='First index build status: -1 pending, 0 building, 1 completed, 2 failed, 3 changing.')
    doc_num: Optional[int] = Field(default=None, description='Number of documents in the collection.')


class ListCollectionsResult(BaseModel):
    collection_list: list[CollectionSummary] = Field(description='Collections in the configured project.')
    total_num: Optional[int] = Field(default=None, description='Total number of collections reported by Viking; null if unavailable.')


class ChunkAttachment(BaseModel):
    uuid: Optional[str] = Field(default=None, description='Attachment identifier.')
    caption: Optional[str] = Field(default=None, description='Attachment caption.')
    type: Optional[str] = Field(default=None, description='Attachment type; image, doc-image and table represent images.')
    # Internal input for ResourceLink blocks only; never part of JSON output/schema.
    link: SkipJsonSchema[Optional[str]] = Field(default=None, exclude=True)


class SearchChunk(BaseModel):
    id: str = Field(description='Chunk identifier.')
    content: str = Field(description='Content text.')
    doc_id: Optional[str] = Field(description='Document ID; can be used with get_doc.')
    doc_name: Optional[str] = Field(description='Document name.')
    title: Optional[str] = Field(default=None, description='Document title.')
    doc_type: Optional[str] = Field(default=None, description='Document format, such as pdf or markdown.')
    score: Optional[float] = Field(default=None, description='Retrieval score returned by Viking.')
    rerank_score: Optional[float] = Field(default=None, description='Reranking score, when available.')
    chunk_title: Optional[str] = Field(default=None, description='Chunk title.')
    audio_start_time: Optional[Timestamp] = Field(default=None, description='Audio start time in the format and units returned by Viking.')
    audio_end_time: Optional[Timestamp] = Field(default=None, description='Audio end time in the format and units returned by Viking.')
    video_start_time: Optional[Timestamp] = Field(default=None, description='Video start time in the format and units returned by Viking.')
    video_end_time: Optional[Timestamp] = Field(default=None, description='Video end time in the format and units returned by Viking.')
    chunk_attachment: Optional[list[ChunkAttachment]] = Field(default=None, description='Attachment metadata (uuid, caption, type). Image URLs are returned separately as MCP ResourceLink blocks, not as link fields here.')


class SearchKnowledgeResult(BaseModel):
    result_list: list[SearchChunk] = Field(description='Matching knowledge chunks.')

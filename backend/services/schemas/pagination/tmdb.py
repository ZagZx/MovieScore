from typing import TypeVar, Generic
from pydantic import BaseModel, Field

T = TypeVar("T")


class TmdbPaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=20, gt=0, le=20)

class TmdbPagination(BaseModel):
    page: int
    total_pages: int
    total_results: int
    has_more: bool

class TmdbPage(BaseModel, Generic[T]):
    data: list[T]
    pagination: TmdbPagination
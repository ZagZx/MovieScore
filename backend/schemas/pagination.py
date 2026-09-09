from typing import TypeVar, Generic, Optional
from pydantic import BaseModel, Field

T = TypeVar("T")


class CursorParams(BaseModel):
    limit: int = Field(default=20, gt=0, le=20)
    cursor: Optional[int] = 0

class CursorPagination(BaseModel):
    cursor: Optional[int] = None
    has_more: bool = False

class CursorPage(BaseModel, Generic[T]):
    data: list[T]
    pagination: CursorPagination


class TmdbParams(BaseModel):
    page: int = 1
    limit: int = Field(default=20, gt=0, le=20)

class TmdbPagination(BaseModel):
    page: int
    total_pages: int
    total_results: int

class TmdbPage(BaseModel, Generic[T]):
    data: list[T]
    pagination: TmdbPagination
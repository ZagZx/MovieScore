from typing import TypeVar, Generic
from pydantic import BaseModel, Field

T = TypeVar("T")


class KitsuPaginationParams(BaseModel):
    limit: int = Field(default=20, gt=0, le=20)
    offset: int = Field(default=0, ge=0)

    def to_kitsu_query_params(self):
        return {
            "page[limit]": self.limit,
            "page[offset]": self.offset
        }

class KitsuPagination(BaseModel):
    limit: int
    offset: int
    total_results: int
    has_more: bool

class KitsuPage(BaseModel, Generic[T]):
    data: list[T]
    pagination: KitsuPagination
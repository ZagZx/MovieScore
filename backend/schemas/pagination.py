from typing import TypeVar, Generic, Optional
from pydantic import BaseModel


T = TypeVar("T")

class CursorParams(BaseModel):
    limit: int = 20
    cursor: Optional[int] = 0


class CursorPaging(BaseModel):
    cursor: Optional[int] = None
    has_more: bool = False

class CursorPage(BaseModel, Generic[T]):
    data: list[T]
    paging: CursorPaging
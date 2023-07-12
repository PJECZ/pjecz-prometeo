"""
FastAPI Pagination Custom Page
"""
from typing import Any, Generic, Optional, Sequence, TypeVar

from fastapi import Query
from pydantic import BaseModel
from typing_extensions import Self

from fastapi_pagination.bases import AbstractPage, AbstractParams, RawParams
from fastapi_pagination.limit_offset import LimitOffsetPage


class CustomLimitOffsetPage(LimitOffsetPage):
    """Create pagination params"""

    limit: int = Query(10, ge=1, le=10)
    offset: int = Query(0, ge=0)

    def to_raw_params(self) -> RawParams:
        """Convert to raw params"""
        return RawParams(limit=self.limit, offset=self.offset)


T = TypeVar("T")


class CustomPageResult(BaseModel, Generic[T]):
    """Custom page result"""

    items: Sequence[T]
    limit: int
    offset: int
    total: int


class CustomPage(AbstractPage[T], Generic[T]):
    """Custom page"""

    message: str
    result: CustomPageResult[T]
    success: bool

    __params_type__ = CustomLimitOffsetPage

    @classmethod
    def create(
        cls,
        items: Sequence[T],
        total: int,
        params: AbstractParams,
    ) -> Self:
        """Create custom page"""
        assert isinstance(params, CustomLimitOffsetPage)
        assert total is not None
        return cls(
            message="Success",
            result=CustomPageResult(
                items=items,
                limit=params.limit,
                offset=params.offset,
                total=total,
            ),
            success=True,
        )

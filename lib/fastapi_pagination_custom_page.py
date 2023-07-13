"""
FastAPI Pagination Custom Page
"""
from typing import Any, Generic, Optional, Sequence, TypeVar

from fastapi import Query
from pydantic import BaseModel
from typing_extensions import Self

from fastapi_pagination.bases import AbstractPage, AbstractParams, BasePage, RawParams
from fastapi_pagination.limit_offset import LimitOffsetPage, LimitOffsetParams
from fastapi_pagination.types import GreaterEqualOne, GreaterEqualZero


class CustomPageParams(LimitOffsetParams):
    """
    Custom Page Params
    """

    offset: Optional[int] = Query(0, ge=0, description="Page offset")
    limit: Optional[int] = Query(10, ge=1, le=20, description="Page size limit")


class CustomPageResult(BaseModel):
    """
    Custom Page Meta
    """

    total: int
    offset: int
    limit: int


T = TypeVar("T")


class CustomPage(BasePage[T], Generic[T]):
    """
    Custom Page
    """

    success: bool = True
    message: str = "Success"

    limit: Optional[GreaterEqualOne]
    offset: Optional[GreaterEqualZero]

    __params_type__ = CustomPageParams

    @classmethod
    def create(
        cls,
        items: Sequence[T],
        params: AbstractParams,
        *,
        total: Optional[int] = None,
        **kwargs: Any,
    ) -> LimitOffsetPage[T]:
        raw_params = params.to_raw_params().as_limit_offset()

        return cls(
            success=True,
            message="Success",
            total=total,
            items=items,
            limit=raw_params.limit,
            offset=raw_params.offset,
            **kwargs,
        )

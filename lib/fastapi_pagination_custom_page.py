"""
FastAPI Pagination Custom Page
"""
from typing import Any, Generic, List, Optional, Sequence, TypeVar

from fastapi import Query
from pydantic import BaseModel

from abc import ABC
from fastapi_pagination.bases import AbstractPage, AbstractParams, BasePage, RawParams
from fastapi_pagination.limit_offset import LimitOffsetPage, LimitOffsetParams
from fastapi_pagination.types import GreaterEqualOne, GreaterEqualZero


class CustomPageParams(LimitOffsetParams):
    """
    Custom Page Params
    """

    offset: Optional[int] = Query(0, ge=0, description="Page offset")
    limit: Optional[int] = Query(10, ge=1, le=20, description="Page size limit")


T = TypeVar("T")


class CustomPageResult(BaseModel):
    """
    Custom Page Result
    """

    total: Optional[GreaterEqualZero] = 0
    limit: Optional[GreaterEqualOne] = None
    offset: Optional[GreaterEqualZero] = None


class CustomPage(AbstractPage[T], Generic[T], ABC):
    """
    Custom Page
    """

    success: bool = True
    message: str = "Success"
    result: CustomPageResult

    data: Sequence[T]

    __params_type__ = CustomPageParams

    @classmethod
    def create(
        cls,
        items: Sequence[T],
        params: AbstractParams,
        total: Optional[int] = None,
        **kwargs: Any,
    ) -> LimitOffsetPage[T]:
        raw_params = params.to_raw_params().as_limit_offset()

        return cls(
            success=True,
            message="Success",
            result=CustomPageResult(
                total=total,
                offset=raw_params.offset,
                limit=raw_params.limit,
            ),
            data=items,
            **kwargs,
        )

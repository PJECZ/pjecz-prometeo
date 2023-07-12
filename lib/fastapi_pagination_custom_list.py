"""
FastAPI Pagination Custom List
"""
from typing import Any, Generic, List, Optional, Sequence, TypeVar

from fastapi import Query
from pydantic import BaseModel

from fastapi_pagination.bases import AbstractPage, AbstractParams, RawParams
from fastapi_pagination.default import Page, Params


class CustomParams(Params):
    """Custom params"""

    size: int = Query(200, ge=1, le=200)


T = TypeVar("T")


class CustomResult(BaseModel, Generic[T]):
    """Custom result"""

    items: Sequence[T]
    size: int
    total: int


class CustomList(AbstractPage[T], Generic[T]):
    """Custom list"""

    message: str
    result: CustomResult[T]
    success: bool

    __params_type__ = CustomParams

    @classmethod
    def create(
        cls,
        items: Sequence[T],
        params: AbstractParams,
        *,
        total: Optional[int] = None,
        **kwargs: Any,
    ):
        """Create custom list"""
        assert isinstance(params, CustomParams)
        assert total is not None
        return cls(
            message="Success",
            result=CustomResult(
                items=items,
                size=params.size,
                total=total,
            ),
            success=True,
            **kwargs,
        )

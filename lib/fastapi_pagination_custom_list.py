"""
FastAPI Pagination Custom List
"""
from math import ceil
from typing import Any, Generic, Optional, Sequence, TypeVar

from fastapi import Query
from fastapi_pagination.bases import AbstractPage, AbstractParams
from fastapi_pagination.default import Params
from fastapi_pagination.types import GreaterEqualOne, GreaterEqualZero
from typing_extensions import Self


class CustomListParams(Params):
    """
    Custom Page Params
    """

    page: int = Query(1, ge=1, description="Page number")
    size: int = Query(200, ge=1, le=400, description="Page size")


T = TypeVar("T")


class CustomList(AbstractPage[T], Generic[T]):
    """
    Custom Page
    """

    success: bool
    message: str

    total: Optional[GreaterEqualZero] = None
    items: Sequence[T] = []
    page: Optional[GreaterEqualOne] = None
    size: Optional[GreaterEqualOne] = None
    pages: Optional[GreaterEqualZero] = None

    __params_type__ = CustomListParams

    @classmethod
    def create(
        cls,
        items: Sequence[T],
        params: AbstractParams,
        total: Optional[int] = None,
        **kwargs: Any,
    ) -> Self:
        """
        Create Custom Page
        """
        if not isinstance(params, Params):
            raise TypeError("Page should be used with Params")

        if total is None or total < 0:
            return cls(
                success=False,
                message="No se encontraron registros",
            )

        size = params.size if params.size is not None else total
        page = params.page if params.page is not None else 1
        pages = ceil(total / size) if total is not None else None

        return cls(
            success=True,
            message="Success",
            total=total,
            items=items,
            page=page,
            size=size,
            pages=pages,
            **kwargs,
        )

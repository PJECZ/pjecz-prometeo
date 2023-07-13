"""
FastAPI Pagination Custom Page

Provides a custom pagination class to be used with FastAPI 0.100.0 and Pydantic 2.0.2

This is an example of the output JSON:

    {
      "success": true,
      "message": "Success",
      "total": 116135,
      "items": [
        { ... },
        { ... },
        ...
      ],
      "limit": 10,
      "offset": 0
    }

Usage:

    from typing import Annotated

    from fastapi import APIRouter, Depends
    from fastapi_pagination.ext.sqlalchemy import paginate

    from lib.fastapi_pagination_custom_page import CustomPage

    from .crud import get_examples
    from .schemas import ExampleOut

    examples = APIRouter(prefix="/examples")

    @examples.get("", response_model=CustomPage[ExampleOut])
    async def list_examples(
        db: Annotated[Session, Depends(get_db)],
    ):
        query = get_examples(db=db)
        return paginate(query)

"""
from typing import Any, Generic, Optional, Sequence, TypeVar
from abc import ABC

from fastapi import Query
from fastapi_pagination.bases import AbstractPage, AbstractParams
from fastapi_pagination.limit_offset import LimitOffsetParams
from fastapi_pagination.types import GreaterEqualOne, GreaterEqualZero
from typing_extensions import Self


class CustomPageParams(LimitOffsetParams):
    """
    Custom Page Params
    """

    offset: int = Query(0, ge=0, description="Page offset")
    limit: int = Query(10, ge=1, le=20, description="Page size limit")


T = TypeVar("T")


class CustomPage(AbstractPage[T], Generic[T], ABC):
    """
    Custom Page
    """

    success: bool
    message: str

    total: Optional[GreaterEqualZero] = None
    items: Sequence[T] = []
    limit: Optional[GreaterEqualOne] = None
    offset: Optional[GreaterEqualZero] = None

    __params_type__ = CustomPageParams

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
        raw_params = params.to_raw_params().as_limit_offset()

        if total is None or total < 0:
            return cls(
                success=False,
                message="No se encontraron registros",
            )

        return cls(
            success=True,
            message="Success",
            total=total,
            items=items,
            limit=raw_params.limit,
            offset=raw_params.offset,
            **kwargs,
        )

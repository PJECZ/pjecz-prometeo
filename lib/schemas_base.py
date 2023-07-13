"""
Schemas Base
"""
from pydantic import BaseModel


class OneBaseOut(BaseModel):
    """OneBaseOut"""

    success: bool = True
    message: str = "Success"


class ListBaseResult(BaseModel):
    """ListBaseResult"""

    total: int
    size: int


class ListBaseOut(OneBaseOut):
    """ListBaseOut"""

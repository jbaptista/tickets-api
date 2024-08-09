from typing import Optional
from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str
    description: str
    active: bool
    parent_id: Optional[int] = None

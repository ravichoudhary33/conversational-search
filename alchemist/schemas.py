from pydantic import BaseModel
from typing import List

class Product(BaseModel):
    title: str
    imageUrl: List[str]
    listPrice: str
    salePrice: str
from pydantic import BaseModel
from typing import List

class CakeInformation(BaseModel):
    name: str
    sizes: List[str]
    price: str
    tested: bool
    finalized: bool
    description: str
    type: str
    image: str
    productId: str
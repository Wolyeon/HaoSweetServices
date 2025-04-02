from pydantic import BaseModel

class CakeInformation(BaseModel):
    name: str
    sizes: str
    price: str
    tested: bool
    finalized: bool
    description: str
    type: str
    image: str
    productId: str
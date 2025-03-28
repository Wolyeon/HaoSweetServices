from pydantic import BaseModel

class CakeInformation(BaseModel):
    name: str
    sizes: str
    price: str
    tested: str
    finalized: str
    description: str
    image: str
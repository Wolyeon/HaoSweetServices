from pydantic import BaseModel

class OrderInformation(BaseModel):
     pickupdate: str
     lactose: str
     cakeName: str
     cakeSize: str
     email: str
     message: str
     allergies: str

   
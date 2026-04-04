# Pydantic Models
from pydantic import BaseModel, Validator, Field

class Item(BaseModel):
    name: str
    price: float
    description: str = None

# Pydantic validator
# Pydantic Field()

class Item(BaseModel):
    name: str = Field(..., min_length=3)
    price: float
    description: str = None
    tax: float = Field(0.0, ge=0)

    @validator('price')
    def check_price(cls, v):
        if v is not None and v < 0:
            raise ValueError("the price can't be negative") 
        return v


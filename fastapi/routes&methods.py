from fastapi import FastAPI
from typing import Optional

app = FastAPI(title='fastapi app', description='this is a simple fast api app', version='1.0.0')

# HTTP methods

# GET method
@app.get('/')
def root():
    return {'status': 'running'}

@app.get('/items/{item_id}')
def read_item(item_id: int):
    return {'id': item_id}

# POST method
@app.post('/items/')
def create_item(item: Item):    #  Item is a pydantic model
    return {'name': item.name}

# PUT method
@app.put('/items/{item_id}')
def update(item_id, item: Item):
    return {'id': item_id, 'new':item.name}


# DELETE method
@app.delete('items/item_id')
def delete(item_id: int):
    return {"message": f"the item with the id {item_id} has been deleted"}

# Path parameter
@app.get('/users/{user_id}')
def read_user(user_id: int):
    return {"id": user_id}

# Query parameters
@app.get('/blogs')
def read_blogs(limit: int =10, published: bool =True):
    if published:
        return {"message": f"they are {limit} blogs published"}
    else:
        return {"message": f"they are {limit} blogs unpublished"}
 

# Combining query parameters with path parameters
@app.get('/users/{user_id}')
def read_user(user_id: int, detail: bool = True):
    if detail:
        return {"id": user_id, "detail": "user details"}
    else: 
        return {"id": user_id}
    

    
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


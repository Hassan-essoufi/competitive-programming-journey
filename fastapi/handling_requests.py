from fastapi import FastAPI, status, HTTPException
from fastapi.response import JSONResponse
from datetime import datetime

app = FastAPI()

# Customizing HTTP responses
@app.get('/items/', status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return {"name": item.name, "price": item.price}


# Customizing response content
@app.post("/items/")
async def create_item(item:Item):
    response_data = {
        "timestamp":datetime.now().isoformat(),
        "data":{"name":item.name, "price":item.price}
       }
    return JSONResponse(content=response_data)

# Custom headers
@app.get("/custom_headers/")
async def custom_headers():
    headers = {"X-Custom-Header": "MyCustomHeaderValue"}
    return JSONResponse(content={"message": "Custom headers added!"},
    headers=headers)

# HTTPExceptions for error handling
from fastapi import HTTPException
app= FastAPI()
items= {"1": {"name": "Item1", "price": 10}}
@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(
        status_code=404,
        detail="Itemnotfound"
    )
    return items[item_id]
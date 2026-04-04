from fastapi import FastAPI
import asyncio


app = FastAPI()
async def fake_db_query():
    await asyncio.sleep(2) # Simulating a database query with a 2-second delay
    return {"message": "Database query completed"}

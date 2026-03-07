from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def valide():
    return {"api running": "we run api"}


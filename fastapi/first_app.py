from fastapi import FastAPI

app = FastAPI(title='hello world')

@app.get('/')
async def root():
    return {'status': 'api running'}

@app.get('/about')
async def about():
    return {'status': 'about page'}


@app.get('/blogs/{id}')
async def blog(id:int):
    return {'blog':id}
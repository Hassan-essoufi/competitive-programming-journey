from typing import List
from fastapi import FastAPI, File, UploadFile

app = FastAPI()
@app.post("/files/")
async def create_file(file: bytes = 
File(...)):
    return {"file_size": len(file)}
@app.post("/uploadfiles/")
async def create_upload_files(files: 
List[UploadFile] = File(...)):
    return {"filenames": [file.filename 
for file in files]}
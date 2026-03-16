from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from main import main
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class ProductRequest(BaseModel):
    product: str

@app.get("/")
def root():
    return FileResponse("index.html")

@app.post("/analyze")
async def analyze(request: ProductRequest):
    result = main(request.product)
    return result
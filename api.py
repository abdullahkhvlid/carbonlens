from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from main import main


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class ProductRequest(BaseModel):
    product: str

@app.post("/analyze")
async def analyze(request: ProductRequest):
    result = main(request.product)
    return result
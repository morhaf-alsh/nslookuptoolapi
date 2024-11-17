from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from lookup import lookup
from schemas import record_type
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/dnslookup")
async def dnslookup(record_type: record_type, request: Request):
    results = {}
    domains = await request.json()
    results = lookup(domains, record_type.value)
    return results
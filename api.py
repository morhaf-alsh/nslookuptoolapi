from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from lookup import lookup
from schemas import record_type
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# origins = [
#     "https://www.morhafsh.com",
#     "https://morhafsh.com"
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.middleware("https")
# async def validate_referer(request: Request, call_next):
#     referer = request.headers.get("referer")
#     if referer and not referer.startswith("https://www.morhafsh.com"):
#         raise HTTPException(status_code=403, detail="Referer not allowed")
#     response = await call_next(request)
#     return response

@app.post("/dnslookup")
async def dnslookup(record_type: record_type, request: Request):
    results = {}
    domains = await request.json()
    results = lookup(domains, record_type.value)
    return results
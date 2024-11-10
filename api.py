from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from lookup import lookup
from schemas import record_type
import uvicorn

app = FastAPI()

@app.get("/dnslookup/")
async def dnslookup(record_type: record_type, request: Request):
    results = {}
    domains = await request.json()
    results = lookup(domains, record_type.value)
    return results

if __name__ == '__main__':
    uvicorn.run("api:app", port=443, host="0.0.0.0", reload=False)
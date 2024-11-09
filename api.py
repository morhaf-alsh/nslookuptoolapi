from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from enum import Enum
import dns
import dns.resolver
from pydantic import BaseModel

class record_type(Enum):
    A = 'A'
    MX = 'MX'
    NS = 'NS'
    AAAA = 'AAAA'
    SOA = 'SOA'
    SPF = 'SPF'
    CNAME = 'CNAME'


app = FastAPI()

@app.post("/dnslookup/")
async def dnslookup(record_type: record_type, request: Request):
    results = {}
    domains = await request.json()
    for domain in domains:
        try:
            answers = dns.resolver.resolve(domain, record_type.value)
            results[domain] = [str(answer) for answer in answers]
        
        except dns.resolver.NoAnswer:
            results[domain] = "No answer found"
        except dns.resolver.NXDOMAIN:
            results[domain] = "Domain not found"
        except Exception as e:
            results[domain] = str(e)

    return results
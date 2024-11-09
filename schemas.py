from pydantic import BaseModel
from enum import Enum

class record_type(Enum):
    A = 'A'
    MX = 'MX'
    NS = 'NS'
    AAAA = 'AAAA'
    SOA = 'SOA'
    SPF = 'SPF'
    CNAME = 'CNAME'
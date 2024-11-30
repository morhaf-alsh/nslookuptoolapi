import dns
import dns.resolver
from schemas import record_type


def lookup(domains, record_type):
    results = {}
    for domain in domains:
        try:
            answers = dns.resolver.resolve(domain, record_type)
            results[domain] = [str(answer) for answer in answers]
        
        except dns.resolver.NoAnswer:
            results[domain] = ["No answer found"]
        except dns.resolver.NXDOMAIN:
            results[domain] = ["Domain not found"]
        except Exception as e:
            results[domain] = str(e)
    return results
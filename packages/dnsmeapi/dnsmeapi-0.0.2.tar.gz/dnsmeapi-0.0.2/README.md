# Dnsmeapi Python client
simplify dnsmadeeasy api calls :- https://api-docs.dnsmadeeasy.com/?version=latest#6a7eef29-27fb-4f37-af89-e3ec4a3dcf66
**Python 3.7**

# Tests  
From the project root directory  
```
export PYTHONPATH=$(pwd)
pytest .
```
# Dnsmeapi Class
```
class Dnsmeapi:
    hmac = None
    request_date = None
    api_key = ""
    api_secret_key = ""

    def __init__(self, api_key, api_secret_key):
        self.api_key = api_key
        self.api_secret_key = api_secret_key

    def make_request(self, method_type, url, payload):
        self.request_date = formatdate(timeval=None, localtime=False, usegmt=True)
        try:
            self.hmac = hmac.new(
                bytes(self.api_secret_key, "UTF-8"),
                bytes(self.request_date, "UTF-8"),
                hashlib.sha1,
            ).hexdigest()
        except Exception as e:
            raise e

        headers = {
            "Content-Type": "application/json",
            "x-dnsme-hmac": self.hmac,
            "x-dnsme-apiKey": self.api_key,
            "x-dnsme-requestDate": self.request_date,
        }

        try:
            response = requests.request(method_type, url, headers=headers, data=payload)
            return response.text.encode('utf-8')
        except Exception as e:
            raise e
```
# Import 
from dnsmeapi import Dnsmeapi

# Initalise class
dnsmeapi = Dnsmeapi(
    "api_key", "api_secret_key"
)

# Send Request
dnsmeapi.make_request(
        "GET", "URL", {}
    )
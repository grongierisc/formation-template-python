import requests

url = "https://localhost/csp/bin/Systems/Module.cxw"

# post on a self-signed certificate
response = requests.get(url, verify=False)

print(response.text)
import requests

url = "http://mockbin.org/bin/900787a9-d40e-4044-b252-feb453ec5b60"

payload = {'foo': 'bar'}

response = requests.request("POST", url, data=payload)

print(response.text)
from sqlalchemy import create_engine,types

import pandas as pd

import requests

engine = create_engine('iris://SuperUser:SYS@localhost:51776/IRISAPP')

# create fake data
df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})

# write to IRIS
df.to_sql('test', engine, if_exists='replace', index=False)

# read from IRIS
df = pd.read_sql('select * from test', engine)

# post to mockbin
url = "https://mockbin.org/echo"
payload = df.to_json(orient='records')
response = requests.request("POST", url, data=payload)
print(response.text)
from sqlalchemy import create_engine,types

import pandas as pd

engine = create_engine('iris://SuperUser:SYS@localhost:51776/IRISAPP')

# create fake data
df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})

# write to IRIS
df.to_sql('test', engine, if_exists='replace', index=False)

# read from IRIS
df = pd.read_sql('select * from test', engine)

engine_pg = create_engine('postgresql://DemoData:DemoData@localhost:5432/DemoData')

# write to Postgres
df.to_sql('test', engine_pg, if_exists='replace', index=False)

# read from Postgres
df = pd.read_sql('select * from test', engine_pg)
print(df)
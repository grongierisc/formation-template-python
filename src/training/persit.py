from sqlalchemy import create_engine

import pandas as pd

# import iris

# iris.system.Process.SetNamespace("IRISAPP")

engine = create_engine('iris+emb://IRISAPP')

df = pd.read_csv('/irisdev/app/misc/formation.csv', sep=';')

df.to_sql('panda', engine, if_exists='replace', schema='Python')
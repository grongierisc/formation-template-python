from flask import Flask, jsonify, request

app = Flask(__name__)

from sqlalchemy import create_engine
import pandas as pd

#engine = create_engine('iris+emb:///IRISAPP')
#engine = create_engine('iris://SuperUser:SYS@localhost:1972/IRISAPP', echo=True)

@app.route("/", methods=["GET"])
def get_info():
    info = {'version':'1.0.6'}
    return jsonify(info)

@app.route("/alchemy/formation/", methods=["POST"])
def formation():
    name = request.get_json()['name']
    room = request.get_json()['room']

    df = pd.DataFrame({'name':[name],'room':[room]})
    df.to_sql('training', engine, schema='iris', if_exists='append', index=False)

    return jsonify({'value':'ok'})

if __name__ == '__main__':
    app.run('0.0.0.0', port = "5000")
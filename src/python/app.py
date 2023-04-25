from flask import Flask, jsonify, request

from msg import FormationRequest
from obj import Formation

from grongier.pex import Director

from sqlalchemy import create_engine
import pandas as pd

import iris

#engine = create_engine('iris://SuperUser:SYS@localhost:1972/IRISAPP')
#engine_pg = create_engine('postgresql://DemoData:DemoData@db:5432/DemoData')

app = Flask(__name__)

@app.route("/", methods=["GET"])
def get_info():
    info = {'version':'1.0.6'}
    return jsonify(info)

@app.route("/", methods=["POST"])
def get_info_post():
    info = {'version':'1.0.6'}
    return jsonify(info)

@app.route("/hello", methods=["POST"])
def hello():
    # get an json attribute named 'name' form the request
    payload = request.get_json()['name']
    # prepare the response
    response = f"Hello {payload}"
    # return the response
    return jsonify({'value':response})

@app.route("/formation", methods=["POST"])
def formation():
    nom = request.get_json()['nom']
    salle = request.get_json()['salle']

    # create Formation 
    formation = Formation(nom=nom,salle=salle)
    # create FormationRequest
    msg = FormationRequest(formation=formation)
    print("before dispatchProcessInput")
    service = Director.CreateBusinessService("Python.FlaskService")
    print("after dispatchProcessInput")
    response = service.ProcessInput(msg)
    print("after dispatchProcessInput(msg)")

    return jsonify({'value':'ok'})


@app.route("/alchemy/formation/", methods=["POST"])
def formation_sqlalchemy():
    name = request.get_json()['name']
    room = request.get_json()['room']

    df = pd.DataFrame({'name':[name],'room':[room]})
    df.to_sql('training', engine, schema='iris', if_exists='append', index=False)

    return jsonify({'value':'ok'})

@app.route("/alchemy/formation_pg/", methods=["GET"])
def formation_sqlalchemy_pg():

    df = pd.read_sql_table('formation', engine_pg, schema='public')
    df.to_sql('training', engine, schema='iris', if_exists='append', index=False)

    return jsonify({'value':'ok'})


if __name__ == '__main__':
    app.run('0.0.0.0', port = "5000")
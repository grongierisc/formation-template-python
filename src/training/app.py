from flask import Flask, request, jsonify

from msg import TrainingMessage,Training

from grongier.pex import Director

app = Flask(__name__)

@app.route('/training', methods=['POST'])
def training():
    # get the payload data
    data = request.get_json()
    # create the message
    training_message = TrainingMessage(
        training=Training(
            id=data['id'],
            name=data['name'],
            room=data['room']
        ),
        verbe='POST'
    )
    # get a new instance of a business service
    service = Director.create_python_business_service('Python.RestService')
    # invoke it
    result = service.dispatch_message(training_message)

    return jsonify(result.training),201

@app.route('/training/<id>', methods=['GET'])
def get_training(id):
    # create the message
    training_message = TrainingMessage(
        training=Training(
            id=id,
            name='',
            room=''
        ),
        verbe='GET'
    )
    # get a new instance of a business service
    service = Director.create_python_business_service('Python.RestService')
    # invoke it
    result = service.dispatch_message(training_message)
    if hasattr(result, 'training'):
        return jsonify(result.training), 200
    else:
        return "", 404

@app.route('/process', methods=['POST'])
def process():
    # get the payload data
    data = request.get_json()
    # create the message
    training_message = TrainingMessage(
        training=Training(
            id=data['id'],
            name=data['name'],
            room=data['room']
        )
    )
    # get a new instance of a business service
    service = Director.create_python_business_service('Python.RestService')
    # invoke it
    result = service.dispatch_message(training_message)

    return jsonify(result.training), 201

@app.route('/training/<id>', methods=['DELETE'])
def delete_training(id):
    # create the message
    training_message = TrainingMessage(
        training=Training(
            id=id,
            name='',
            room=''
        ),
        verbe='DELETE'
    )
    # get a new instance of a business service
    service = Director.create_python_business_service('Python.RestService')
    # invoke it
    result = service.dispatch_message(training_message)
    return "",200

@app.route('/training/<id>', methods=['PUT'])
def put_training(id):
    # get the payload data
    data = request.get_json()
    # create the message
    training_message = TrainingMessage(
        training=Training(
            id=id,
            name=data['name'],
            room=data['room']
        ),
        verbe='PUT'
    )
    # get a new instance of a business service
    service = Director.create_python_business_service('Python.RestService')
    # invoke it
    result = service.dispatch_message(training_message)

    if hasattr(result, 'training'):
        return jsonify(result.training), 200
    else:
        return "", 404

@app.route('/training', methods=['GET'])
def get_all_training():
    # create the message
    training_message = TrainingMessage(
        training=Training(
            id='',
            name='',
            room=''
        ),
        verbe='GET'
    )
    # get a new instance of a business service
    service = Director.create_python_business_service('Python.RestService')
    # invoke it
    result = service.dispatch_message(training_message)
    if hasattr(result, 'training_list'):
        return jsonify(result.training_list), 200
    else:
        return "", 404

if __name__ == '__main__':
    app.run(port=5000)
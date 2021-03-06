"""
	api
~~~

"""

#### Libraries
# Standard library
import os
from flask import Flask, request, jsonify
from flask_cors import cross_origin

# My library
import net_runner
from redis_connector import redis, redis_key


app = Flask(__name__)
#app.config['CORS_ORIGINS'] = ['http://kressi.github.io']

@app.route("/")
def index():
    return 'Github project of <a href="https://github.com/kressi/neural_net">neural_net</a>'

@app.route("/api")
@cross_origin(headers=['Content-Type'])
def api():
    return jsonify( train_with_mnist='http://neural-net.herokuapp.com/train-mnist',
                    train='http://neural-net.herokuapp.com/train',
                    delete_neural_net='http://neural-net.herokuapp.com/delete',
                    recognize_pattern='http://neural-net.herokuapp.com/recognize-pattern' )

@app.route("/train-mnist", methods=["GET", "POST", "OPTIONS"])
@cross_origin(headers=['Content-Type'])
def train_mnist():
    if request.method == 'GET':
        return jsonify(net_runner.train_mnist())
    else:
        print net_runner.train_mnist(request.get_json())
        return jsonify(net_runner.train_mnist(request.get_json()))

@app.route("/train", methods=["POST", "OPTIONS"])
@cross_origin(headers=['Content-Type'])
def train():
    return jsonify(success=0, message='not implemented yet')

@app.route("/delete", methods=["GET", "POST", "OPTIONS"])
@cross_origin(headers=['Content-Type'])
def delete():
    if request.method == 'GET':
        net_id = 'nn'
    else:
        net_id = request.get_json().get('net-id', 'nn')
    return jsonify(net_runner.delete_net(net_id))

@app.route("/recognize-pattern", methods=["POST", "OPTIONS"])
@cross_origin(headers=['Content-Type'])
def recognize():
    params = request.get_json()
    result = net_runner.recognize_pattern(params)
    return jsonify(result)

@app.route("/list-nets", methods=["GET", "OPTIONS"])
@cross_origin(headers=['Content-Type'])
def list_nets():
    nws = net_runner.list_nets()
    if nws != None:
        return jsonify(success = 1, nets = nws)
    else:
        return jsonify(success = 0, message = 'no trained nets found')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)


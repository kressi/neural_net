"""
	api
~~~

"""

#### Libraries
# Standard library
import os
import simplejson as json
from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import cross_origin

# My library
import net_runner
from redis_connector import redis, redis_key


app = Flask(__name__)
app.debug=True
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
    if net_id == 'nn': return jsonify(success=0, message='nn cannot be deleted')
    count=0
    for key in redis.keys():
        if key.split('-')[0]==net_id:
            count += redis.delete(key)
    sccs = 1 if count > 0 else 1
    return jsonify(success=sccs, message='%d records from net %s deleted' % (count, net_id))

@app.route("/recognize-pattern", methods=["POST", "OPTIONS"])
@cross_origin(headers=['Content-Type'])
def recognize():
    pattern = request.get_json()['pattern']
    result = net_runner.recognize_pattern(pattern)
    return jsonify(result)

@app.route("/list-nets")
@cross_origin(headers=['Content-Type'])
def list_nets():
    nets = filter(lambda x: x.split('-')[-1] == 'data', redis.keys())
    if nets.__len__() <= 0:
        return jsonify(success = 0, message = 'no trained nets found')
    else:
        net_ids = list(x.split('-')[0] for x in nets)
        net_params = (redis.get(redis_key('params', key)) for key in net_ids)
        return jsonify(nets=net_ids)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


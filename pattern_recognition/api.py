"""
	api
~~~

"""

#### Libraries
# Standard library
import os
import flask-cors
import simplejson as json
from flask import Flask
from flask import request
from flask import Response

# My library
import net_runner
from redis_connector import redis


app = Flask(__name__)
app.config['CORS_ORIGINS'] = ['http://kressi.github.io']

@app.route("/")
def index():
  return 'Github project of <a href="https://github.com/kressi/neural_net">neural_net</a>'

@app.route("/api")
@cross_origin(headers=['Content-Type'])
def api():
  pretty_api=json.dumps({'train_with_mnist': 'http://neural-net.herokuapp.com/train-mnist',
                         'train': 'http://neural-net.herokuapp.com/train',
                         'reset_neural_net': 'http://neural-net.herokuapp.com/reset',
                         'recognize_pattern': 'http://neural-net.herokuapp.com/recognize-pattern'
                        }, sort_keys=True, indent=4 * ' ')
  return Response(pretty_api, mimetype='application/json')

@app.route("/train-mnist")
@cross_origin(headers=['Content-Type'])
def train_mnist():
  return net_runner.train_mnist()

@app.route("/train", methods=["POST"])
@cross_origin(headers=['Content-Type'])
def train():
  return "train neural net with single letter - not implemented yet"

@app.route("/reset")
@cross_origin(headers=['Content-Type'])
def reset():
  count=redis.delete('nn-status')
  return "net reset, %d records deleted from redis" % count

@app.route("/recognize-pattern", methods=["POST"])
@cross_origin(headers=['Content-Type'])
def recognize():
  pattern = request.get_json()['pattern']
  result = net_runner.recognize_pattern(pattern)
  return Response(str(result), mimetype='application/json')

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port)


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
from flask import render_template

# My library
import net_runner
from redis_connector import redis


app = Flask(__name__)

@app.route("/")
def index():
  return 'Github project of <a href="https://github.com/kressi/neural_net">neural_net</a>'

@app.route("/api")
def api():
  pretty_api=json.dumps({'train_with_mnist': 'http://neural-net.herokuapp.com/train-mnist',
                         'train': 'http://neural-net.herokuapp.com/train',
                         'reset_neural_net': 'http://neural-net.herokuapp.com/reset',
                         'recognize_pattern': 'http://neural-net.herokuapp.com/recognize-pattern'
                        }, sort_keys=True, indent=4 * ' ')
  return render_template('pre_code.html', body=pretty_api)

@app.route("/train-mnist")
def train_mnist():
  net_runner.train_mnist()

@app.route("/train", methods=["POST"])
def train():
  return "train neural net with single letter"

@app.route("/reset")
def reset():
  count=redis.delete('nn-status')
  return "net reset, %d records deleted from redis" % count

@app.route("/recognize-pattern", methods=["POST"])
def recognize():
  f = request.files['the_file']
  return "recognize pattern"

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port)


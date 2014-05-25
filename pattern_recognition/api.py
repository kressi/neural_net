import os
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/api")
@app.route("/")
def api():
  return "api"

@app.route("/train-mnist")
def train_mnist():
  return "training neural net with mnist training data"

@app.route("/train", methods=["POST"])
def train():
  return "train neural net with single letter"

@app.route("/reset")
def reset():
  return "neural net reset"

@app.route("/recognize", methods=["POST"])
def recognize():
  f = request.files['the_file']
  return "recognize pattern"

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port)


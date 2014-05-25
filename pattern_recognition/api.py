import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def api():
  return "api"

@app.route("/api")
return api()

@app.route("/train-mnist")
def train()
  return "training neural net with mnist training data"

@app.route("/train", method='POST')
  return "train neural net with single letter"

@app.route("/reset")
  return "neural net reset"

@app.route("/recognize", method='POST')
  return "recognize pattern"

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port)


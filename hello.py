from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
  import random
  return str(random.randint(1,1000001))

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8081)

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    print("✅ Hello route was hit")
    return "Hello from minimal app", 200

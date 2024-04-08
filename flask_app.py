from flask import Flask, request

from RootUtils.webhook import webhook

REPO_PATH_SERVER = "mysite/"


app = Flask(__name__)

app.config["REPO_PATH_SERVER"] = REPO_PATH_SERVER

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/update_server', methods=['POST'])
def func():
    return webhook(request, app.config)
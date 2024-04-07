import json
from flask import Flask, request
import git

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/update_server', methods=['POST'])
def webhook():
    
    if request.method == 'POST':
        event = request.headers.get('X-GitHub-Event')
        if event == "ping":
            return json.dumps({'msg': 'Hi!'}), 200
        if event != "push":
            return json.dumps({'msg': "Wrong event type"}), 400
        repo = git.Repo('path/to/git_repo')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400
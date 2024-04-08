import json
import git

def webhook(request, appConfig):
    if request.method == 'POST':
        event = request.headers.get('X-GitHub-Event')
        if event == "ping":
            return json.dumps({'msg': 'Hi!'}), 200
        if event != "push":
            return json.dumps({'msg': "Wrong event type"}), 400
        repo = git.Repo(appConfig["REPO_PATH_SERVER"])
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400
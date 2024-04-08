from flask import Flask, request
import os

from CropsDiseaseClassifier.upload_file import upload_image

from RootUtils.webhook import webhook

REPO_PATH_SERVER = "mysite/"
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'CropsDiseaseClassifier/uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_SIZE = 16 * 1000 * 1000

app = Flask(__name__)

app.config["REPO_PATH_SERVER"] = REPO_PATH_SERVER
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["ALLOWED_EXTENSIONS"] = ALLOWED_EXTENSIONS
app.config["ALLOWED_SIZE"] = ALLOWED_SIZE

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/crops/upload_image", methods=["POST"])
def upload_file()->str:
    return upload_image(request, app.config)


@app.route('/update_server', methods=['POST'])
def webhook_func():
    return webhook(request, app.config)
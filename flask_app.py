from flask import Flask, request
import os
import json

from CropsDiseaseClassifier.upload_file import upload_image
from RootUtils.webhook import webhook
from CropsDiseaseClassifier.inference import inference

from flask_cors import CORS

REPO_PATH_SERVER = "mysite/"
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'CropsDiseaseClassifier/uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_SIZE = 16 * 1000 * 1000

app = Flask(__name__)
cors = CORS(app, resources={r"/crops/infer_image": {"origins": "*"}})

app.config["REPO_PATH_SERVER"] = REPO_PATH_SERVER
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["ALLOWED_EXTENSIONS"] = ALLOWED_EXTENSIONS
app.config["ALLOWED_SIZE"] = ALLOWED_SIZE

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/crops/infer_image", methods=["POST"])
def infer_img()->str:
    try:
        string, file_name = upload_image(request, app.config)
        if file_name != "":
            prediction, confidence = inference(os.path.join(app.config["UPLOAD_FOLDER"], file_name))
            # Delete the file after inference
            os.remove(os.path.join(app.config["UPLOAD_FOLDER"], file_name))
            return json.dumps({"message": "Prediction Successful", "prediction": prediction, "confidence": confidence})
        else:
            return f"{string}"
    except Exception as e:
        return json.dumps(f"Error: {e}"), 500


@app.route('/update_server', methods=['POST'])
def webhook_func():
    return webhook(request, app.config)
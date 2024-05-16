import base64
import io
from flask import Flask, request, send_file
import os
import json
from flask_cors import CORS
from markupsafe import escape

from PIL import Image

from CropsDiseaseClassifier.upload_file import upload_image
from CropsDiseaseClassifier.inference import inference, simulateAttack
from RootUtils.webhook import webhook
from RootUtils.npToImg import npToImg64

from RootUtils.allowed_file import allowed_file_hash
from werkzeug.utils import secure_filename

from Tree.Models.Encoder import Encoder


REPO_PATH_SERVER = "mysite/"
UPLOAD_FOLDER_CROPS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'CropsDiseaseClassifier/uploads')
ALLOWED_EXTENSIONS_CROPS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_SIZE = 16 * 1000 * 1000

UPLOAD_FOLDER_HASH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Tree/uploads')
ALLOWED_EXTENSIONS_HASH = {'txt'}

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

app.config["REPO_PATH_SERVER"] = REPO_PATH_SERVER
app.config["UPLOAD_FOLDER_CROPS"] = UPLOAD_FOLDER_CROPS
app.config["ALLOWED_EXTENSIONS_CROPS"] = ALLOWED_EXTENSIONS_CROPS
app.config["ALLOWED_SIZE"] = ALLOWED_SIZE

app.config["UPLOAD_FOLDER_HASH"] = UPLOAD_FOLDER_HASH
app.config["ALLOWED_EXTENSIONS_HASH"] = ALLOWED_EXTENSIONS_HASH

file_name = ""

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/crops/infer_image", methods=["POST"])
def infer_img()->str:
    global file_name
    try:
        string, file_name = upload_image(request, app.config)
        if file_name != "":
            prediction, confidence = inference(os.path.join(app.config["UPLOAD_FOLDER_CROPS"], file_name))
            # Delete the file after inference
            # os.remove(os.path.join(app.config["UPLOAD_FOLDER_CROPS"], file_name))
            return json.dumps({"message": "Prediction Successful", "prediction": prediction, "confidence": confidence})
        else:
            return f"{string}"
    except Exception as e:
        return json.dumps(f"Error: {e}"), 500
    
@app.route("/crops/attack/<attackMethod>", methods=["POST"])
def attack_image(attackMethod):
    global file_name
    file_name = "Unknown.jpeg"
    if file_name == "":
        return json.dumps({"message": "No file uploaded yet"}), 400
    img,className,attackConf,noiseImg,_,_ = simulateAttack(inputPath=(os.path.join(app.config["UPLOAD_FOLDER_CROPS"], file_name)), fgsm=(attackMethod=="fgsm"))

    img_base64 = npToImg64(img)

    noise_base64 = npToImg64(noiseImg)


    return json.dumps({"message": "Attack Successful", "adversial_image": img_base64, "adversial_class": className, "adversial_confidence": attackConf, "noiseImg":noise_base64})


@app.route('/update_server', methods=['POST'])
def webhook_func():
    return webhook(request, app.config)

@app.route("/hash/upload_file", methods=['POST'])
def upload_file():
    if request.method != 'POST':
        return "Method not allowed. Please send a POST request.", 405
    
    if 'file' not in request.files:
        return "No file part", 400
    
    file = request.files['file']

    if file and allowed_file_hash(file.filename, app.config, request):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER_HASH'], filename)
        file.save(file_path)
        encoder = Encoder(fileOrString=file_path, isFile=True)
        return f"File Hash Value {encoder.getFinalHash()}", 200
        # return f"File uploaded successfully {filename}", 200
    else:
        return "File not allowed", ""
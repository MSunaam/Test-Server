import base64
import io
from flask import Flask, request, send_file
import os
import json
from flask_cors import CORS
from markupsafe import escape

from PIL import Image

from CropsDiseaseClassifier.upload_file import upload_image
from RootUtils.webhook import webhook
from CropsDiseaseClassifier.inference import inference, simulateAttack

#test


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
            prediction, confidence = inference(os.path.join(app.config["UPLOAD_FOLDER"], file_name))
            # Delete the file after inference
            # os.remove(os.path.join(app.config["UPLOAD_FOLDER"], file_name))
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
    img,className,attackConf,noiseImg,_,_ = simulateAttack(inputPath=(os.path.join(app.config["UPLOAD_FOLDER"], file_name)), fgsm=(attackMethod=="fgsm"))
    
    img = Image.fromarray(img)
    img_byte_array = io.BytesIO()
    img.save(img_byte_array, format='PNG')
    img_byte_array.seek(0)

    img_base64 = base64.b64encode(img_byte_array.read()).decode('utf-8')


    return json.dumps({"message": "Attack Successful", "adversial_image": f"data:image/png;base64,{img_base64}", "adversial_class": className, "adversial_confidence": attackConf})


@app.route('/update_server', methods=['POST'])
def webhook_func():
    return webhook(request, app.config)
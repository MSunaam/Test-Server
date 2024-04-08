import os
import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
import argparse

DEVICE = "cpu"
NUM_CLASSES = 22
PATH_TO_MODEL = "CropsDiseaseClassifier/checkpoint_11_epoch_lr=0.000001_2.pth"
CLASSES = ['Cashew_anthracnose', 'Cashew_gumosis', 'Cashew_healthy', 'Cashew_leaf miner', 'Cashew_red rust', 'Cassava_bacterial blight', 'Cassava_brown spot', 'Cassava_green mite', 'Cassava_healthy', 'Cassava_mosaic', 'Maize_fall armyworm', 'Maize_grasshoper', 'Maize_healthy', 'Maize_leaf beetle', 'Maize_leaf blight', 'Maize_leaf spot', 'Maize_streak virus', 'Tomato_healthy', 'Tomato_leaf blight', 'Tomato_leaf curl', 'Tomato_septoria leaf spot', 'Tomato_verticulium wilt']


def loadImage(pathToImage):
    """"
    takes input the path of image and returns the tensor with the dimensions of batch
    """
    image = Image.open(pathToImage)

    transformToTorch = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor()
    ])

    tensorImage = transformToTorch(image).to(DEVICE, dtype=torch.float32)

    batchTensor = tensorImage.unsqueeze(0)

    return batchTensor

def loadModel(pathToModel):
    """
    takes input the path for .pth file of the (modified)resnet, loads weights and returns the model
    """
    
    resnet = models.resnet50(pretrained=True)

    resnet.fc = nn.Linear(resnet.fc.in_features, NUM_CLASSES)

    resnet = resnet.to(DEVICE)

    checkpoint = torch.load(pathToModel,map_location=torch.device(DEVICE))                                                                              
    
    resnet.load_state_dict(checkpoint['model_state_dict'])

    return resnet


def inference(pathToImage):
    """"
    takes input the path for the image and returns the probabilities
    """
    tensor = loadImage(pathToImage)
    model = loadModel(pathToModel=PATH_TO_MODEL)
    
    model.eval()
    with torch.no_grad():
        output = model(tensor)
        confidenceTesnor = torch.nn.Softmax(dim=1)(output).data
        maxProbIdx = torch.argmax(confidenceTesnor,dim=1)
        finalPrediction = CLASSES[maxProbIdx];
    
    print(f"Disease {finalPrediction} Confidence Level {(confidenceTesnor.tolist())[0][maxProbIdx]*100}%\n")
    return finalPrediction, round(confidenceTesnor.tolist()[0][maxProbIdx]*100, 2)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script for making infrences from model')
    parser.add_argument('-p', type=str, required=True, help='path to the image for which inference has to be made')
    args = parser.parse_args()

    print("Image path:", args.p)

    imagePath = args.p

    assert os.path.exists(imagePath), f"No file found at {imagePath}"

    inference(imagePath)

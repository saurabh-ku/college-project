import torch 
import torch.nn as nn
import torchvision
from torchvision import datasets, models, transforms
import os
from torch.autograd import Variable
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.layer1 = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=5, padding=2),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.MaxPool2d(2))
        self.layer2 = nn.Sequential(
            nn.Conv2d(16, 32, kernel_size=5, padding=2),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2))
        self.fc = nn.Linear(56*56*32, 5)
        
    def forward(self, x):
        out = self.layer1(x)
        out = self.layer2(out)
        out = out.view(out.size(0), -1)
        out = self.fc(out)
        return out

def image_loader(image):
    """load image, returns cuda tensor"""
    loader =  transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    # image = Image.open(image_name)
    image = loader(image).float()
    image = Variable(image, requires_grad=True)
    image = image.unsqueeze(0)  #this is for VGG, may not be needed for ResNet
    return image  #assumes that you're using GPU

def inference(img):
    state_dict = torch.load('./cnn_2layer_latest.pkl', map_location='cpu')
    # image = image_loader('./data/lena.jpg')
    image = image_loader(img)	
    cnn = CNN()

    cnn.load_state_dict(state_dict)

    output = cnn(image)
    _, predicted = torch.max(output.data, 1)
    return int(predicted)
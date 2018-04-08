#!flask/bin/python
from flask import Flask, request, Response
import jsonpickle
import numpy as np
import cv2
import random
from PIL import Image
import imutils

from tester import *

import os
import paramiko
from scp import SCPClient

def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client

# Initialize the Flask application
app = Flask(__name__)

def getClassFromImg(img):
    # return random.randint(0, 4)

    return inference(img)

# route http posts to this method
@app.route('/api/getclass', methods=['POST'])
def getclass():
    ssh = createSSHClient("192.168.43.70", 22, "pi", "raspberry")
    scp = SCPClient(ssh.get_transport())
    scp.get("/home/pi/Documents/college-project/data/img.jpg", "./fromscp", recursive = True)

    img = Image.open("./fromscp/img.jpg")
    # img.show()

    imgClass = getClassFromImg(img)
    print(imgClass)
    # build a response dict to send back to client
    response = {
            'class': '{}'.format(imgClass)
                }
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")
    

# start flask app
app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)

#!flask/bin/python
from flask import Flask, request, Response
import jsonpickle
import numpy as np
import cv2
import random
from PIL import Image

from tester import *

# Initialize the Flask application
app = Flask(__name__)

def getClassFromImg(img):
    # return random.randint(0, 4)

    return inference(img)

# route http posts to this method
@app.route('/api/getclass', methods=['POST'])
def getclass():
    r = request
    # convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # do some fancy processing here....

    img = Image.fromarray(img)
    img.show()
    # img.show()

    imgClass = getClassFromImg(img)
    # build a response dict to send back to client
    response = {
            'class': '{}'.format(imgClass)
                }
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")
    

# start flask app
app.run(host="0.0.0.0", port=5000, debug=False)

#!flask/bin/python

import RPi.GPIO as GPIO
import time
import cv2
import requests
import json
from picamera import PiCamera
from PIL import Image

classToLed = [24, 25, 8, 7, 12]

def switchOnLed(type):
        GPIO.output(classToLed[type], True)

def switchOffLed(type):
        GPIO.output(classToLed[type], False)

def resetLed():
    for i in range(0, 5):
        GPIO.output(classToLed[i], False)
        time.sleep(0.2)

def testLights():
    for i in range(0, 5):
        print "light up", i
        switchOnLed(i)
        time.sleep(2)
        switchOffLed(i)

def clientCode():
    addr = 'http://192.168.29.148:5000'
    test_url = addr + '/api/getclass'

    # prepare headers for http request
    content_type = 'image/jpeg'
    headers = {'content-type': content_type}

    img = cv2.imread('/data/img.jpg')
    # encode image as jpeg
    _, img_encoded = cv2.imencode('.jpg', img)
    # send http request with image and receive response
    
    # img = Image.open('lena.jpg')

    response = requests.post(test_url, data=img_encoded.tostring(), headers=headers)
    classObj = json.loads(response.text)
    imgClass = classObj['class']
    imgClass = int(imgClass)
    # decode response
    return imgClass

def takePictue(camera):
    imgPath = 'lena.jpg'
    camera.capture(imgPath)
    # camera.close()
    

def callPi():
    GPIO.setmode(GPIO.BCM)

    #Button to GPIO23
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)	
    #Led
    GPIO.setup(24, GPIO.OUT)
    GPIO.setup(25, GPIO.OUT)  
    GPIO.setup(8, GPIO.OUT)  
    GPIO.setup(7, GPIO.OUT)  
    GPIO.setup(12, GPIO.OUT)

    # camera = PiCamera()
    # camera.start_preview()
    
    resetLed()
    switchOnLed(4)
    # prev_input = 0

    try:
        resetLed()
        imgClass = clientCode()
        print "Image class is {}".format(imgClass)
        switchOnLed(imgClass)
    except:
        print "clean up"
        GPIO.cleanup()
    finally:
        camera.stop_preview()

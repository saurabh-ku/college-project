#!flask/bin/python

import RPi.GPIO as GPIO
import time
import cv2
import requests
import json

classToLed = [24, 25, 8, 7, 12]

def switchOnLed(type):
        GPIO.output(classToLed[type], True)

def switchOffLed(type):
        GPIO.output(classToLed[type], False)

def resetLed():
    for i in range(0, 4):
        GPIO.output(classToLed[i], False)

def clientCode():
    addr = 'http://192.168.29.148:5000'
    test_url = addr + '/api/getclass'

    # prepare headers for http request
    content_type = 'image/jpeg'
    headers = {'content-type': content_type}

    img = cv2.imread('lena.jpg')
    # encode image as jpeg
    _, img_encoded = cv2.imencode('.jpg', img)
    # send http request with image and receive response
    
    response = requests.post(test_url, data=img_encoded.tostring(), headers=headers)
    classObj = json.loads(response.text)
    imgClass = classObj['class']

    # decode response
    return imgClass



def main():
    GPIO.setmode(GPIO.BCM)

    #Button to GPIO23
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    #Led
    GPIO.setup(24, GPIO.OUT)
    GPIO.setup(25, GPIO.OUT)  
    GPIO.setup(8, GPIO.OUT)  
    GPIO.setup(7, GPIO.OUT)  
    GPIO.setup(12, GPIO.OUT)    

    try:
        while True:
            button_state = GPIO.input(23)
            if button_state == False:
                # resetLed()
                # imgClass = clientCode() 
                # print ("Image class is {}".format(imgClass))
                print "button pressed"
                switchOnLed(0)
            else:
                switchOffLed(0)
    except:
        GPIO.cleanup()

main()


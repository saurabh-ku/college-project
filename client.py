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

    img = cv2.imread('lena.jpg')
    # encode image as jpeg
    _, img_encoded = cv2.imencode('.jpg', img)
    # send http request with image and receive response
    
    response = requests.post(test_url, data=img_encoded.tostring(), headers=headers)
    classObj = json.loads(response.text)
    imgClass = classObj['class']
    imgClass = int(imgClass)
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

    i = 0
    j = 0

    resetLed()
    switchOnLed(4)
    prev_input = 1
    try:
        while True:
            input = GPIO.input(23)
            #if the last reading was low and this one high, print
            if ((not prev_input) and input):
                resetLed()
                imgClass = clientCode()
                print "Image class is {}".format(imgClass)
                switchOnLed(imgClass)
                time.sleep(0.2)
                
            #update previous input
            prev_input = input
            #slight pause to debounce
            time.sleep(0.05)
    except:
        print "clean up"
        GPIO.cleanup()

main()



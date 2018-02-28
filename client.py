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

def testLights():
    for i in range(0, 4):
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

    # decode response
    return imgClass



def main():
    GPIO.setmode(GPIO.BCM)

    #Button to GPIO23
    GPIO.setup(23, GPIO.IN)

    #Led
    GPIO.setup(24, GPIO.OUT)
    GPIO.setup(25, GPIO.OUT)  
    GPIO.setup(8, GPIO.OUT)  
    GPIO.setup(7, GPIO.OUT)  
    GPIO.setup(12, GPIO.OUT)    

    i = 0
    j = 0
    print "start of code"
    resetLed()
    prev_input = 0
    try:
        while True:

            # button_state = GPIO.input(23)
            # if ((not prev_input) and button_state):
            #     # resetLed()
            #     # imgClass = clientCode() 
            #     # print ("Image class is {}".format(imgClass))
            #     i += 1
            #     print "button pressed", i
            #     switchOnLed(0)
            # j += 1
            # print "hello", j
            # prev_input = button_state
            # testLights()

            # button_state = GPIO.input(23)
            # if button_state == False:
            #     switchOnLed(0)
            #     print "Button pressed"
            #     time.sleep(0.2)
            # else:
            #     switchOffLed(0)
            
            #take a reading
            input = GPIO.input(23)
            #if the last reading was low and this one high, print
            if ((not prev_input) and input):
                print("Button pressed")
            #update previous input
            prev_input = input
            #slight pause to debounce
            time.sleep(0.05)
    except:
        print "clean up"
        GPIO.cleanup()

main()



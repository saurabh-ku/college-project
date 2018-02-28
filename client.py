import RPi.GPIO as GPIO
import time

classToLed = [24, 25, 8, 7, 12]

def switchOnLed(type):
        GPIO.output(classToLed[type], True)

def switchOffLed(type):
        GPIO.output(classToLed[type], False)


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
                 #button_state = GPIO.input(23)
                 #if button_state == False:
                 #   GPIO.output(24, True)
                 #    print('Button Pressed...')
                 #    time.sleep(0.2)
                 #else:
                 #    GPIO.output(24, False)
                 for i in range(0, 5):
                        switchOnLed(i)
                        time.sleep(1)
                        switchOffLed(i)
        except:
                GPIO.cleanup()
main()

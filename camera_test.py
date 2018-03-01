from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.start_preview()

camera.capture("./test1.jpg")

sleep(3)

camera.capture("./test2.jpg")

camera.stop_preview()
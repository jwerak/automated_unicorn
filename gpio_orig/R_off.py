import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.OUT)
GPIO.output(17, GPIO.HIGH)

#GPIO.cleanup()

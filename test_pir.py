import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

PIR_GPIO_PIN=18
GPIO.setup(PIR_GPIO_PIN, GPIO.IN)
print ("PIR Module test")
time.sleep(2)
print ("ready")

while True:
        if GPIO.input(PIR_GPIO_PIN):
            print ("Motion detected!")
        time.sleep(0.2)
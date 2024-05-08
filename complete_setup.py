import RPi.GPIO as GPIO
import time

PIR_GPIO_PIN=18
RELAY_GPIO_PIN=15

GPIO.setmode(GPIO.BCM)

GPIO.setup(PIR_GPIO_PIN,GPIO.IN)
GPIO.setup(RELAY_GPIO_PIN,GPIO.OUT)
print("Motion dependent security sensor")
time.sleep(2)

while True:
    #print(GPIO.input(PIR_GPIO_PIN))
    if GPIO.input(PIR_GPIO_PIN):
        #print("Motion detected")
        GPIO.output(RELAY_GPIO_PIN, GPIO.LOW)
        time.sleep(0.5)
        GPIO.output(RELAY_GPIO_PIN, GPIO.HIGH)
    time.sleep(0.2)
GPIO.cleanup()
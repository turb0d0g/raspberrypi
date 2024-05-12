import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BCM)
gpio.setup(21, gpio.OUT)

while True:
   gpio.output(21, gpio.HIGH)
   passcode = raw_input("What is pi?: ")
   
   if passcode == "Awesome":
      gpio.output(21, gpio.LOW)
      time.sleep(4)
   else:
      gpio.output(21, gpio.HIGH)
      print("Wrong Password!")	

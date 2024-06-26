import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BCM)
gpio.setup(17, gpio.OUT)

while True:
   gpio.output(17, gpio.HIGH)
   passcode = "Awesome"
   
   if passcode == "Awesome":
      gpio.output(17, gpio.LOW)
      time.sleep(4)
   else:
      gpio.output(17, gpio.HIGH)
      print("Wrong Password!")	

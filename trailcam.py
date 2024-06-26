
#!/usr/bin/python
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|R|a|s|p|b|e|r|r|y|P|i|-|S|p|y|.|c|o|.|u|k|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# pir_2.py
# Measure the holding time of a PIR module
#
# Author : Matt Hawkins
# Date   : 20/02/2013

# Import required Python libraries
import time
import RPi.GPIO as GPIO
import picamera2

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Define GPIO to use on Pi
GPIO_PIR = 7

print ("PIR Module Holding Time Test (CTRL-C to exit)")

# Set pin as input
GPIO.setup(GPIO_PIR,GPIO.IN)      # Echo

Current_State  = 0
Previous_State = 0

try:

  print ("Waiting for PIR to settle ...")

  # Loop until PIR output is 0
  while GPIO.input(GPIO_PIR)==1:
    Current_State  = 0

  print ("  Ready")

  piccounter = 0
  camera = picamera.PiCamera()
  camera.resolution = (1024, 768)
  camera.hflip = True
  camera.vflip = True

  # Loop until users quits with CTRL-C
  while True :

    # Read PIR state
    Current_State = GPIO.input(GPIO_PIR)

    if Current_State==1 and Previous_State==0:
      # PIR is triggered
      start_time=time.time()
      print ("  Motion detected!")
      # Record previous state
      Previous_State=1
      # !!! modified pir_2.py here !!!
      # capture image now
      camera.capture('image' + str(piccounter) + '.jpg')
      piccounter = piccounter + 1
    elif Current_State==0 and Previous_State==1:
      # PIR has returned to ready state
      stop_time=time.time()
      print ("  Ready ",)
      elapsed_time=int(stop_time-start_time)
      print (" (Elapsed time : " + str(elapsed_time) + " secs)")
      Previous_State=0

except KeyboardInterrupt:
  print ("  Quit")
  # Reset GPIO settings
  GPIO.cleanup()

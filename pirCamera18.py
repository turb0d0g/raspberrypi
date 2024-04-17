#!/usr/bin/python
# pirCamera18.py
#
# Raspberry Pi day and night game camera
# This project uses the Raspberry NOR Pi Camera module(infrared)for
# night time video recording when something is detected.
# It has an external IR LED Lamp that is enabled when motion is 
# detected to illuminate the area while capturing video.  Once the
# selected video duration completes the IR LED lamp is turned off.
#
# The design also has an LDR circuit to detect whether its day or 
# night.  If it is nightime and motion is detected, the IR LED lamp 
# is enabled and lamp is disabled. If daytime is detected, the external
# IR LED lamp is disabled.
# 
# Connecting the external IR LED cable grounds a sense pin to detect
# if lamp is connected. If the external IR Lamp is not detected, the
# lamp output is disabled.
# 
# After PIR detect, if night, GPIO pin 22 activates the relay
# which drives the high current IR LED's (If connected).

#*********Other notes ***********************************
#
# Sudo command to hard-set date and time on Raspberry:
# sudo date -s "Mon Aug 12 20:14:11 PST 2014"
#
# To disable the Camera LED, modify:
# /boot/config.txt
# adding:  disable_camera_led=1
#
# Save ~20mA by turning off PAL/HDMI outputs by changing config.txt
# adding: /opt/vc/bin/tvservice -off
# 

# Kent Peterson
# 15 June 2015

import os
import RPi.GPIO as GPIO
import time
import picamera
import datetime		# add date time
def getFileName():		# specifying .h264 encoded file
    return datetime.datetime.now() .strftime("%Y-%m-%d_%H.%M.%s.h264")

video_duration = 5		# recording duration in seconds
minimumspace = 1000000000	# minimum space to reserve

# Define PIR input pin 7 (GPIO 4)
PIR_Pin = 7 			# PIR sensor input pin 7 
# Define relay drive set pin 5 (GPIO 24)
relay_set_pin = 18 		# Output to Set Relay On IR LED array
# Define relay drive reset pin 3 (GPIO 25)
relay_reset_pin = 22 	# Output to Reset Relay Off IR LED array
# Define LDR sense circuit input pin 16 (GPIO 23)
LDR_Pin = 16 			# LDR circuit input 16
# Define IR Lamp sense circuit input pin 15 (GPIO 22)
IR_Pin = 15 			# Cable Sense circuit input 15


GPIO.setmode(GPIO.BOARD) # Sets up GPIO by pin#
# Set up GPIO interface output for LED relay
GPIO.setup(relay_set_pin, GPIO.OUT)
GPIO.setup(relay_reset_pin, GPIO.OUT)
# Set up GPIO interface input for PIR Sensor
GPIO.setup(PIR_Pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# Set up GPIO interface input for LDR circuit sensor
GPIO.setup(LDR_Pin, GPIO.IN)
# Set up GPIO interface input for LED cable detect
GPIO.setup(IR_Pin, GPIO.IN)
# Define the Pi Camera
cam = picamera.PiCamera()

# Reset detect flags
detect = False	# Set PIR detect flag to faulse
day_time = True	# Set as true in case LDR failure
LED = False		# Set LED to faulse


try:
    while True:
        time.sleep(0.1)
#  First step is if any motion is detected
        detect = GPIO.input(PIR_Pin) #PIR detect? set new=TRUE, if not, loop
        day_time = GPIO.input(LDR_Pin) #is it day or night? True = Day
        LED = GPIO.input(IR_Pin)       #is LED connected?

        if detect:	# PIR is true when movement detection
            time.sleep(0.1)

            if day_time:    # Day time detected
                print ("Day Time Detect")
#   Make sure that IR LED Relay is off
                GPIO.output(relay_reset_pin, False) 	# Turn off LED's


# Is the disk full?  check before creating file.
# First step below is to determine remaining disk space
                disk = os.statvfs("/var/")         
                totalAvailSpaceNonRoot = float(disk.f_bsize*disk.f_bavail)
                print "Available space: %d Bytes " % (totalAvailSpaceNonRoot)

                if totalAvailSpaceNonRoot > minimumspace: # Disk space available?
                    print("Available Space OK")

#   Turn on camera here
                    fileName = getFileName() 	 # generate time-tagged filename
                    cam.start_preview()
                    cam.start_recording(fileName)# Start recording
                    time.sleep(video_duration)   # Duration for video recording
#   Stop camera recording
                    cam.stop_preview()
                    cam.stop_recording()         # new video captured!!
                    print("Stop Recording")
                    print("*********************")


                else:
                    print("Available disk space too small")
                    GPIO.output(relay_reset_pin, True)  # Turn off LED's
                    time.sleep(0.02)                    # relay pulse width
                    GPIO.output(relay_reset_pin, False) # reset pulse complete
                    GPIO.cleanup()                      # cleanup all GPIO
                    print("GPIO Cleaned up, Aborting Program")
                    break          # stop program - ran out of disk space


            else:          # Night time detected
                print ("Night Time Detect")

#   Only enable relay if LED cable is connected.  

                if LED:    # Cable not detected, do not drive relay
                    print ("LED Cable Not Detected")
                    time.sleep(video_duration)


                else:      # Cable detected, drive relay
                    print ("LED Cable Detected")
    
#   Turn on IR LED Relays
                    GPIO.output(relay_set_pin, True) 	# Turn on LED's
                    time.sleep(0.02)                   # relay pulse width
                    GPIO.output(relay_set_pin, False)  # set pulse completed

#   Is the disk full?  check before creating file
                disk = os.statvfs("/var/")
          
                totalAvailSpaceNonRoot = float(disk.f_bsize*disk.f_bavail)
                print "Available space: %d Bytes " % (totalAvailSpaceNonRoot)

                if totalAvailSpaceNonRoot > minimumspace:
                    time.sleep(1)
                    print("Available Space OK")

                    fileName = getFileName() 	# generate time-tagged filename
#   Turn on camera here
                    cam.start_preview()
                    cam.start_recording(fileName) 	# Start recording
                    time.sleep(video_duration)
#   Stop camera recording
                    cam.stop_preview()
                    cam.stop_recording() # new video captured!!
                    print("Stop Recording")
                    print("*********************")

                else:
                    print("Available disk space too small")
                    GPIO.output(relay_reset_pin, True)	# Turn off LED's
                    time.sleep(0.02)				# relay pulse width
                    GPIO.output(relay_reset_pin, False) 	# reset pulse complete
                    GPIO.cleanup()  				# cleanup all GPIO
                    print("GPIO Cleaned up, Aborting Program")
                    break   # stop program - ran out of disk space

#   Turn off Relays
                GPIO.output(relay_reset_pin, True) 	# Turn off LED's
                time.sleep(0.02)                       # relay pulse width
                GPIO.output(relay_reset_pin, False) 	# reset pulse completed
        
        else:
            time.sleep(0.1)


# Cleanup code
except KeyboardInterrupt: 			# If CTRL-C
    GPIO.output(relay_reset_pin, True) 	# Turn off LED's
    time.sleep(0.02)                	# pulse width
    GPIO.output(relay_reset_pin, False)	# pulse complete
    GPIO.cleanup()				# cleanup all GPIO
    print("GPIO Cleaned up")
    
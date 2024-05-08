#!/usr/bin/python
import time
from random import randint
import cv2

from picamera2 import Picamera2, Preview, MappedArray

# Let's pick a random number and use that in our testing session. We can
# append this number to the photograph that's saved so we know which session belongs to which
rand = randint(2,100000)

# We're using picamera to talk to the camera module and take a photo
# cam = picamera.PiCamera()
picam2 = Picamera2()

# Show a live preview from the camera on the desktop and take a photo
preview_config = picam2.create_preview_configuration(main={"size": (800, 600)})
picam2.configure(preview_config)
picam2.start_preview(Preview.QTGL)
picam2.start()
time.sleep(2)

metadata = picam2.capture_file("/home/hairpi/HogJuice/images/hogJuiceCam_"+ str(rand) + ".jpg")
#print(metadata)

# Wait 5 seconds and then stop the preview
time.sleep(5)   
picam2.close()
          
 
#cam.stop_preview()

# Check the same folder (Test_my_camera) to view the photos that have been taken

# END

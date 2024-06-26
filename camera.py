#!/usr/bin/python3

from picamera2 import Picamera2, Preview
from time import sleep
from datetime import datetime

picam2 = Picamera2()
preview_config = picam2.create_preview_configuration(main={"size": (800, 600)})
picam2.configure(preview_config)

#gets the current date and time to name the picture taken
now = datetime.now()
dt_string = now.strftime("%d_%m_%Y_%H.%M.%S")

picam2.start_preview(Preview.QTGL)

picam2.start()
time.sleep(2)

metadata = picam2.capture_file('/home/hairpi/HogJuice/images' + dt_string + '.jpg')
print(metadata)

picam2.close()


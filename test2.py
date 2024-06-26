import cv2
import numpy as np
import time
from picamera2 import Picamera2, Preview, MappedArray
from PIL import Image

picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (1920,1080)}, lores={"size": (640,480)}, display="lores")
picam2.configure(camera_config)

def apply_timestamp(request):
    ts = time.strftime("%A,%B%e,%Y %r")
    with MappedArray(request, "main") as m:
        cv2.putText(m.array, ts, (0, 30), 
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

picam2.pre_callback = apply_timestamp

picam2.start_preview(Preview.QT)
picam2.start()

def countdown(val):
    time_val = val
    colour = (0, 255, 0, 255)
    origin = (240, 320)
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 3
    thickness = 8
    overlay = np.zeros((640, 480, 4), dtype=np.uint8)
    cv2.putText(overlay, str(time_val), origin, font, scale, colour, thickness)
    picam2.set_overlay(overlay)
    time.sleep(1)
#    picam2.stop_preview()
#    picam2.start_preview(Preview.QTGL)

for time_left in range(5, 0, -1):
	countdown(time_left)

picam2.capture_file('/home/hairpi/Desktop/test.jpg')
picam2.stop_preview()
picam2.stop()
time.sleep(0.5)
img = Image.open('/home/hairpi/Desktop/test.jpg')
img.show()

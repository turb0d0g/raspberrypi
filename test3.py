from picamera2 import PiCamera2, Color
from time import sleep
from datetime import datetime as dt

with PiCamera2() as camera:

    camera.rotation = 180 # omit or use 90, 180, 270 depending on setup
    camera.annotate_background = Color("black")
    camera.annotate_text = 'Hello world!'
    start = dt.now()
    camera.start_preview()
    camera.start_recording("video.h264")

    while (dt.now() - start).seconds < 10: # records video for 10 seconds
        camera.annotate_text = dt.now().strftime("%H:%M:%S %D")
        camera.wait_recording(0.2)
    camera.stop_recording()

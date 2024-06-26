import time
import numpy as np
from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput

picam2 = Picamera2()

width, height = 1280, 960
# width, height = 640, 480

video_config = picam2.create_video_configuration({"size": (width, height)})
picam2.configure(video_config)

picam2.start_preview(Preview.DRM, width=width, height=height)
picam2.start()

buffer = np.zeros((height, width, 4), dtype=np.int8)

encoder = H264Encoder(bitrate=1000000, repeat=True, iperiod=15)
output_stream = FfmpegOutput(" -an -f rtsp rtsp://localhost:8554/mystream")
output_file = FfmpegOutput("pi2cam.mp4")
picam2.start_recording(encoder, output=[output_stream, output_file])

try:
    while 1:
        time.sleep(0.5)

        # update buffer
        
        picam2.set_overlay(buffer)

except KeyboardInterrupt:
    print("Key exit")

picam2.stop_recording()

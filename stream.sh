#!/bin/bash
libcamera-vid -t 0 --width 1920 --height 1080 --nopreview --exposure long \
 --sharpness 1.2 --contrast 1.4 --brightness 0.2 --saturation 1.0 --awb auto --denoise auto \
--rotation 0 --codec libav --libav-format flv -n --framerate 30 -b 3200000 --autofocus-mode auto \
 --inline -o "rtmp://127.0.0.1/hairpi/test"

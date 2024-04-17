#!/usr/bin/python
# Naturebytes Wildlife Cam Kit | V1.01
# Based on the excellent official Raspberry Pi tutorials and a little extra from Naturebytes

from gpiozero import DigitalInputDevice
from picamera2 import Picamera2
from datetime import datetime
from signal import pause
import sys
import subprocess
import time
import logging

SENSOR_PIN = 17
LOW_BATTERY_PIN = 27

PHOTO_DIR = "/home/pi/Naturebytes/images"
NUM_PHOTOS = 5
# It takes approximately 1s to take a picture and write it to a file so actually no need to wait
DELAY_BETWEEN_PHOTOS = 0
LATITUDE_REF = "N"
LATITUDE_TUPLE = "51/1 5/1 37463/1000"
LONGITUDE_REF = "W"
LONGITUDE_TUPLE = "0/1 43/1 57185/1000"


def pir_trigger():
    logger.info("PIR Trigger!")
    # Take a number of photos to ensure we capture the subject
    for i in range(NUM_PHOTOS):
        takePhoto()
        time.sleep(DELAY_BETWEEN_PHOTOS)


def low_battery():
    logger.warn("** Low battery warning! Powering off... **")
    subprocess.run(["sudo", "poweroff"])
    sys.exit()


def takePhoto():
    now = datetime.utcnow() # Get the time now
    filename_datetime = now.strftime("%Y-%m-%d_%H-%M-%S-%f")
    exif_datetime = now.strftime("%Y:%m:%d %H:%M:%S")

    photo_filename = PHOTO_DIR + "/nbimg_" + filename_datetime + ".jpg"

    logger.info("About to take a photo, filename='%s'", photo_filename)
    picam2.capture_file(photo_filename)
    logger.info("Photo '%s' taken successfully, updating EXIF metadata...", photo_filename)

    # Add EXIF metadata (image date/time, GPS location)
    subprocess.run(["exiv2",
        "-Mset Exif.Image.DateTime " + exif_datetime, "-Mset Exif.Image.DateTimeOriginal " + exif_datetime,
        "-Mset Exif.GPSInfo.GPSVersionID 2 3 0 0",
        "-Mset Exif.GPSInfo.GPSLatitudeRef " + LATITUDE_REF, "-Mset Exif.GPSInfo.GPSLatitude " + LATITUDE_TUPLE,
        "-Mset Exif.GPSInfo.GPSLongitudeRef " + LONGITUDE_REF, "-Mset Exif.GPSInfo.GPSLongitude " + LONGITUDE_TUPLE,
        photo_filename])
    logger.info("EXIF metadata updated for photo '%s'", photo_filename)


def main():
    logging.basicConfig(format="%(levelname)s - %(asctime)s - %(name)s - %(message)s", filename="naturebytes_camera_log", level=logging.DEBUG)
    global logger
    logger = logging.getLogger(__name__)

    logger.info("Setting up PIR and low battery input GPIOs...")
    pir_input = DigitalInputDevice(SENSOR_PIN, pull_up=False)
    pir_input.when_activated = pir_trigger
    lowbatt_input = DigitalInputDevice(LOW_BATTERY_PIN, pull_up=None, active_state=True)
    lowbatt_input.when_deactivated = low_battery

    logger.info("Starting Picamera2...")
    global picam2
    picam2 = Picamera2()
    still_config = picam2.create_still_configuration()
    picam2.configure(still_config)
    picam2.start()

    logger.info("Naturebytes Wildlife Cam Kit started up successfully, waiting for events...")

    # Now wait for events...
    pause()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting")
    picam2.stop()
    sys.exit()


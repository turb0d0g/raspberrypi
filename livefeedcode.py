from picamera2 import Picamera2
import cv2
import time

def img_capt():
    Flag=False
    
    #initializing picam
    piCam=Picamera2()
    piCam.preview_configuration.main.size=(1280,720)
    #640,360
    #1280,720
    piCam.preview_configuration.main.format="RGB888"
    piCam.preview_configuration.align()
    piCam.configure("preview")
    piCam.start()
    
    #capturing and saving the image
    while True:
        frame=piCam.capture_array()
        cv2.imshow("Livefeed",frame)
        if cv2.waitKey(1)==ord('q'):
            img=frame
            Flag=True
            cv2.imwrite("Livefeed.jpg",img)
            del piCam
            break
    cv2.destroyAllWindows()
    
    #returning img if captured else 0
    if Flag:
        return img, "Image is Captured", 1
    else:
        return 0, "Error101\nImage was not captured",0


img_capt()

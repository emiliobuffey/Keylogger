import cv2
from cv2 import CAP_PROP_SETTINGS

def TakePicture():
    cam_port = 0  # camera 0 is laptop camera
    ramp_frames = 1  # 1 frame pause before taking picture to adjust
    camera = cv2.VideoCapture(cam_port, cv2.CAP_DSHOW)  # establish camera

    #capture a single image
    def get_image():
        retval, im = camera.read()
        return im

    for i in range(ramp_frames):
        temp = get_image()
    print("Capturing Face...")

    #Takes the picture
    camera_capture = get_image()
    File = "myscreenshot.png"
    cv2.imwrite(File, camera_capture)

    #release camera object
    del camera
    print("Screenshot taken!")
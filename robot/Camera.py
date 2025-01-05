import subprocess
import os

class Camera(object):
    def __init__(self, device_id=0):
        self.device_id = device_id
        self.process = None
    def CaptureImg(self, img_path):
        # 拍照
        self.process = subprocess.Popen(
            "fswebcam -r 1280x720 --no-banner " + img_path, shell=True
        )
        self.process.wait()
        













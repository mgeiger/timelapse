import picamera


class Camera():
    def __init__(self):
        self.camera = picamera.PiCamera()
        self.camera.resolution = (1280, 720)

    def capture(self, file_name):
        self.camera.capture(file_name)

import picamera
import datetime as dt

time_format = '%Y-%m-%d %H:%M:%S'

camera = picamera.PiCamera(resolution=(1280, 720), framerate=24)
camera.start_preview()
camera.annotate_background = picamera.Color('black')
camera.annotate_text = dt.datetime.now().strftime(time_format)
camera.start_recording('timestampd.h264')
start = dt.datetime.now()
while (dt.datetime.now() - start).seconds < 30:
    camera.annotate_text = dt.datetime.now().strftime(time_format)
    camera.wait_recording(0.2)
camera.stop_recording()

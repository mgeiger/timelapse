from twisted.internet import task
from twisted.internet import reactor
from datetime import datetime

camera_timeout = 1.0
system_timeout = (24.0 * 60.0 * 60.0)

prior_camera = datetime.now()

def capture_camera():
    print('{}: camera'.format(datetime.now()))
    print('{}'.format(datetime.now() - prior_camera))
    prior_camera = datetime.now()

def do_video():
    print('{}: video'.format(datetime.now()))

loop_camera = task.LoopingCall(do_camera)
loop_camera.start(camera_timeout)
loop_video = task.LoopingCall(do_video)
loop_video.start(system_timeout)

reactor.run()

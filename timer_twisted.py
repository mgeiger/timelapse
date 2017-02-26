from twisted.internet import task
from twisted.internet import reactor
from datetime import datetime, date, timedelta
import logging
from astral import Location
import pytz
import os
from subprocess import call


# Folder Locations
base_dir = '/opt/camera'
img_dir = os.path.join(base_dir, 'img')
vid_dir = os.path.join(base_dir, 'vid')

# Interval time for trying the camera
camera_timeout = 60.0

# Location information
latitude = 42.288611
longitude = -71.445

logging.basicConfig(format='%(asctime)s : %(message)s', 
        datefmt='%Y-%m-%d %H:%M:%S', 
        level=logging.INFO)


class TimeLapseCamera():
    def __init__(self):
        pass

    def take_picture(self):
        pass

    def store_picture(self):
        pass

    def close(self):
        pass
    


def sun_up():
    """
    Determines if the sun is up right now.
    """
    loc = Location(('Framingham, MA', 'USA', latitude, longitude, 'US/Eastern', 0))
    sunrise = loc.sunrise()
    sunset = loc.sunset()
    now = datetime.now(pytz.timezone('US/Eastern'))
    return sunset > now > sunrise

def capture_camera():
    """
    This will store the file name into today's directory.
    """
    logging.info('Capturing camera. Insert Raspistill here.')
    prog = '/usr/bin/raspistill'
    today = date.today()
    img_today_dir = os.path.join(img_dir, 
            str(today.year), 
            str(today.month).zfill(2), 
            str(today.day).zfill(2))
    # Check if today's directory exists
    if not os.path.exists(img_today_dir):
        os.makedirs(img_today_dir)
    time_str = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    output = '{}.jpg'.format(time_str)
    full_output = os.path.join(img_today_dir, output)
    call_list = [prog, '--height', '720', '--width', '1280', '--output', full_output]
    call(call_list)

def is_one_am():
    """
    Determines if we are between 01:00 and 01:01
    """
    today = date.today()
    today_one_am = datetime(year=today.year, month=today.month, 
            day=today.day, hour=1)
    above_one = datetime.now() >= today_one_am
    less_one = (today_one_am + timedelta(days=1)) > datetime.now()
    return above_one and less_one 

def make_video():
    logging.info('Generating video.')
    # Figure out yesterday's video path
    yesterday = date.today() - timedelta(days=1)
    img_yesterday_dir = os.path.join(img_dir, 
            str(yesterday.year), 
            str(yesterday.month).zfill(2), 
            str(yesterday.day).zfill(2))
    # Need to find all of the *.jpg images in the directory
    # Need to make a soft link for all of them
    # Now turn these files into something
    app = '/usr/bin/avconv'
    call_list = [app, '-r', '24', '-i', '%05.jpg', 
            '-codec:v', 'libx264', '-bf', '2', '-flags', '+cgop',
            '-crf', '21']

def upload_youtube():
    logging.error('Not implemented.')
    logging.info('Uploading to Youtube.')

def timelapse_arbiter():
    logging.info('Running timelapse arbiter')
    if sun_up():
        logging.info('Sun is up. Capturing image.')
        capture_camera()
    if is_one_am():
        logging.info('Making video and uploading.')
        make_video()
        upload_youtube()

logging.info('Starting logging timer.')
loop_camera = task.LoopingCall(timelapse_arbiter)
loop_camera.start(camera_timeout)

reactor.run()

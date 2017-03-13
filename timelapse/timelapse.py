#!/usr/bin/python
# -*- coding: utf-8 -*-

import glob
import logging
import os
import pytz
import sys
from socket import gethostname
from astral import Location
from datetime import datetime, date, timedelta
from subprocess import call
from twisted.internet import reactor
from twisted.internet import task

__author__ = "Matthew J. Geiger"
__copyright__ = "Matthew J. Geiger"
__license__ = "none"
__version__ = '0.0.1'

# Folder Locations
base_dir = '/opt/camera'
img_dir = os.path.join(base_dir, 'img')
vid_dir = os.path.join(base_dir, 'vid')

# Interval time for trying the camera
camera_timeout = 60.0

# Logging Options
_logger = logging.getLogger(__name__)
logformat = "[%(asctime)s] %(levelname)s:%(name)s: %(message)s"
logging.basicConfig(format=logformat,
        datefmt='%Y-%m-%d %H:%M:%S', 
        level=logging.DEBUG)


class Sun(object):

    @staticmethod
    def sun_up():
        """
        Determines if the sun is up right now.
        """
        # Location information
        latitude = 42.288611
        longitude = -71.445
        city = 'Framingham, MA'
        country = 'USA'
        tz = 'US/Eastern'
        loc = Location((city, country, latitude, longitude, tz, 0))
        sunrise = loc.sunrise()
        sunset = loc.sunset()
        now = datetime.now(pytz.timezone(tz))
        return sunset > now > sunrise

def capture_camera():
    """
    This will store the file name into today's directory.
    """
    logging.info('Capturing camera.')
    prog = '/usr/bin/raspistill'
    today = date.today()
    img_today_dir = os.path.join(img_dir, 
            str(today.year), 
            str(today.month).zfill(2), 
            str(today.day).zfill(2))
    # Check if today's directory exists
    if not os.path.exists(img_today_dir):
        os.makedirs(img_today_dir)
    time_str = datetime.now().strftime('%Y-%m-%dT%H:%M')
    output = '{}.jpg'.format(time_str)
    full_output = os.path.join(img_today_dir, output)
    call_list = [prog, '--height', '720', '--width', '1280', '--output', full_output]
    call(call_list)
    
    # Add in a timestamp
    conv = '/usr/bin/convert'
    conv_call = [conv, full_output, '-pointsize', '20', 
            '-gravity', 'SouthWest', '-stroke', '#000C', 
            '-strokewidth', '2', '-annotate', '+10+10', 
            time_str, '-stroke', 'none', '-fill', 'white', 
            '-annotate', '+10+10', time_str, full_output]
    call(conv_call)

def is_one_am():
    """
    Determines if we are between 01:00 and 01:01
    """
    today = date.today()
    today_one_am = datetime(year=today.year, month=today.month, 
            day=today.day, hour=1)
    above_one = datetime.now() >= today_one_am
    less_one = (today_one_am + timedelta(minutes=1)) > datetime.now()
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
    jpg_list = glob.glob(os.path.join(img_yesterday_dir, "*.jpg"))
    jpg_list.sort(key=lambda x: os.path.getmtime(x))

    # Need to make a soft link for all of them
    counter = 0
    for f in jpg_list:
        os.symlink(f, os.path.join(img_yesterday_dir, '{:05}.jpg'.format(counter)))
        counter += 1

    # Now turn these files into something
    video_filename = os.path.join(vid_dir, '{}-{}-{}.avi'.format(str(yesterday.year),
        str(yesterday.month).zfill(2), str(yesterday.day).zfill(2)))
    app = '/usr/bin/avconv'
    call_list = [app, '-r', '24', 
            '-i', os.path.join(img_yesterday_dir, '%05.jpg'), 
            '-codec:v', 'libx264', 
            '-bf', '2', 
            '-flags', '+cgop',
            '-crf', '21',
            '-g', '12',
            video_filename]
    logging.debug('Converting a video named {}.'.format(video_filename))
    call(call_list)

    # Now delete all these files
    logging.error('Deleting files is not yet implemented. Please do this manually.')

def upload_youtube():
    _logger.error('Youtube Upload is not implemented at this time.')
    _logger.info('Uploading to Youtube.')

def timelapse_arbiter():
    _logger.info('Running timelapse arbiter')
    # Want to ensure we are on the raspberry pi camera.
    if gethostname() == 'camera':
        # Check if the sun is up
        if Sun().sun_up():
            _logger.info('Sun is up. Capturing image.')
            capture_camera()
        else:
            _logger.info('Sun is not up.')
        # Check if we are in the first minute of 1am
        if is_one_am():
            _logger.info('Making video and uploading.')
            make_video()
            upload_youtube()
    else:
        _logger.info('My hostname is not camera. Leaving this arbiter.')
        pass

def main():
    """Main entry point allowing external calls
    """

    _logger.debug("Starting timelapse camera.")
    loop_camera = task.LoopingCall(timelapse_arbiter)
    loop_camera.start(camera_timeout)

    reactor.run()

if __name__ == "__main__":
    main()


#!/usr/bin/python
# -*- coding: utf-8 -*-
from twisted.internet import task
from twisted.internet import reactor
from datetime import datetime, date, timedelta
import logging
from astral import Location
import pytz
import os
from subprocess import call
import glob

__author__ = "Matthew J. Geiger"
__copyright__ = "Matthew J. Geiger"
__license__ = "none"

# Folder Locations
base_dir = '/opt/camera'
img_dir = os.path.join(base_dir, 'img')
vid_dir = os.path.join(base_dir, 'vid')

# Interval time for trying the camera
camera_timeout = 60.0

# Logging Options
_logger = logging.getLogger(__name__)
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
    

class Sun(object):
    # Location information
    latitude = 42.288611
    longitude = -71.445
    city = 'Framingham, MA'
    country = 'USA'
    tz = 'US/Eastern'

    @staticmethod
    def sun_up():
        """
        Determines if the sun is up right now.
        """
        loc = Location((self.city, self.country, self.latitude, self.longitude, self.tz, 0))
        sunrise = loc.sunrise()
        sunset = loc.sunset()
        now = datetime.now(pytz.timezone(self.tz))
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
    app = '/usr/bin/avconv'
    call_list = [app, '-r', '24', 
            '-i', os.path.join(img_yesterday_dir, '%05.jpg'), 
            '-codec:v', 'libx264', 
            '-bf', '2', 
            '-flags', '+cgop',
            '-crf', '21']

def upload_youtube():
    logging.error('Not implemented.')
    logging.info('Uploading to Youtube.')

def timelapse_arbiter():
    logging.info('Running timelapse arbiter')
    if Sun().sun_up():
        logging.info('Sun is up. Capturing image.')
        capture_camera()
    if is_one_am():
        logging.info('Making video and uploading.')
        make_video()
        upload_youtube()

def parse_args(args):
    """Parse command line parameters

    Args:
        args ([str]): command line parameters as list of strings

    Returns:
        :obj:`argparse.Namespace`: command line paramters namespace
    """
    parser = argparser.ArgumentParser(
            description="Backyard Raspberry Pi Timelapse Camera")
    parser.add_argument(
            '--version',
            action='version',
            version='timelapse {ver}'.format(ver=__version__))
    parser.add_argument(
            '-c',
            '--capture',
            help="The timelapse capture duration in seconds.",
            type=int,
            action='store_const',
            const=60)
    parser.add_argument(
            '-s',
            '--storage',
            help="The default storage directory for images.",
            type=str)
    parser.add_argument(
            '-vv',
            '--very-verbose',
            dest="loglevel",
            help="Set LogLevel to DEBUG",
            action='store_const',
            const=logging.DEBUG)
    return parser.parse_args(args)

def setup_logging(loglevel):
    """Setup basic logging

    Args:
        loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
            format=logformat, datefmt="%Y-%m-%d %H:%M:%S")

def main(args):
    """Main entry point allowing external calls

    Args:
        args ([str]): command line parameter list
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug("Starting timelapse camera...")

    logging.info('Starting logging timer.')
    loop_camera = task.LoopingCall(timelapse_arbiter)
    loop_camera.start(camera_timeout)

    reactor.run()

def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])

if __name__ == "__main__":
    run()


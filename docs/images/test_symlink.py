import os
import glob

base_dir = '/home/mgeiger/Projects/timelapse/images'
date = '2017-02-10'

date_dir = os.path.join(base_dir, date)
jpg_files = glob.glob(os.path.join(date_dir, '*.jpg'))
jpg_files.sort(key=lambda x: os.path.getmtime(x))
counter = 0
for f in jpg_files:
    os.symlink(f, os.path.join(date_dir, '{:05}.jpg'.format(counter)))
    counter += 1

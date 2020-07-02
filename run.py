import os
import time
import datetime
import glob

# Script
script = os.path.basename(__file__)

# Set Datetime to File
def setTime(filepath):
    date = datetime.datetime.now()
    modTime = time.mktime(date.timetuple())
    os.utime(filepath, (modTime, modTime))

# Main Process
for f in sorted(glob.iglob('**/*', recursive=True)):
    if f.startswith('venv') == False and f != script:
        fpath = os.path.realpath(f)
        setTime(fpath)

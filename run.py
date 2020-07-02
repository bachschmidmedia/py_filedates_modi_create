import os
import platform
import time
import datetime
import glob
from win32_setctime import setctime
import PySimpleGUI as sg

# Script
script = os.path.basename(__file__)
date = datetime.datetime.now()
date_str = date.strftime('%m/%d/%Y %H:%M:%S')
modTime = time.mktime(date.timetuple())
user_os = platform.system()
list = []

# Set Modification-Datetime to File
def setModificationTime(filepath):
    os.utime(filepath, (modTime, modTime))

# Set Creation-Datetime to File
def setCreationTime(filepath):
    # format filepath
    new_filepath = '"{}"'.format(filepath.replace('\"', '\\"'))

    if user_os == 'Windows':
        # Set on Windows
        setctime(filepath, modTime)
    elif user_os == 'Darwin':
        # Set on Mac
        os.system('SetFile -d "{}" {}'.format(date_str, new_filepath))

def set_list():
    for f in sorted(glob.iglob('**/*', recursive=True)):
        if f.startswith(('venv', '.git')) == False and f != script:
            fpath = os.path.realpath(f)
            list.append(fpath)

# Set The Dates
def set_dates():

    setModificationTime(fpath)
    setCreationTime(fpath)

    print('Set the Date on: {}'.format(fpath))

# Main Process
def runMain():
    # Set List
    set_list()

    # SG Theme
    sg.theme('DarkAmber')  # Add a touch of color

    # All the stuff inside your window.
    layout = [
        [sg.Text('Aenderungs- und Erstelldatum anpassen')],
        [sg.Button('Dateien suchen'), sg.Button('Cancel')],
        [sg.InputText('Wähle den Ordner'), sg.FolderBrowse('Ordner auswählen')]
    ]

    # Create the Window
    window = sg.Window('Window Title', layout)

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
            break
        print('You entered ', values[0])

    window.close()

    # print('main')
    # set_dates()
    # print('second')

if __name__ == "__main__":
    runMain()

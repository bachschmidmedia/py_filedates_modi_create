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
my_list = []
l_count = 0


# Set Modification-Datetime to File
def set_modification_time(filepath):
    os.utime(filepath, (modTime, modTime))


# Set Creation-Datetime to File
def set_creation_time(filepath):
    # format filepath
    new_filepath = '"{}"'.format(filepath.replace('\"', '\\"'))

    if user_os == 'Windows':
        # Set on Windows
        setctime(filepath, modTime)
    elif user_os == 'Darwin':
        # Set on Mac
        os.system('SetFile -d "{}" {}'.format(date_str, new_filepath))


def set_list(start='', recursive=True):
    global my_list
    my_list = []

    if recursive:
        basepath = '{}/**/*'
    else:
        basepath = '{}/*'

    for f in sorted(glob.iglob(basepath.format(start), recursive=True)):
        if f.startswith(('venv', '.git')) == False and f != script:
            fpath = os.path.realpath(f)
            if os.path.isfile(fpath):
                my_list.append(fpath)


def get_list():
    return my_list


# Set The Dates
def set_file_dates():
    res = []
    for f in get_list():
        set_modification_time(f)
        set_creation_time(f)
        res.append('Datum verändert für: {}'.format(f))
    return res


# Main Process
def runMain():
    s_update_files = 'Dateien (Datum) anpassen'
    global l_count

    # SG Theme
    sg.theme('LightBlue2')  # Add a touch of color


    # All the stuff inside your window.

    layout = [
        [sg.Text('Änderungsdatum und Erstelldatum von Dateien anpassen')],
        [sg.Text('Bitte wählen Sie den Ordner aus:')],
        [sg.Checkbox('Unterordner mit einbeziehen?', key='recursive')],
        [sg.FolderBrowse('Ordner auswählen', key='folder_browser'), sg.InputText()],
        [sg.Submit('Scan starten', key='scan'), sg.Submit(s_update_files, key='try_update_files', disabled=True)],
        [sg.Listbox(values=get_list(), bind_return_key=False, size=(100, 10), key='list_box')],
        [sg.MLine(key='subinfo')],
        [sg.Cancel('Schließen', key='close')]
    ]

    # Create the Window
    window = sg.Window('Datei-Daten anpassen', layout).Finalize()

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        close_app = False
        event, values = window.read()

        # On Scanning
        if event == 'scan':
            print('Scan! Event:', event)

            path = values['folder_browser']
            set_list(path, recursive=values['recursive'])

            l_count = len(get_list())

            window.FindElement('list_box').Update(
                values=get_list()
            )
            window.FindElement('try_update_files').Update(
                disabled=l_count <= 0,
                text="{} {}".format(l_count, s_update_files)
            )
            window.FindElement('subinfo').Update(
                'Insgesamt "{}" Dateien wurden gefunden!'.format(l_count)
            )
            window.Finalize()

        # On Modify Dates
        if event == 'try_update_files':
            update_files = sg.PopupYesNo(
                'Dateien anpassen?', 'Möchten Sie die Dateien anpassen?',
                line_width=200,
                keep_on_top=True
            )

            if update_files == 'Yes':
                changes = set_file_dates()

                succ_text = '\r\nERFOLG!!!\r\n\r\n {} Dateien erfolgreich verändert!\r\n\r\n'.format(l_count)
                succ_changes = '\r\n => '.join(changes)

                close_app = sg.PopupScrolled(succ_text + succ_changes + succ_text)

        if event == sg.WIN_CLOSED or event == 'close' or close_app:  # if user closes window or clicks cancel
            break

    window.close()

    # print('main')
    # print('second')


if __name__ == "__main__":
    runMain()

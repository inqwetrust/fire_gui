import traceback
import datetime
import ctypes
from firebase import firebase
import os.path
import sys
import socket
import pyautogui
# Code to check if left or right mouse buttons were pressed
import win32api
import time
import win32gui
import pyperclip
from random import randint

start_time = datetime.datetime.now()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = s.getsockname()[0]
ip_prefix = '_'.join(ip.split('.')[:3])
s.close()

filename = 'firebase_database_url.txt'
if os.path.isfile(filename):
    f = open(filename, "r")
else:
    open(filename, 'a').close()
firebase = firebase.FirebaseApplication(f.read(), None)

# firebase.put(url='/ip/{}'.format(ip).replace('.', '_'),name='click', data=data)
# result = firebase.get('/ip/{}'.format(ip).replace('.', '_'),name='click')

firebase.put(url='/ip/{}'.format(ip).replace('.', '_'),name='click', data='')


def monitor():
    result = firebase.get('/ip/{}'.format(ip).replace('.', '_'), name='click')
    wait_time = 0.2
    while True:
        result_current = firebase.get('/ip/{}'.format(ip).replace('.', '_'), name='click')
        if result != result_current:
            print(result_current)
            if "state" in result_current:
                if result_current['state'] == "Left":
                    pyautogui.click((int(result_current['x']), int(result_current['y'])))
                    firebase.put(url='/ip/{}'.format(ip).replace('.', '_'), name='click', data='')
                elif result_current['state'] == "Right":
                    pyautogui.rightClick((int(result_current['x']), int(result_current['y'])))
                    firebase.put(url='/ip/{}'.format(ip).replace('.', '_'), name='click', data='')
                elif result_current['state'] == "Move":
                    pyautogui.moveTo((int(result_current['x']), int(result_current['y'])))
                    pyperclip.copy(result_current['text_copy'])
                    firebase.put(url='/ip/{}'.format(ip).replace('.', '_'), name='click', data='')
                result = result_current
                # print(result)
                wait_time = 0.1
        elif wait_time >= 54:
            firebase.put(url='/ip/{}'.format(ip).replace('.', '_'), name='drive_count', data='{}'.format(get_drive_count()))
            wait_time = 30
            pass
        else:
            wait_time *= 1.1
            wait_time = max(min(wait_time, 65), 0.1)
        time.sleep(wait_time)


def broadcast():
    move_time = datetime.datetime.now()
    position_last = (0, 0)
    state_left = win32api.GetKeyState(0x01)  # Left button down = 0 or 1. Button up = -127 or -128
    state_right = win32api.GetKeyState(0x02)  # Right button down = 0 or 1. Button up = -127 or -128
    scroll_last_state = None
    num_last_state = None
    scroll_last_state = get_scrolllock_state()
    num_last_state = get_numlock_state()

    while True:
        on_duration = datetime.datetime.now() - start_time
        on_duration = on_duration.total_seconds()
        if on_duration > 3600:
            print("Restart again")
            time.sleep(3600000)
            exit()
        a = win32api.GetKeyState(0x01)
        b = win32api.GetKeyState(0x02)

        if scroll_last_state != get_scrolllock_state() and scroll_last_state != None and get_caplock_state() == False:  # Button state changed
        # if a != state_left and get_scrolllock_state():  # old Button state changed
            move_time = datetime.datetime.now()
            state_left = a
            # print(a)
            if a < 0 or True:
                # print('Left Button Pressed')
                flags, hcursor, (x, y) = win32gui.GetCursorInfo()
                data = {'x': x + randint(-1, 1), 'y': y + randint(-1, 1), 'state': 'Left', 'text_copy': "1"}
                result = firebase.get('/ip/', name=None)
                for k, v in result.items():
                    if ip_prefix in k:
                        firebase.put(url='/ip/{}'.format(k), name='click', data=data)
                result_len = ' '
                while True:
                    result = firebase.get('/ip/', name=None)
                    for k, v in result.items():
                        if len(v['click']) == 0:
                            result_len = ''
                            time.sleep(0.1)
                            print('ready after left click')
                            scroll_last_state = get_scrolllock_state()
                            num_last_state = get_numlock_state()
                            break
                    if len(result_len) == 0:
                        break
                    time.sleep(0.1)
            else:
                # print('Left Button Released')
                pass

        elif num_last_state != get_numlock_state() and num_last_state != None and get_caplock_state() == False:  # Button state changed
        # elif b != state_right and get_scrolllock_state():  # Button state changed
            move_time = datetime.datetime.now()
            state_right = b
            # print(b)
            if b < 0 or True:
                # print('Right Button Pressed')
                flags, hcursor, (x, y) = win32gui.GetCursorInfo()
                data = {'x': x + randint(-1, 1), 'y': y + randint(-1, 1), 'state': 'Right', 'text_copy': "0"}
                result = firebase.get('/ip/', name=None)
                for k, v in result.items():
                    if ip_prefix in k:
                        firebase.put(url='/ip/{}'.format(k), name='click', data=data)
                result_len = ' '
                while True:
                    result = firebase.get('/ip/', name=None)
                    for k, v in result.items():
                        if len(v['click']) == 0:
                            result_len = ''
                            time.sleep(0.1)
                            print('ready after right click')
                            scroll_last_state = get_scrolllock_state()
                            num_last_state = get_numlock_state()
                            break
                    if len(result_len) == 0:
                        break
                    time.sleep(0.1)
            else:
                # print('Right Button Released')
                pass
        elif get_caplock_state() and get_numlock_state() == False and get_scrolllock_state() == False:
            f = open('text_list.txt','r')
            text_list = [t.replace("\n", "") for t in f.readlines()]
            text_list = text_list * 200
            f.close()
            if move_time < (datetime.datetime.now() - datetime.timedelta(seconds=3)):
                flags, hcursor, (x, y) = win32gui.GetCursorInfo()
                if (x, y) != position_last:
                    data = [{'x': x, 'y': y, 'state': 'Move', 'text_copy': t} for t in text_list]
                    result = firebase.get('/ip/', name=None)
                    ix = 0
                    for k, v in result.items():
                        firebase.put(url='/ip/{}'.format(k), name='click', data=data[ix])
                        ix += 1
                    move_time = datetime.datetime.now()
                    position_last = (x, y)
            elif (datetime.datetime.now() - move_time).total_seconds() % 5 == 0:
                result = firebase.get('/ip/', name=None)
                for k, v in result.items():
                    if ip_prefix in k:
                        if 'drive_count' in v:
                            if int(v['drive_count']) < 4:
                                print('ERROR: ip {} drive_count {} RE-MAP DRIVE'.format(k, v['drive_count']))
        time.sleep(0.1)


def get_numlock_state():
    hllDll = ctypes.WinDLL("User32.dll")
    VK_CAPITAL = 0x90
    return hllDll.GetKeyState(VK_CAPITAL)


def get_caplock_state():
    hllDll = ctypes.WinDLL("User32.dll")
    VK_CAPITAL = 0x14
    return hllDll.GetKeyState(VK_CAPITAL)


def get_scrolllock_state():
    hllDll = ctypes.WinDLL("User32.dll")
    VK_CAPITAL = 0x91
    return hllDll.GetKeyState(VK_CAPITAL)


def get_drive_count():
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    return len(drives)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        while True:
            try:
                monitor()
            except:
                print(traceback.format_exc())
    elif sys.argv[1] == "control":
        while True:
            try:
                broadcast()
            except:
                print(traceback.format_exc())

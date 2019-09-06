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


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = s.getsockname()[0]
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
                    firebase.put(url='/ip/{}'.format(ip).replace('.', '_'), name='click', data='')
                result = result_current
                # print(result)
        time.sleep(0.2)


def broadcast():
    move_time = datetime.datetime.now()
    position_last = (0, 0)
    state_left = win32api.GetKeyState(0x01)  # Left button down = 0 or 1. Button up = -127 or -128
    state_right = win32api.GetKeyState(0x02)  # Right button down = 0 or 1. Button up = -127 or -128
    scroll_last_state = None
    num_last_state = None
    while True:
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
                data = {'x': x, 'y': y, 'state': 'Left'}
                result = firebase.get('/ip/', name=None)
                for k, v in result.items():
                    firebase.put(url='/ip/{}'.format(k), name='click', data=data)
                result_len = ' '
                while True:
                    result = firebase.get('/ip/', name=None)
                    for k, v in result.items():
                        if len(v['click']) == 0:
                            result_len = ''
                            time.sleep(1)
                            print('ready after left click')
                            break
                    if len(result_len) == 0:
                        break
                time.sleep(0.1)
            else:
                # print('Left Button Released')
                pass

        elif num_last_state != get_scrolllock_state() and num_last_state != None and get_caplock_state() == False:  # Button state changed
        # elif b != state_right and get_scrolllock_state():  # Button state changed
            move_time = datetime.datetime.now()
            state_right = b
            # print(b)
            if b < 0 or True:
                # print('Right Button Pressed')
                flags, hcursor, (x, y) = win32gui.GetCursorInfo()
                data = {'x': x, 'y': y, 'state': 'Right'}
                result = firebase.get('/ip/', name=None)
                for k, v in result.items():
                    firebase.put(url='/ip/{}'.format(k), name='click', data=data)
                result_len = ' '
                while True:
                    result = firebase.get('/ip/', name=None)
                    for k, v in result.items():
                        if len(v['click']) == 0:
                            result_len = ''
                            time.sleep(1)
                            print('ready after right click')
                            break
                    if len(result_len) == 0:
                        break
                time.sleep(0.1)
            else:
                # print('Right Button Released')
                pass
        elif get_caplock_state():
            if move_time < (datetime.datetime.now() - datetime.timedelta(seconds=3)):
                flags, hcursor, (x, y) = win32gui.GetCursorInfo()
                if (x, y) != position_last:
                    data = {'x': x, 'y': y, 'state': 'Move'}
                    result = firebase.get('/ip/', name=None)
                    for k, v in result.items():
                        firebase.put(url='/ip/{}'.format(k), name='click', data=data)
                    move_time = datetime.datetime.now()
                    position_last = (x, y)
        time.sleep(0.001)
        scroll_last_state = get_scrolllock_state()
        num_last_state = get_numlock_state()

        # time.sleep(1)


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

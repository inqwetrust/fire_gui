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
result = firebase.get('/ip/{}'.format(ip).replace('.', '_'),name='click')
print(result)

firebase.put(url='/ip/{}'.format(ip).replace('.', '_'),name='click', data='')

def monitor():
    result = ''
    while True:
        result_current = firebase.get('/ip/{}'.format(ip).replace('.', '_'), name='click')
        if result != result_current:
            if len(result_current) > 0:
                if result_current['state'] == "Left":
                    pyautogui.click((int(result_current['x']), int(result_current['y'])))
                elif result_current['state'] == "Right":
                    pyautogui.rightClick((int(result_current['x']), int(result_current['y'])))
                elif result_current['state'] == "Move":
                    pyautogui.moveTo((int(result_current['x']), int(result_current['y'])))
            result = result_current
            time.sleep(0.2)


def broadcast():
    state_left = win32api.GetKeyState(0x01)  # Left button down = 0 or 1. Button up = -127 or -128
    state_right = win32api.GetKeyState(0x02)  # Right button down = 0 or 1. Button up = -127 or -128
    while True:
        a = win32api.GetKeyState(0x01)
        b = win32api.GetKeyState(0x02)

        if a != state_left and get_capslock_state():  # Button state changed
            state_left = a
            print(a)
            if a < 0:
                print('Left Button Pressed')
                flags, hcursor, (x, y) = win32gui.GetCursorInfo()
                data = {'x': x, 'y': y, 'state': 'Left'}
                result = firebase.get('/ip/', name=None)
                for k, v in result.items():
                    print(k)
                    firebase.put(url='/ip/{}'.format(k), name='click', data=data)
            else:
                print('Left Button Released')

        elif b != state_right and get_capslock_state():  # Button state changed
            state_right = b
            print(b)
            if b < 0:
                print('Right Button Pressed')
                flags, hcursor, (x, y) = win32gui.GetCursorInfo()
                data = {'x': x, 'y': y, 'state': 'Right'}
                result = firebase.get('/ip/', name=None)
                for k, v in result.items():
                    print(k)
                    firebase.put(url='/ip/{}'.format(k), name='click', data=data)
            else:
                print('Right Button Released')
        elif get_capslock_state():
            flags, hcursor, (x, y) = win32gui.GetCursorInfo()
            data = {'x': x, 'y': y, 'state': 'Move'}
            result = firebase.get('/ip/', name=None)
            for k, v in result.items():
                print(k)
                firebase.put(url='/ip/{}'.format(k), name='click', data=data)
            time.sleep(0.5)
        time.sleep(0.001)

        # time.sleep(1)

def get_capslock_state():
    hllDll = ctypes.WinDLL ("User32.dll")
    VK_CAPITAL = 0x91
    return hllDll.GetKeyState(VK_CAPITAL)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        monitor()
    elif sys.argv[1] == "control":
        broadcast()

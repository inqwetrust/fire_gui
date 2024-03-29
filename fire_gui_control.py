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

global start_time
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


def monitor():
    global start_time
    result = firebase.get('/ip/{}'.format(ip).replace('.', '_'), name='click')
    wait_time = 0.2
    while True:
        on_duration = datetime.datetime.now() - start_time
        on_duration = on_duration.total_seconds()
        if on_duration > 9600 and wait_time > 60:
            print("restart again")
            time.sleep(1800)
            break
        result_current = firebase.get('/ip/{}'.format(ip).replace('.', '_'), name='click')
        if result != result_current:
            # print(result_current)
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
                elif result_current['state'] == "Paste":
                    pyautogui.hotkey('ctrl', 'v')
                    firebase.put(url='/ip/{}'.format(ip).replace('.', '_'), name='click', data='')
                elif result_current['state'] == "Copy":
                    pyperclip.copy(result_current['text_copy'])
                    firebase.put(url='/ip/{}'.format(ip).replace('.', '_'), name='click', data='')
                elif result_current['state'] == "Exit":
                    print("Program Stopped")
                    firebase.put(url='/ip/{}'.format(ip).replace('.', '_'), name='click', data='')
                    time.sleep(100000)
                result = result_current
                print(result)
                wait_time = 0.1
        elif wait_time >= 54:
            print(ip, report_drive_count())
            wait_time = 30
            pass
        else:
            wait_time *= 1.3
            wait_time = max(min(wait_time, 65), 0.1)
        time.sleep(wait_time)


def broadcast():
    global start_time
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
        if on_duration > 3600 and get_caplock_state():
            pyautogui.press('capslock')
            start_time += datetime.timedelta(hours=1)
            pass
        a = win32api.GetKeyState(0x01)
        b = win32api.GetKeyState(0x02)

        if scroll_last_state != get_scrolllock_state() and scroll_last_state != None and get_caplock_state() == False:  # Button state changed
        # if a != state_left and get_scrolllock_state():  # old Button state changed
            move_time = datetime.datetime.now()
            state_left = a
            # print(a)
            if a < 0 or True:
                print('Left Button Pressed')
                flags, hcursor, (x, y) = win32gui.GetCursorInfo()
                data = {'x': x + randint(-1, 1), 'y': y + randint(-1, 1), 'state': 'Left', 'text_copy': "{}".format(randint(-1234567, -1))}
                result = firebase.get('/ip/', name=None)
                for k, v in result.items():
                    if ip_prefix in k:
                        firebase.put(url='/ip/{}'.format(k), name='click', data=data)
                result_len = ' '
                while True:
                    result = firebase.get('/ip/', name=None)
                    for k, v in result.items():
                        if ip_prefix in k:
                            if len(v['click']) == 0:
                                result_len = ''
                                time.sleep(0.1)
                                print('ready after left click')
                                break
                    if len(result_len) == 0:
                        pyautogui.press("scrolllock")
                        scroll_last_state = get_scrolllock_state()
                        num_last_state = get_numlock_state()
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
                print('Right Button Pressed')
                flags, hcursor, (x, y) = win32gui.GetCursorInfo()
                data = {'x': x + randint(-1, 1), 'y': y + randint(-1, 1), 'state': 'Right', 'text_copy': "{}".format(randint(1,12345))}
                result = firebase.get('/ip/', name=None)
                for k, v in result.items():
                    if ip_prefix in k:
                        firebase.put(url='/ip/{}'.format(k), name='click', data=data)
                result_len = ' '
                while True:
                    result = firebase.get('/ip/', name=None)
                    for k, v in result.items():
                        if ip_prefix in k:
                            if len(v['click']) == 0:
                                result_len = ''
                                time.sleep(0.1)
                                print('ready after right click')
                                break
                    if len(result_len) == 0:
                        pyautogui.press("numlock")
                        scroll_last_state = get_scrolllock_state()
                        num_last_state = get_numlock_state()
                        break
                    time.sleep(0.1)
            else:
                # print('Right Button Released')
                pass
        elif get_caplock_state() and get_numlock_state() and get_scrolllock_state() == False:
            data = {'x': randint(100, 200), 'y': randint(100, 200), 'state': 'Paste', 'text_copy': "{}".format(randint(1, 12345))}
            result = firebase.get('/ip/', name=None)
            for k, v in result.items():
                if ip_prefix in k:
                    firebase.put(url='/ip/{}'.format(k), name='click', data=data)
            result_len = ' '
            while True:
                result = firebase.get('/ip/', name=None)
                for k, v in result.items():
                    if ip_prefix in k:
                        if len(v['click']) == 0:
                            result_len = ''
                            time.sleep(0.1)
                            print('ready after Paste')
                            break
                if len(result_len) == 0:
                    pyautogui.press("numlock")
                    # pyautogui.press("scrolllock")
                    scroll_last_state = get_scrolllock_state()
                    num_last_state = get_numlock_state()
                    break
        elif get_caplock_state() and get_numlock_state() == False and get_scrolllock_state():
            f = open('text_list.txt', 'r')
            text_list = [t.replace("\n", "") for t in f.readlines()]
            text_list = text_list * 200
            f.close()
            data = [{'x': randint(100, 200), 'y': randint(100, 200), 'state': 'Copy', 'text_copy': t} for t in text_list]
            result = firebase.get('/ip/', name=None)
            ix = 0
            for k, v in result.items():
                if ip_prefix in k:
                    firebase.put(url='/ip/{}'.format(k), name='click', data=data[ix])
                    ix += 1
            result_len = ' '
            while True:
                result = firebase.get('/ip/', name=None)
                for k, v in result.items():
                    if ip_prefix in k:
                        if len(v['click']) == 0:
                            result_len = ''
                            time.sleep(0.1)
                            print('ready after Copy')
                            break
                if len(result_len) == 0:
                    # pyautogui.press("numlock")
                    pyautogui.press("scrolllock")
                    scroll_last_state = get_scrolllock_state()
                    num_last_state = get_numlock_state()
                    break
        elif get_caplock_state() and get_numlock_state() == False and get_scrolllock_state() == False:
            if move_time < (datetime.datetime.now() - datetime.timedelta(seconds=3)):
                scroll_last_state = get_scrolllock_state()
                num_last_state = get_numlock_state()
                flags, hcursor, (x, y) = win32gui.GetCursorInfo()
                if (x, y) != position_last:
                    data = {'x': x, 'y': y, 'state': 'Move', 'text_copy': "{}".format(randint(1, 1234567))}
                    result = firebase.get('/ip/', name=None)
                    for k, v in result.items():
                        if ip_prefix in k:
                            firebase.put(url='/ip/{}'.format(k), name='click', data=data)
                    move_time = datetime.datetime.now()
                    position_last = (x, y)
            pass
        time.sleep(0.1)


def report_drive_count():
    drive_count = get_drive_count()
    firebase.put(url='/ip/{}'.format(ip).replace('.', '_'), name='drive_count', data='{}'.format(drive_count))
    return drive_count


def check_drive_count():
    result = firebase.get('/ip/', name=None)
    msg_list = []
    for k, v in result.items():
        if ip_prefix in k:
            if 'drive_count' in v:
                if int(v['drive_count']) < 4:
                    msg_list.append((k, v['drive_count']))
                    pass
    return 'ERROR: ip, drive_count {} RE-MAP DRIVE'.format(msg_list)


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


def exit_all_same_subnet():
    data = {'x': 100, 'y': 100, 'state': 'Exit', 'text_copy': "{}".format(randint(1, 1234567))}
    result = firebase.get('/ip/', name=None)
    for k, v in result.items():
        if ip_prefix in k:
            firebase.put(url='/ip/{}'.format(k), name='click', data=data)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        while True:
            try:
                firebase.put(url='/ip/{}'.format(ip).replace('.', '_'), name='click', data='')
                print(ip, report_drive_count())
                monitor()
                print("exiting monitor")
                time.sleep(10000)
            except:
                print(traceback.format_exc())
                time.sleep(10)
    elif sys.argv[1] == "control":
        while True:
            try:
                print(check_drive_count())
                broadcast()
            except:
                print(traceback.format_exc())
                time.sleep(5)
    elif sys.argv[1] == "exit":
        while True:
            try:
                print("sending exit signal to all same subnet")
                exit_all_same_subnet()
                time.sleep(100000)
            except:
                print(traceback.format_exc())
                time.sleep(5)

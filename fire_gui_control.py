import time
import random
from firebase import firebase
import os.path
import sys
import socket
import pyautogui

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
    result = None
    while True:
        result_current = firebase.get('/ip/{}'.format(ip).replace('.', '_'), name='click')
        if result != result_current:
            print(result_current)
            pyautogui.moveTo((result_current['x'], result_current['y']))
            result = result_current
            time.sleep(1)


def broadcast():
    while True:
        data = {'x': random.randint(100,1000), 'y': random.randint(100,1000)}
        result = firebase.get('/ip/', name=None)
        for k, v in result.items():
            print(k)
            firebase.put(url='/ip/{}'.format(k), name='click', data=data)
        time.sleep(1)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        monitor()
    elif sys.argv[1] == "control":
        broadcast()

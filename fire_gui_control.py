from firebase import firebase
import os.path
import datetime
import socket
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

data = {'x': 200, 'y': 300}
firebase.put(url='/ip/{}'.format(ip).replace('.', '_'),name='click', data=data)
result = firebase.get('/ip/{}'.format(ip).replace('.', '_'),name='click')
print(result)

firebase.put(url='/ip/{}'.format(ip).replace('.', '_'),name='click', data='')
result = firebase.get('/ip/{}'.format(ip).replace('.', '_'),name='click')
print(result)

result = firebase.get('/ip/', name=None)
for k, v in result.items():
    print(k)
    firebase.put(url='/ip/{}'.format(k), name='click', data=data)

if __name__ == '__main__':
    pass

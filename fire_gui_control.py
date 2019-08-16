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
# firebase.delete(url='/ip/{}'.format(ip), name='2')
data = ip
firebase.put(url='/ip/{}'.format(ip).replace('.', '_'),name='1', data=data)

result = firebase.get('/',name=None)
print(result)

if __name__ == '__main__':
    pass

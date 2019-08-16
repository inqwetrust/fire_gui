from firebase import firebase
import os.path
import datetime
filename = 'firebase_database_url.txt'
if os.path.isfile(filename):
    f = open(filename, "r")
else:
    open(filename, 'a').close()
firebase = firebase.FirebaseApplication(f.read(), None)
firebase.delete(url='/test/1', name='2')
data = {'name': 'Ozgur Vatansever', 'age': 26, 'created_at': datetime.datetime.now()}
firebase.post(url='/test/1/2', data=data)
result = firebase.get('/test/', None)
print(result)

if __name__ == '__main__':
    pass

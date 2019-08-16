from firebase import firebase
import os.path
filename = 'firebase_database_url.txt'
if os.path.isfile(filename):
    f = open(filename, "r")
else:
    open(filename, 'a').close()
firebase = firebase.FirebaseApplication(f.read(), None)
result = firebase.get('/test/', None)
print(result)


from firebase import firebase
f = open("firebase_database_url.txt", "r")
firebase = firebase.FirebaseApplication(f.read(), None)
result = firebase.get('/test/', None)
print(result)


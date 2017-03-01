import pyrebase

config = {
  "apiKey": "AIzaSyBy0LRWpIWtXEZumKm8Ypv4o3my7uq5C9I",
  "authDomain": "cloudassigment2-100514985.firebaseapp.com",
  "databaseURL": "https://cloudassigment2-100514985.firebaseio.com",
  "storageBucket": "cloudassigment2-100514985.appspot.com",
  "serviceAccount": "cloudassigment2-100514985-firebase-adminsdk-da2v5-52032d2082.json"
}

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()
user = auth.sign_in_with_email_and_password("alexanderwheadon@gmail.com", "170930w")

db = firebase.database()

alex = {"userName": "awheadon", "First Name": "Alexander", "Last Name": "Wheadon",
"Email": "alexanderwheadon@gmail.com", "password": "alexwheadon"}
db.child("users").child("awheadon").set(alex, user['idToken'])

thumper = {"userName": "thumper123", "First Name": "Thumper", "Last Name": "Wheadon",
"Email": "eoshac@gmail.com", "password": "imthumper"}
db.child("users").child("thumper123").set(thumper, user['idToken'])
all_agents = db.child("users").child('').get()#.equal_to("thumper123").get()#user['idToken'])
if(all_agents.val()==None and ''!=None):
	print("Hi")
print ("all_agents: ", all_agents.val())
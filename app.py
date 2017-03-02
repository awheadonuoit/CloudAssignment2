# Created by Alexander Wheadon
# 02/21/17
# Assignment 1

from flask import Flask, render_template, redirect, \
    url_for, request, session, flash
from functools import wraps
from flask.ext.sqlalchemy import SQLAlchemy
import pyrebase


# create the application object
app = Flask(__name__)

# config firebase
config = {
        "apiKey": "AIzaSyBy0LRWpIWtXEZumKm8Ypv4o3my7uq5C9I",
        "authDomain": "cloudassigment2-100514985.firebaseapp.com",
        "databaseURL": "https://cloudassigment2-100514985.firebaseio.com",
        "storageBucket": "cloudassigment2-100514985.appspot.com",
        "serviceAccount": "cloudassigment2-100514985-firebase-adminsdk-da2v5-52032d2082.json"
    }


import os
#get configuration settings from config,py using enviroment variables
app.config.from_object(os.environ['APP_SETTINGS'])

# create the connect and authenticate firebase connection
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
userAuth = auth.sign_in_with_email_and_password("alexanderwheadon@gmail.com", "170930w")
db = firebase.database()

# method check login to prevent access to pages that require login
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        #if logged in allow user to view page
        if 'logged_in' in session:
            return f(*args, **kwargs)
        #else redirect to the login page and prompt the user to login
        else:
            flash('You need to login first.')
            return redirect(url_for('welcome'))
    return wrap

# handle login
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    # if data has been entered
    if request.method == 'POST':
        if request.form['submit'] == 'Login':
            # if user tries to login get login credentials from firebase
            user = db.child("users").child(request.form['username']).get()
            #check if username exists
            if (user.val()!=None and request.form['username']!=""):
                #check if password is correct
                if user.val()['password'] == request.form['password']:
                    #set up session varaibles
                    session['logged_in'] = True
                    session['username'] = request.form['username']
                    session['rank'] = user.val()['rank']
                    session['role'] = user.val()['role']
                    #Check if user is an istructor
                    if(user.val()['role']=="instructor"):
                        return redirect(url_for('teacher'))

                    return redirect(url_for('home'))
            #Display invalid credentials
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('signUp'))
    #Show html page for login
    return render_template('login.html', error=error)

#Allow user to sign up
@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
    error = None
    if request.method == 'POST':
        #check if username is in use
        user = db.child("users").child(request.form['username']).get()
        if user.val()==None:
            #get user credentails
            userAccount = {"userName": request.form['username'],
            "First Name": request.form['firstName'],
            "Last Name": request.form['lastName'],
            "Email": request.form['email'],
            "password": request.form['password'], "rank": "10",
            "role": "student"}
            #add user to firebase
            db.child("users").child(request.form['username']).set(userAccount, userAuth['idToken'])
            #go back to login page
            return redirect(url_for('login'))
        else:
            #display that name has been taken
            error = 'That name has already been taken'
    return render_template('signUp.html', error=error)


# controls main page for students
@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    uname=session['username']
    ranks = []
    rankCounter=10
    #loop while the rank couter is below the users rank
    while(rankCounter>=int(session["rank"])):
        #get rank name and add rank to the list of ranks
        rankName = db.child("rank").child(rankCounter).get().val()
        ranks.append(rankName)
        rankCounter-=1
    #show html page form the main page and will show list of ranks the user can access
    return render_template('index.html', ranks=ranks, uname=uname)

# controls page that show videos for the selected rank
@app.route('/<rank>', methods=['GET', 'POST'])
@login_required
def ranks(rank):
    #get all of the videos
    videoData = db.child("videos").child(rank).get().val()
    video = []
    #store videos titles in list
    for key in videoData:
        video.append(key)
    #show list of videos
    return render_template('rank.html', ranks=rank, videos=video)


@app.route('/<rank>/<vid>')
@login_required
def videos(rank, vid):
    #shows selected video to the user
    videoData = db.child("videos").child(rank).child(vid).get().val()
    vidurl = videoData['link']
    return render_template("video.html", video=vid, vidurl=vidurl, rank=rank)


#Create welcome page
@app.route('/welcome')
def welcome():
    return render_template('welcome.html') 

#Shows the main page for instructors
@app.route('/teacher', methods=['GET', 'POST'])
@login_required
def teacher():
    #only allow instructors to access this page
    if(session['role']!="instructor"):
        return redirect(url_for('home'))
    return render_template('teacher.html', uname=session['username'])

#Shows page that will allow teachers to modify students ranks
@app.route('/teacher/ranks', methods=['GET', 'POST'])
@login_required
def modifyRanks():
    #only allow instructors 
    if(session['role']!="instructor"):
        return redirect(url_for('home'))
    if request.method == 'POST':
        #get selected rank number
        selectedRank = db.child("rank").child(request.form['rank']).get().val()
        #update rank number
        db.child("users").child(request.form['username']).update({"rank":selectedRank}, userAuth['idToken'])
        flash("Rank has been updated.")
    return render_template('changeRank.html')

@app.route('/teacher/add', methods=['GET', 'POST'])
@login_required
def addMaterials():
    #only allow instructors to access this page
    if(session['role']!="instructor"):
        return redirect(url_for('home'))

    if request.method == 'POST':
        #get the video details
        vidDetails={"title": request.form['name'], "link": request.form['video']}
        #flash("Hello")
        db.child("videos").child(request.form['rank']).child(request.form['name']).set(vidDetails, userAuth['idToken'])
        #db.child("videos").child(request.form['rank']).child(request.form['name']).set(vidDetails, userAuth['idToken'])
        flash(request.form['name'])
        flash(" has been added.")
    return render_template('addMaterials.html')

@app.route('/teacher/remove', methods=['GET', 'POST'])
@login_required
def removeMaterials():
    videos = []
    #only allow instructors to access this page
    if(session['role']!="instructor"):
        return redirect(url_for('home'))

    if request.method == 'POST':
        #show the list of videos for specific rank
        if request.form['submit'] == 'show videos':
            videoData = db.child("videos").child(request.form['rank']).get().val()
            for key in videoData:
                videos.append(key)
        else:
            #delete all checked videos
            value = request.form.getlist('materials')
            for mat in value:
                db.child("videos").child(request.form['rank']).child(mat).remove(userAuth['idToken'])
            flash(value)
            flash(" deleted")

    return render_template('removeMaterials.html', videos=videos)

#Create logout transition
@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('welcome'))


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run()

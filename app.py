# Created by Alexander Wheadon
# 02/08/17
# Assignment 1

from flask import Flask, render_template, redirect, \
    url_for, request, session, flash
from functools import wraps
from flask.ext.sqlalchemy import SQLAlchemy
import pyrebase


# create the application object
app = Flask(__name__)

# config
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
# create the sqlalchemy object
firebase = pyrebase.initialize_app(config)

auth = firebase.auth()
userAuth = auth.sign_in_with_email_and_password("alexanderwheadon@gmail.com", "170930w")

db = firebase.database()
#db = SQLAlchemy(app)
# import db schema
#from models import *


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

# handel login
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    # if data has been entered
    if request.method == 'POST':
        if request.form['submit'] == 'Login':
            # if user tries to login as administrator show invalid credentials
            user = db.child("users").child(request.form['username']).get()
            if (user.val()!=None and request.form['username']!=""):
                if user.val()['password'] == request.form['password']:
                    session['logged_in'] = True
                    session['username'] = request.form['username']
                    session['rank'] = user.val()['rank']
                    session['role'] = user.val()['role']
                    print(user.val()['role'])
                    if(user.val()['role']=="instructor"):
                        return redirect(url_for('teacher'))
                    #TODO:Add teacher site
                    return redirect(url_for('home'))
                #allow user to login and create a session
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('signUp'))
    #Show html page for login
    return render_template('login.html', error=error)

@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
    error = None
    if request.method == 'POST':
        user = db.child("users").child(request.form['username']).get()
        if user.val()==None:
            userAccount = {"userName": request.form['username'],
            "First Name": request.form['firstName'],
            "Last Name": request.form['lastName'],
            "Email": request.form['email'],
            "password": request.form['password'], "rank": "10",
            "role": "student"}
            db.child("users").child(request.form['username']).set(userAccount, userAuth['idToken'])
            return redirect(url_for('login'))
        else:
            error = 'That name has already been taken'
    return render_template('signUp.html', error=error)


# controls interactions with messaging page
@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    uname=session['username']
    ranks = []#db.session.query(MessagePost).all()
    rankCounter=10
    #rankName=db.child("rank").get().val()
    #print(rankName)
    while(rankCounter>=int(session["rank"])):
        rankName = db.child("rank").child(rankCounter).get().val()
        #print(rankName)
        print(rankName)
        ranks.append(rankName)
        rankCounter-=1
    #show html page form the main page
    return render_template('index.html', ranks=ranks, uname=uname)

@app.route('/<rank>', methods=['GET', 'POST'])
@login_required
def ranks(rank):
    videoData = db.child("videos").child(rank).get().val()
    video = []
    #print(video)
    for key in videoData:
        video.append(key)
    return render_template('rank.html', ranks=rank, videos=video)


@app.route('/<rank>/<vid>')
@login_required
def videos(rank, vid):
    videoData = db.child("videos").child(rank).child(vid).get().val()
    vidurl = videoData['link']
    return render_template("video.html", video=vid, vidurl=vidurl, rank=rank)


#Create welcome page
@app.route('/welcome')
def welcome():
    return render_template('welcome.html') 


@app.route('/teacher', methods=['GET', 'POST'])
@login_required
#@teacherRequired
def teacher():
    if(session['role']!="instructor"):
        return redirect(url_for('home'))
    return render_template('teacher.html', uname=session['username'])

@app.route('/teacher/ranks', methods=['GET', 'POST'])
@login_required
def modifyRanks():
    if(session['role']!="instructor"):
        return redirect(url_for('home'))
    if request.method == 'POST':
        selectedRank = db.child("rank").child(request.form['rank']).get().val()
        print(selectedRank)
        db.child("users").child(request.form['username']).update({"rank":selectedRank}, userAuth['idToken'])
        flash("Rank has been updated.")
    return render_template('changeRank.html')

@app.route('/teacher/add', methods=['GET', 'POST'])
@login_required
def addMaterials():
    if request.method == 'POST':
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
    if request.method == 'POST':
        if request.form['submit'] == 'show videos':
            videoData = db.child("videos").child(request.form['rank']).get().val()
            for key in videoData:
                videos.append(key)
        else:
            value = request.form.getlist('materials')
            for mat in value:
                db.child("videos").child(request.form['rank']).child(mat).remove(userAuth['idToken'])
            flash(value)
            flash("deleted")

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

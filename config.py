# Created by Alexander Wheadon
# 02/08/17
# Assignment 1

import os
# default config
class BaseConfig(object):
	# debug mode disabled unless changed
	DEBUG = False
	#secret session key
	SECRET_KEY = 'b\'9;6\\xbeKt\\xdcv\\xad6\\x1b\\xd2\\x06Z?\\xe7\\x0ci\\x86\\xe7\\xfc\\x99\\x91S\''
	#Data base location as specified by enviroment variable
	#SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
	#disable alchemy track modifications to prevent warning
	#SQLALCHEMY_TRACK_MODIFICATIONS = False
	config = {
  		"apiKey": "AIzaSyBy0LRWpIWtXEZumKm8Ypv4o3my7uq5C9I",
  		"authDomain": "cloudassigment2-100514985.firebaseapp.com",
  		"databaseURL": "https://cloudassigment2-100514985.firebaseio.com",
  		"storageBucket": "cloudassigment2-100514985.appspot.com",
  		"serviceAccount": "cloudassigment2-100514985-firebase-adminsdk-da2v5-52032d2082.json"
	}
#local testing config
class DevelopmentConfig(BaseConfig):
	DEBUG = True
#heroku configuration
class ProductionConfig(BaseConfig):
	DEBUG = False

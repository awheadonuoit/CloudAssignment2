# Created by Alexander Wheadon
# 02/08/17
# Assignment 1

from app import db


class MessagePost(db.Model):
	#name sql table
    __tablename__ = "posts"
    #Create table columns
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String, nullable=False)
    message = db.Column(db.String, nullable=False)

    def __init__(self, user, message):
        self.user = user
        self.message = message

    def __repr__(self):
    	return '<user {}'.format(self.user)

# Created by Alexander Wheadon
# 02/08/17
# Assignment 1

from app import db
from models import MessagePost

# create the database and the db table
db.create_all()

# insert data
db.session.add(MessagePost("greg", "Hi all"))
db.session.add(MessagePost("alex", "Hi."))
db.session.add(MessagePost("jeff", "hi greg."))
db.session.add(MessagePost("greg", "how is everyone"))

# commit the changes
db.session.commit()

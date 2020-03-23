#~movie-bag/database/models.py
from .db import db
import datetime as dt

class User(db.Document):
    username = db.StringField(required=True, unique=True)
    email = db.StringField(required=True, unique=True)
    password = db.StringField(required=True, unique=True)
    date = db.DateTimeField(default=dt.datetime.utcnow)

class Post(db.Document):
    author = db.ReferenceField(User, required=True)
    created = db.DateTimeField(default=dt.datetime.utcnow)
    title = db.StringField(required=True, unique=True)
    body = db.StringField(required=True, unique=True)

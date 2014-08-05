"""
Author: Tomas
Date : 2014-03-02
Desc: QASystem's Database model, Use Flask-mongoengine
"""
from app import db
from flask.ext.login import UserMixin

class User(db.Document, UserMixin):
    """
    It's for user system schema, it is store in the collection named users.

    account : account Field
    pwd : Password Field
    name : Nickname Field
    email : Email Field
    get_id : return the unicode of uid
    get_user : return a user object
    """
    account = db.StringField( required=True)
    pwd = db.StringField(required=True)
    name = db.StringField()
    email = db.StringField()
    logo = db.StringField()
    old_logo = db.ListField(db.StringField())
    skills = db.StringField()
    demourl = db.ListField(db.StringField())

    meta = {
            'collection': 'users'
    }

    def get_id(self):
        return unicode(self.id)

class Todo(db.Document):
    """
    It store the TODO infomation

    topic : topic Field
    start: start timestamp
    end: end timestamp
    desc:description of this todo
    """
    poster = db.ObjectIdField()
    topic = db.StringField(required = True)
    start = db.DateTimeField(required = True)
    end = db.DateTimeField()
    desc = db.StringField()
    done = db.BooleanField()
    #note = db.StringField()

    meta ={
        'collection':'todo'
    }

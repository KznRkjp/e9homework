from app import db
from flask_login import UserMixin

class Events(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, unique=False, nullable=False)
    date_start = db.Column(db.Date, unique=False, nullable=False)
    date_end = db.Column(db.Date, unique=False, nullable=False)
    topic = db.Column(db.String(80), unique=False, nullable=False)
    text = db.Column(db.String(1000), unique=False, nullable=False)



class Users(db.Model, UserMixin):
    _id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)

    def get_id(self):
        return self.user_email

    def is_authenticated(self):
        return self.authenticated

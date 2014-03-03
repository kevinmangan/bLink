from app import db
from datetime import datetime

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    password = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    opportunities = db.relationship('Opportunity', backref = 'author', lazy = 'dynamic') # backref allows us to obtain opportinity.author

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Opportunity(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    subject = db.Column(db.String(40))
    description = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<Opportunity %r>' % (self.body)
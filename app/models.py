from app import db

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    opportunities = db.relationship('Opportunity', backref = 'author', lazy = 'dynamic') # backref allows us to obtain opportinity.author

    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Opportunity(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    subject = db.Column(db.String(40))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Opportunity %r>' % (self.body)
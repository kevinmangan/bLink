from app import db

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(64), index = True, unique = True)
	firstName = db.Column(db.String(64), index = False, unique = True)
	lastName = db.Column(db.String(64), index = True, unique = True)
	password = db.Column(db.String(64), index = False, unique = False)
	email = db.Column(db.String(120), index = True, unique = True)
	location = db.Column(db.String(120), index = False, unique = False)
	phone = db.Column(db.String(120), index = False, unique = False)
	about = db.Column(db.String(1000), index = False, unique = False)
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
		return '<User %r>' % (self.username)

	def post_op(self, subject, body):
		opportunity = Opportunity(network=self.network, subject=subject, body=body, user_id=self.id)
		db.session.add(opportunity)
		db.session.commit()

class Student(User):
	network = db.Column(db.String(120), index = True, unique = False)
	class_year = db.Column(db.Integer(), index = True, unique = False)

class Recruiter(User):
	pass




class Opportunity(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	network = db.Column(db.String(120), index = True, unique = False)
	subject = db.Column(db.String(40))
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Opportunity %r>' % (self.body)











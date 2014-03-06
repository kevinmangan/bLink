from app import db
import time
import datetime


### Establishes many to many relationship between user and messages
sent_to_table = db.Table('sent_to_table',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('message_id', db.Integer, db.ForeignKey('message.id'))
)

sent_from_table = db.Table('sent_from_table',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('message_id', db.Integer, db.ForeignKey('message.id'))
)

conversation_table = db.Table('conversation_table',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('conversation_id', db.Integer, db.ForeignKey('conversation.id'))
)

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
	opportunities = db.relationship('Opportunity', backref = 'author', lazy = 'dynamic')
	sentLikes = db.relationship('Like', backref = 'sender', lazy = 'dynamic')

	## Backrefs ##
	##############
	## sentMessages
	## receivedMessages
	## conversation

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
		ts = time.time()
		timestamp = datetime.datetime.fromtimestamp(ts)
		opportunity = Opportunity(network=self.network, subject=subject, body=body, user_id=self.id, timestamp=timestamp)
		db.session.add(opportunity)
		db.session.commit()

	def like_op(self, receiver, opportunity):
		ts = time.time()
		timestamp = datetime.datetime.fromtimestamp(ts)
		like = Like(timestamp=timestamp, is_new=True, user_id=self.id, opportunity=opportunity)
		db.session.add(opportunity)
		db.session.commit()

	def start_conversation(self, subject, opportunity):
		conversation = Conversation(subject=subject, opportinity=opportunity)
		db.session.add(conversation)
		db.session.commit()

	def send_message(self, body, sentTo, conversation):
		message = Message(body=body, sentTo=sentTo, sentFrom=self, conversation=conversation)
		db.session.add(message)
		db.session.commit()

	def unread_messages(self):
		return Message.query.join(User.receivedMessages).filter_by(isNew=True).count()


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
	timestamp = db.Column(db.DateTime())
	conversations = db.relationship('Conversation', lazy = 'dynamic')
	likes = db.relationship('Like', lazy = 'dynamic')
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	
	def getTime(self):
		ts = time.time()
		return self.timestamp.strftime('%I:%M %p').lstrip('0')

	## Backrefs ##
	## author

	def __repr__(self):
		return '<Opportunity %r>' % (self.body)

# A user sends a message
# Relationship: A user has many messages, and a message has many users (2 users, the sender and reciever)
# Relationship: A message belongs to one conversation
class Message(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.String(20))
	isNew = db.Column(db.Boolean())
	sentTo = db.relationship('User', secondary=sent_to_table, backref=db.backref('receivedMessages', lazy='dynamic'))
	sentFrom = db.relationship('User', secondary=sent_from_table, backref=db.backref('sentMessages', lazy='dynamic'))
	conversation = db.Column(db.Integer, db.ForeignKey('conversation.id'))


# Relationship: A conversation has many messages
# Relationship: A conversation has one user
class Conversation(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	subject = db.Column(db.String(40))
	messages = db.relationship('Message', lazy = 'dynamic')
	opportunity = db.Column(db.Integer, db.ForeignKey('opportunity.id'))
	users = db.relationship('User', secondary=conversation_table, backref=db.backref('conversations', lazy='dynamic'))

	def mostRecentMessage(self):
		return Message.query.filter(conversation=self).order_by(desc(Message.timestamp)).first()


# A user likes an opportunity
# Relationship: One user has many likes (that they sent)
# Relationship: One Opportunity has many likes
class Like(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	timestamp = db.Column(db.DateTime(), index = True)
	isNew = db.Column(db.String(140))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	opportunity = db.Column(db.Integer, db.ForeignKey('opportunity.id'))

	## Backrefs ##
	## sender

### For each user.conversation, display most recent message subject
	### For each message in conversation, display them















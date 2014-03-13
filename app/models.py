from app import db
import time
import datetime
from sqlalchemy import desc
from config import WHOOSH_ENABLED

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
	firstName = db.Column(db.String(64), index = False, unique = False)
	lastName = db.Column(db.String(64), index = True, unique = False)
	password = db.Column(db.String(64), index = False, unique = False)
	email = db.Column(db.String(120), index = True, unique = True)
	location = db.Column(db.String(120), index = False, unique = False)
	phone = db.Column(db.String(120), index = False, unique = False)
	about = db.Column(db.String(1000), index = False, unique = False)
	opportunities = db.relationship('Opportunity', backref = 'author', lazy = 'dynamic')
	sentLikes = db.relationship('Like', backref = 'sender', lazy = 'dynamic')
	network = db.Column(db.String(120), index = True, unique = False)
	class_year = db.Column(db.Integer(), index = True, unique = False)

	## Backrefs ##
	##############
	## sentMessages
	## receivedMessages
	## conversations

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

	def like_op(self, opportunity):
		ts = time.time()
		timestamp = datetime.datetime.fromtimestamp(ts)
		like = Like(timestamp=timestamp, isNew=True, sentFrom=self.id, opportunity=opportunity.id)
		db.session.add(like)
		db.session.commit()

	def start_conversation(self, subject, opportunity, sentTo):
		conversation = Conversation(subject=subject, opportunity=opportunity.id, users=[self, sentTo])
		db.session.add(conversation)
		db.session.commit()
		return conversation

	def send_message(self, body, sentTo, conversation):
		ts = time.time()
		timestamp = datetime.datetime.fromtimestamp(ts)
		message = Message(body=body, sentTo=[sentTo], sentFrom=[self], conversation=conversation.id, isNew=True, timestamp=timestamp) # The many to many parameters have to be in lists. weird.
		db.session.add(message)
		db.session.commit()

	def unread_messages(self):
		#return Message.query.join(User.receivedMessages).filter(User.id==self.id).filter_by(isNew=True).count()
		messages = self.receivedMessages.all()
		i = 0
		for message in messages:
			if message.isNew:
				i = i + 1
		return i

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
	timestamp = db.Column(db.DateTime())
	isNew = db.Column(db.Boolean())
	sentTo = db.relationship('User', secondary=sent_to_table, backref=db.backref('receivedMessages', lazy='dynamic'))
	sentFrom = db.relationship('User', secondary=sent_from_table, backref=db.backref('sentMessages', lazy='dynamic'))
	conversation = db.Column(db.Integer, db.ForeignKey('conversation.id'))

	def getTime(self):
		return self.timestamp.strftime('%I:%M %p').lstrip('0')



# Relationship: A conversation has many messages
# Relationship: A conversation has one user
class Conversation(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	subject = db.Column(db.String(40))
	messages = db.relationship('Message', backref="convo", lazy = 'dynamic')
	opportunity = db.Column(db.Integer, db.ForeignKey('opportunity.id'))
	users = db.relationship('User', secondary=conversation_table, backref=db.backref('conversations', lazy='dynamic'))

	# Return most recent message in a conversation
	# Used to display the most recent messages of each conversation in the inbox
	def mostRecentMessage(self, user):
		messages = self.messages.order_by(Message.timestamp).all()
		for message in messages:
			if message.sentFrom[0] == user:
				messages.remove(message)
		if messages:
			return messages[0]
		else:
			return False

# A user likes an opportunity
# Relationship: One user has many likes (that they sent)
# Relationship: One Opportunity has many likes
class Like(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	timestamp = db.Column(db.DateTime(), index = True)
	isNew = db.Column(db.String(140))
	sentFrom = db.Column(db.Integer, db.ForeignKey('user.id'))
	opportunity = db.Column(db.Integer, db.ForeignKey('opportunity.id'))

	## Backrefs ##
	## sender

	def getTime(self):
		ts = time.time()
		return self.timestamp.strftime('%I:%M %p').lstrip('0')

### For each user.conversation, display most recent message subject
	### For each message in conversation, display them















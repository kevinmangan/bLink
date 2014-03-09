from app import app, db, lm, bcrypt
from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import LoginForm, SignupForm, EditProfileForm, OpForm, messageForm
from models import User, Opportunity, Conversation, Message, Like

reserved_usernames = 'home signup login logout post'


@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.before_request   
def before_request():
	g.user = current_user

@app.route('/')
@app.route('/index')
def index():
	loginForm = LoginForm()
	signupForm = SignupForm()
	return render_template("index.html", title = 'Log in', form1=loginForm, form2=signupForm)

@app.route("/login", methods=["POST"])
def login():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))
	loginForm = LoginForm()
	signupForm = SignupForm()
	if loginForm.validate_on_submit():
		username = loginForm.username.data
		password = loginForm.password.data
		if username is None or password is None:
			flash('Invalid login. Please try again.')
			return redirect(url_for('index'))
		user = User.query.filter_by(username = username).first()
		if user is None:
			flash('That username does not exist. Please try again.')
			return redirect(url_for('index'))
		if bcrypt.check_password_hash(user.password, password) is False:
			flash('Invalid Login. Please try again.')
			return redirect(url_for('index'))
		login_user(user, remember=True)
		return redirect(request.args.get("next") or url_for("user", username=user.username, user=user))
	return render_template("index.html", title = 'Sign In', form1=loginForm, form2=signupForm)

@app.route("/signup", methods=["POST"])
def signup():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))
	loginForm = LoginForm
	signupForm = SignupForm()
	if signupForm.validate_on_submit():
		username = signupForm.username.data
		if username not in reserved_usernames.split():
			password = signupForm.password.data
			password_hash = bcrypt.generate_password_hash(password)
			email = signupForm.email.data
			firstName = signupForm.firstName.data
			lastName = signupForm.lastName.data
			network = signupForm.network.data
			location = signupForm.location.data
			class_year = signupForm.class_year.data
			
			user = User.query.filter_by(email = email).first() # Check if that email already exists
			if user is not None:
				flash('That email is already in use')
				return redirect(url_for('index'))
			
			user = User.query.filter_by(username = username).first() # Check if that username already exists
			if user is not None:
				flash('That username is already in use')
				return redirect(url_for('index'))
			
			# Create the user
			user = User(username=username, password=password_hash, email=email, firstName=firstName, lastName=lastName, location=location,
			network=network, class_year=class_year)
			db.session.add(user)
			db.session.commit()
		login_user(user, remember=True)
		return redirect(request.args.get("next") or url_for("editProfile", username=user.username, user=user))
	return render_template("index.html", title = 'Sign Up', form1=loginForm, form2=signupForm)

@app.route("/logout")
@login_required
def logout():
	logout_user()
	form = LoginForm()
	return redirect("/")

# Delete an opportunity
@app.route("/delete/<id>")
@login_required
def delete(id):
	opportunity = Opportunity.query.filter_by(id = id).first()
	user = g.user
	if user == opportunity.author:
		db.session.delete(opportunity)
		db.session.commit()
	return redirect(url_for('user', username=user.username))

@app.route("/opportunities/<network>", methods=["POST", "GET"])
@login_required
def opportunities(network):
	user = g.user
	form = OpForm()
	if request.method == 'POST':
		user.post_op(form.subject.data, form.body.data)
		return redirect(url_for('opportunities', network=network))
	if network == 'All':
		opportunities = Opportunity.query.all()
	else:
		opportunities = Opportunity.query.filter_by(network = network)
	return render_template("opportunities.html", title = 'Opportunities', opportunities=opportunities, user=user, form=form, network=network)

@app.route("/user/<username>", methods=["POST", "GET"])
@login_required   # login required wrapper to make sure the user is logged in
def user(username):
	form = messageForm()
	user = User.query.filter_by(username = username).first()
	if user == None:
		flash('User ' + username + ' not found.')
		return redirect(url_for('index'))
	if request.method == 'POST':
		subject = request.form['subject']
		opportunity_id = request.form['opportunity']
		opportunity = Opportunity.query.get(int(opportunity_id))
		body = request.form['body']
		sentTo_id = request.form['sentTo']
		sentTo = User.query.get(int(sentTo_id))
		conversation = user.start_conversation(subject=subject, opportunity=opportunity, sentTo=sentTo)
		user.send_message(body=body, sentTo=sentTo, conversation=conversation)
	return render_template('user.html',
		user = user,
		form = form,
		title = 'Profile - ' + user.username)

@app.route("/edit/<username>", methods=["POST", "GET"])
@login_required
def editProfile(username):
	user = User.query.filter_by(username = username).first()
	if user == None:
		flash('User ' + username + ' not found.')
		return redirect(url_for('index'))
	form = EditProfileForm()
	if request.method == 'POST':
		if form.firstName.data:
			user.firstName = form.firstName.data
		if form.lastName.data:
			user.lastName = form.lastName.data
		if form.location.data:
			user.location = form.location.data
		if form.phone.data:
			user.phone = form.phone.data
		if form.about.data:
			user.about = form.about.data
		if form.password.data:
			if form.confirmPassword.data is None:
				flash('Please confirm your password.')
				return redirect(url_for("editProfile", username=user.username,  user=user))
			if form.password.data != form.confirmPassword.data:
				flash('Confirmation does not match.')
				return redirect(url_for("editProfile", user=user))
			password_hash = bcrypt.generate_password_hash(form.password.data)
			user.password = password_hash
		db.session.commit()
		return redirect(url_for('user', username=user.username))
	return render_template("edit.html", title = 'Edit Profile', username=user.username, user=user, editProfileForm=form)


@app.route("/inbox/<username>", methods=["POST", "GET"])
@login_required
def inbox(username):
	user = User.query.filter_by(username = username).first()
	if request.method == 'POST':
		sentTo_id = request.form['sentTo']
		sentTo = User.query.get(int(sentTo_id))
		conversation_id = request.form['conversation']
		conversation = Conversation.query.get(int(conversation_id))
		user.send_message(request.form['body'], sentTo, conversation)
	return render_template("inbox.html", user=user)

# Mark mail as read when you click it
# AJAX (relevant javascript in base.html)
@app.route("/mark_as_read", methods=["POST"])
@login_required
def mark_as_read():
	message_id = request.form['message']
	message = Message.query.get(int(message_id))
	message.isNew = False
	db.session.commit()
	return jsonify()

# AJAX (relevant javascript in base.html)
@app.route("/like_opportunity", methods=["POST"])
@login_required
def like_opportunity():
	opportunity_id = request.form['opportunity_id']
	opportunity = Opportunity.query.get(int(opportunity_id))
	user_id = request.form['user_id']
	user = User.query.get(int(user_id))
	user.like_op(opportunity=opportunity)
	return jsonify()

	


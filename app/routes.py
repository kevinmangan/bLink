from app import app, db, lm, bcrypt
from flask import render_template
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import LoginForm, SignupForm, PostOpportunityForm
from models import User, Opportunity
from datetime import datetime

reserved_usernames = 'home signup login logout post'

@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.before_request   # If a view uses this decorator, it will run before the request is handled
def before_request():
	g.user = current_user

@app.route('/')
@app.route('/index')
def index():
	form1 = LoginForm()
	form2 = SignupForm()
	return render_template("index.html", title = 'Log in', form1=form1, form2=form2)

@app.route("/login", methods=["POST"])
def login():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))
	form1 = LoginForm()
	form2 = SignupForm()
	if form1.validate_on_submit():
		email = form1.email.data
		username = form1.username.data # Commenting so users can use email as username
		password = form1.password.data
		if email is None or username is None or password is None:
			flash('Invalid login. Please try again.')
			return redirect(url_for('index'))
		user = User.query.filter_by(email = email).first()
		if user is None:
			flash('That email does not exist. Please try again.')
			return redirect(url_for('index'))
		user = User.query.filter_by(username = username).first()
		if user is None:
			flash('That username does not exist. Please try again.')
			return redirect(url_for('index'))
		if bcrypt.check_password_hash(user.password, password) is False:
			flash('Invalid Login. Please try again.')
			return redirect(url_for('index'))
		login_user(user, remember=True)
		flash("Logged in successfully.")
		return redirect(request.args.get("next") or url_for("user", username=user.username))
	return render_template("index.html", title = 'Sign In', form1=form, form2=form2)

@app.route("/signup", methods=["POST"])
def signup():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))
	form1 = LoginForm
	form2 = SignupForm()
	if form2.validate_on_submit():	
		username = form2.username.data
		if username not in reserved_usernames.split():
			password = form2.password.data
			password_hash = bcrypt.generate_password_hash(password)
			email = form2.email.data
			
			user = User.query.filter_by(email = email).first() # Check if that email already exists
			if user is not None:
				flash('That email is already in use')
				return redirect(url_for('index'))
			
			user = User.query.filter_by(username = username).first() # Check if that username already exists
			if user is not None:
				flash('That username is already in use')
				return redirect(url_for('index'))
			
			# Create the user
			user = User(username=username, password=password_hash, email=email)
			db.session.add(user)
			db.session.commit()
		# Also write code for email-ver
		login_user(user, remember=True)
		flash("Logged in successfully.")
		return redirect(request.args.get("next") or url_for("user", username=user.username))
	return render_template("index.html", title = 'Sign Up', form1=form, form2=form2)

@app.route("/logout")
@login_required
def logout():
	logout_user()
	form = LoginForm()
	return redirect("/")


@app.route("/user/<username>")
@login_required   # login required wrapper to make sure the user is logged in
def user(username):
	user = User.query.filter_by(username = username).first()
	if user == None:
		flash('User ' + username + ' not found.')
		return redirect(url_for('index'))
	opportunities = [
		{ 'author': user, 'subject': 'Test post #1', 'body': 'Test post #1' },
		{ 'author': user, 'subject': 'Test post #1', 'body': 'Test post #2' }
	]
	form1 = PostOpportunityForm()
	return render_template('user.html',
		user = user,
		opportunities = opportunities, form1=form1)

# Opportunties Section
@app.route("/user/post_opportunity", methods=["POST"])
def post_opportunity():
	if g.user is None or not g.user.is_authenticated():
		return redirect(url_for('index'))
	form1 = PostOpportunityForm()
	if form1.validate_on_submit():
		subject = form1.subject.data
		description = form1.description.data
		# Create the opportunity
		opportunity = Opportunity(subject=subject, description=description, timestamp=datetime.utcnow(), user_id=g.user.get_id())
		db.session.add(opportunity)
		db.session.commit()
		return 'Opportunity Posted'

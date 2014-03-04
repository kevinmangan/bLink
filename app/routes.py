from app import app, db, lm, bcrypt
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import LoginForm, SignupForm, EditProfileForm, OpForm
from models import User, Student, Recruiter, Opportunity

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
		email = loginForm.email.data
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
			student = Student(username=username, password=password_hash, email=email, firstName=firstName, lastName=lastName, location=location,
			network=network, class_year=class_year)
			db.session.add(student)
			db.session.commit()
		login_user(student, remember=True)
		return redirect(request.args.get("next") or url_for("editProfile", username=student.username, user=student))
	return render_template("index.html", title = 'Sign Up', form1=loginForm, form2=signupForm)

@app.route("/logout")
@login_required
def logout():
	logout_user()
	form = LoginForm()
	return redirect("/")

@app.route("/opportunities/<network>", methods=["POST", "GET"])
@login_required
def opportunities(network):
	user = g.user
	student = Student.query.filter_by(username = user.username).first()
	form = OpForm()
	if request.method == 'POST':
		student.post_op(form.subject.data, form.body.data)
		return redirect(url_for('opportunities', network=network))
	if network == 'All':
		opportunities = Opportunity.query.all()
	else:
		opportunities = Opportunity.query.filter_by(network = network)
	return render_template("opportunities.html", title = 'Opportunities', opportunities=opportunities, user=student, form=form)

@app.route("/user/<username>")
@login_required   # login required wrapper to make sure the user is logged in
def user(username):
	user = Student.query.filter_by(username = username).first()
	if user == None:
		flash('User ' + username + ' not found.')
		return redirect(url_for('index'))
	opportunities = [
		{ 'author': user, 'subject': 'Test post #1', 'body': 'Test post #1' },
		{ 'author': user, 'subject': 'Test post #1', 'body': 'Test post #2' }
	]
	return render_template('user.html',
		user = user,
		opportunities = opportunities,
		title = 'Profile - ' + user.username)

@app.route("/edit/<username>", methods=["POST", "GET"])
@login_required
def editProfile(username):
	user = Student.query.filter_by(username = username).first()
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


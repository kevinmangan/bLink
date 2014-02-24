from app import app, db, lm
from flask import render_template
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import LoginForm, SignupForm
from models import User

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
    return render_template("index.html", title = 'Home')

@app.route("/login", methods=["GET", "POST"])
def login():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('login'))
	form = LoginForm()
	if form.validate_on_submit():
		email = form.email.data
		if email is None:
			flash('Invalid login. Please try again.')
			return redirect(url_for('login'))
		user = User.query.filter_by(email = email).first()
		if user is None:
			flash('Invalid login. Please try again.')
			return redirect(url_for('login'))
		login_user(user, remember=True)
		flash("Logged in successfully.")
		return redirect(request.args.get("next") or url_for("user", username=user.username))
	return render_template("login.html", title = 'Sign In', form=form)

@app.route("/signup", methods=["GET", "POST"])
def signup():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))
	form = SignupForm()
	if form.validate_on_submit():	
		username = form.username.data
		if username not in reserved_usernames.split():
			password = form.password.data
			email = form.email.data
			user = User(username=username, password=password, email=email)
			db.session.add(user)
    		db.session.commit()
		login_user(user, remember=True)
		flash("Logged in successfully.")
		return redirect(request.args.get("next") or url_for("user", username=user.username))
	return render_template("signup.html", title = 'Sign Up', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    form = LoginForm()
    return redirect("login")


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
    return render_template('user.html',
        user = user,
        opportunities = opportunities)

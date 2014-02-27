from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField
from wtforms.validators import Required

class LoginForm(Form):
    username = TextField('username', validators = [Required()])
    password = PasswordField('password', validators = [Required()])
    email = TextField('email', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)

class SignupForm(Form):
    username = TextField('username', validators = [Required()])
    password = PasswordField('password', validators = [Required()])
    firstName = TextField('firstName', validators = [Required()])
    lastName = TextField('lastName', validators = [Required()])
    email = TextField('email', validators = [Required()])
    location = TextField('location', validators = [Required()])
    school = TextField('school', validators = [Required()])
    class_year = TextField('class_year', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)
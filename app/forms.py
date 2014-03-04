from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField, FileField, TextAreaField, SelectField
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
    network = SelectField('network', choices=[('INSEAD', 'INSEAD'), ('Columbia Business School', 'Columbia Business School'), 
        ('London Business School', 'London Business School'),
     ('Harvard Business School', 'Harvard Business School'), ('Stanford Graduate School of Business', 'Stanford Graduate School of Business'),
      ('University of Pennsylvania: Wharton', 'University of Pennsylvania: Wharton')], validators = [Required()])
    class_year = TextField('class_year', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)

class EditProfileForm(Form):
    picture = FileField('picture')
    password = PasswordField('password', id="form-field-pass1")
    confirmPassword = PasswordField('confirmPassword', id="form-field-pass2")
    firstName = TextField('firstName', id="form-field-first")
    lastName = TextField('lastName', id="form-field-last")
    location = TextField('location')
    email = TextField('email', id="form-field-email")
    phone = TextField('phone', id="form-field-phone")
    about = TextAreaField('location')

class OpForm(Form):
    subject = TextField('subject', validators = [Required()])
    body = TextAreaField('body', validators = [Required()])
    

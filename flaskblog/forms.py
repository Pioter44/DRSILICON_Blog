from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User

#Create class for Registation Form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired(),Length(min=2, max=20)])
    email = StringField('Email', validators = [DataRequired(),Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password') ])
    submit = SubmitField('Sign Up')
    
    #Declare function (custom validator) that will prevent to register user with the same username
    def validate_username(self, username):
        #Query db to find all users that have username equal to that one that is registered now. If there is no such user then 'user = None'
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a diffrent one')
    
    #Declare function (custom validator) that will prevent to register user with the same email
    def validate_email(self, email):
        #Query db to find all users that have email equal to that one that is registered now. If there is no such user then 'user = None'
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a diffrent one')
    
#Create class for Login form
class LoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(),Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
#Create secret key that will prevent agains modify the cookies

#Create class for UpdateAccountForm Form
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired(),Length(min=2, max=20)])
    email = StringField('Email', validators = [DataRequired(),Email()])
    picture = FileField('Update Profile Picture', validators = [FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')
    
    #Declare function (custom validator) that will prevent to register user with the same username
    def validate_username(self, username):
        #This if statment is to do update only if data provided by user will be diffrent than current one
        if username.data!= current_user.username:
            #Query db to find all users that have username equal to that one that is registered now. If there is no such user then 'user = None'
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a diffrent one')
    
    #Declare function (custom validator) that will prevent to register user with the same email
    def validate_email(self, email):
        #This if statment is to do update only if data provided by user will be diffrent than current one
        if email.data!= current_user.email:
            #Query db to find all users that have email equal to that one that is registered now. If there is no such user then 'user = None'
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a diffrent one')
    
    
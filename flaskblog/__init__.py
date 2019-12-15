from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

#Create and set secret key that will prevent agains modify the cookies
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
#For setting location of out SQLAlchemy db file. Three slashes '///' means current directory so site.db file will be located in the same directory as flaskblog.py
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

#Create sqlalchemy instance
#Each class will be a separate table in database
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' #this is to tell apllication where our login route is located. View that we are passing here ('login') is a name of our login route
login_manager.login_message_category = 'info' #this is to flash message to look nicer


from flaskblog import routes


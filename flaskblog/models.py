from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin #Class UserMixin is for managing user login session

#Create decorated function that will 
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#Each class will be a separate table in database
#Create User model table. Inherit from two classes. Class UserMixin is for managing user login session
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False) # column in table. This column will be a primary key column (id of the user)
    username = db.Column(db.String(20),unique=True, nullable=False) #unique=True means that the username must be unique. nullable=False means that this field is mandatory
    email = db.Column(db.String(120),unique=True, nullable=False)
    image_file = db.Column(db.String(120),unique=False, default='default.jpeg')  #For user image picture
    password = db.Column(db.String(60),unique=False, nullable=False) #password will be hased and hased password will be 60 characters long. Here #unique=False and this means that the password not need to be unique (two diffrent users can have the same password)
    post = db.relationship('Post', backref='author', lazy=True) #"Post table/module" has a back reference to a author (each 'post' need to have an author). backref allows to get a details of author for a given 'post'. lazy arguments decide when a database load data
    
    #Deciding how the User database object will be printed
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    
#Create User model table
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False) # column in table. This column will be a primary key column (id of the user)
    title = db.Column(db.String(100), nullable=False) #unique=True means that the username must be unique
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) #'user.id' - this a id of the user that wrote a post. 'user' is a default name of a table for class User(db.Model). 'User' is a name of class
    
    #Deciding how the User database object will be printed
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
    
    
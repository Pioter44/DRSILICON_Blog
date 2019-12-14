from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

#Create and set secret key that will prevent agains modify the cookies
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
#For setting location of out SQLAlchemy db file. Three slashes '///' means current directory so site.db file will be located in the same directory as flaskblog.py
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

#Create sqlalchemy instance
#Each class will be a separate table in database
db = SQLAlchemy(app)

#Each class will be a separate table in database
#Create User model table
class User(db.Model):
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
    
    
posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

#Create registration route
@app.route("/register", methods = ['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!","success")
        return redirect(url_for('home'))
    return render_template('register.html', title = 'Register', form = form)

#Create login route
@app.route("/login", methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if (form.email.data =="admin@blog.com") and (form.password.data =="12345"):
            flash(f"You have been logged in !","success")
            return redirect(url_for('home'))
        else:
            flash(f"Login unsuccessfull. Please check username and password !","danger")
    return render_template('login.html', title = 'Login', form = form)


#Create login route



if __name__ == '__main__':
    app.run(debug=True)

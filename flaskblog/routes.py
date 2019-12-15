from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User,Post
from flask_login import login_user #To manage user login session
from flask_login import current_user, logout_user #To manage user login session
from flask_login import login_required #will be used as a decoreator to make sure that user is log in

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
    #If user is log in then this if statment will cause that if user will press register button then will be redirected to home website
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        #If form is valid on submit then lets hash the password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        #Create new user
        user = User(username=form.username.data, email = form.email.data, password = hashed_password)
        #Save user to db
        db.session.add(user)
        db.session.commit()
        flash(f"Your account has been created! You are now able to log in","success")
        return redirect(url_for('login'))
    return render_template('register.html', title = 'Register', form = form)

#Create login route
@app.route("/login", methods = ['GET','POST'])
def login():
    #If user is log in then this if statment will cause that if user will press login button then will be redirected to home website
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        '''
        #if (form.email.data =="admin@blog.com") and (form.password.data =="12345"):
            flash(f"You have been logged in !","success")
            return redirect(url_for('home'))
        else:
            flash(f"Login unsuccessfull. Please check username and password !","danger")
        '''
        #Checking database is email and password are valid
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            #User email is in db and password is matching so user can be login. This will be handled by function 'login_user'
            login_user(user, remember = form.remember.data)
            #This is for redirect user to account page if will be log in successfully
            next_page = request.args.get('next') #request args is a dictionary and here we are getting value from dict for key='next' using get(). get() will no throw error when key will not exist (returning None if key not exist)
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            #Flash message if login not successfull
            flash(f"Login unsuccessfull. Please check username and password !","danger")
        
    return render_template('login.html', title = 'Login', form = form)


#Create logout route
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
    
#Create account route - only visible if user is log in
@app.route("/account")
@login_required #this decorator will cause that user will have access to Account subpage only if is log in
def account():
    return render_template('account.html', title = 'Account')
    
    
    
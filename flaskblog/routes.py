import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog.models import User,Post
from flask_login import login_user #To manage user login session
from flask_login import current_user, logout_user #To manage user login session
from flask_login import login_required #will be used as a decoreator to make sure that user is log in


@app.route("/")
@app.route("/home")
def home():
    
    #Here I create new variable posts where I will store my queary from db about posts 
    posts = Post.query.all()
    
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
        flash("Your account has been created! You are now able to log in","success")
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
    
#Function with logic to save used uploaded picture
def save_picture(form_picture):
    #To avoid problem with the same picture number lets rename picture with hashed value
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    
    #To resize picture in order to save space
    output_size = (125,125)
    i= Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    
    return picture_fn
    
    
    
    
#Create account route - only visible if user is log in
@app.route("/account", methods = ['GET','POST'])
@login_required #this decorator will cause that user will have access to Account subpage only if is log in
def account():
    form = UpdateAccountForm()
    #If form is valid then we can update our email or username and update it in decode
    if form.validate_on_submit():
        
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
            
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f"Your account has been updated! ","success")
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        
    image_file = url_for('static', filename = 'profile_pics/' + current_user.image_file)
    return render_template('account.html', title = 'Account', image_file = image_file, form = form) #here we are also passing some parameters to 'account.html' template for example image_file
    
    
#Create post/new route - only visible if user is log in
@app.route("/post/new", methods = ['GET','POST'])
@login_required #this decorator will cause that user will have access to this subpage only if is log in
def new_post():
    
    #Create instance of PostForm 
    form = PostForm()
    
    #If form is valid then we can update our email or username and update it in decode
    if form.validate_on_submit():
        
        #Save post to a db
        post = Post(title=form.title.data, content=form.content.data, author = current_user)
        #Save post to db
        db.session.add(post)
        db.session.commit()
        
        
        flash("Your post has been created! ","success")
        return redirect(url_for('home'))
    
    
    return render_template('create_post.html', title = 'New Post', form = form, legend='New Post')
    
    
#Create new route - that will take us to a specific post. Flask give us ability to add variable within route
@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title = post.title, post = post)
    
    
#Create new route - that will take us to a specific post and allow us to update it
@app.route("/post/<int:post_id>/update", methods = ['GET','POST'])
@login_required #this decorator will cause that user will have access to this subpage only if is log in
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    #The post can be updated only by author so we will use if for this purpose
    if post.author != current_user:
        abort(403)
    form = PostForm()
    
    #If statment to accept update for a post and save it to db
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        #Save it to db. We dont need to do db.session.add() because this post/record is already in db so db.session.commit() is enougth here
        db.session.commit()
        flash(f"Your post has been updated! ","success")
        return redirect(url_for('post', post_id = post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    
    return render_template('create_post.html', title = 'Update Post', form = form, legend = 'Update Post')
    
#Create new route - that will for deleting route
@app.route("/post/<int:post_id>/delete", methods = ['POST'])
@login_required #this decorator will cause that user will have access to this subpage only if is log in
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    #The post can be updated only by author so we will use if for this purpose
    if post.author != current_user:
        abort(403)
    
    db.session.delete(post)
    db.session.commit()
    flash(f"Your post has been deleted! ","success")
    return redirect(url_for('home'))
    

import urllib
import sys
import datetime
import mongoengine as mg
from flask import Flask, render_template, request, flash, session, redirect, url_for
from mongoengine import *
from flask_bcrypt import Bcrypt
from flask_login import login_manager, current_user, login_user, logout_user
from werkzeug.contrib.fixers import ProxyFix
from forms import RegistrationForm, LoginForm
from schema import *

# You need to create a mongo account and let Jayde know your mongo email address to add you to the db system
# Then you need to create a password.txt and username.txt each storing the password and username of your mongo account
# If the above doesn't work try setting mongo_uri directly to:
# mongodb+srv://your_first_name_with_first_letter_capitalized:your_first_name_with_first_letter_capitalized@csc301-v3uno.mongodb.net/test?retryWrites=true
# If the above works, it should be a parsing problem try updating Python
# If not ask for troubleshoot help in group chat
app = Flask(__name__)

# With these constants strings, we can connect to generic databases
USERNAME_FILE = "username.txt"
PASSWORD_FILE = "password.txt"
DATABASE = "test"
MONGO_SERVER = "csc301-v3uno.mongodb.net"
APP_NAME = "Snacker"

try:
    username = open(USERNAME_FILE,  'r').read().strip().replace("\n","")
    pw = urllib.parse.quote(open(PASSWORD_FILE, 'r').read().strip().replace("\n", ""))
    print("hello")
    mongo_uri = f"mongodb+srv://{username}:{pw}@{MONGO_SERVER}/{DATABASE}?retryWrites=true"
    #mongo_uri = "mongodb+srv://Jayde:Jayde@csc301-v3uno.mongodb.net/test?retryWrites=true"
    app.config["MONGO_URI"] = mongo_uri
    mongo = mg.connect(host=mongo_uri)
    # This is necessary for user tracking
    app.wsgi_app = ProxyFix(app.wsgi_app, num_proxies=1)
except Exception as inst:
    print("Error in database connection:", inst)
    exit()
# TODO: Need to change this to an env variable later
app.config["SECRET_KEY"] = "2a0ca44c88db3d509085f32f2d4ed2e6"
app.config['DEBUG'] = True
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
bcrypt = Bcrypt(app)

@app.route("/index")
def index():
    return render_template('index.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About {APP_NAME}')


# Go to the local url and refresh that page to test
@app.route('/')
def hello_world():
    print('This is standard output', file=sys.stdout)
    # Selecting the database we want to work withf
    my_database = mongo[DATABASE]
    print(mongo.database_names())
    print(my_database)
    print((f"All collections in the database '{DATABASE}':\n\t{my_database.list_collection_names()}"), file=sys.stdout)
    # This prints all collections inside the database with name DATABASE
    print("Documents inside all collections: ", file=sys.stdout)
    for collec in my_database.list_collection_names():
        print(f"    {collec}", file=sys.stdout)
        for doc in my_database[collec].find({}):
            print(f"        {doc}", file=sys.stdout)
    print("", file=sys.stdout)
    for obj in User.objects:
        print(f"   Before Save User: {obj.email} \n", file=sys.stdout)
    for obj in CompanyUser.objects:
        print(f"   Before Save CompanyUser: {obj.email} \n", file=sys.stdout)
    normal_user = User(email="jayde.yue@mail.utoronto.ca",first_name="Jayde", last_name="Yue", password="123123")
    company_user = CompanyUser(email="JaydeYue@jaydeyue.com", first_name="Jayde", last_name="Yue",
                               company_name="The Amazing Jayde Yue Company", password="123123")
    try:
        normal_user.save()
    except Exception as e:
        return "Error \n %s" % e
    try:
        company_user.save()
    except Exception as e:
        return "Error \n %s" % e
    # If without error, then both the normal user and company user should display in User collection
    # And only company user should display in CompanyUser collection
    for obj in User.objects:
        print(f"   After Save User: {obj.email} \n", file=sys.stdout)
    for obj in CompanyUser.objects:
        print(f"   After Save CompanyUser: {obj.email} \n", file=sys.stdout)

    # Display existing snacks in the db
    for obj in Snack.objects:
        print(f"    Before Save Snack: {obj.snack_brand} {obj.snack_name} \n", file=sys.stdout)
    # To test it yourself, create a snack with different name and brand from the exisiting snacks in the db
    snack = Snack(snack_name="Crunchy Cheese Flavoured", available_at_locations=["Canada"], snack_brand="Cheetos")
    snack.description = "Yummy yummy"
    try:
        snack.save()
    except Exception as e:
        return "Error \n %s" % e
    # Display existing snacks in db, your new snack should be here if it has been saved without error
    for obj in Snack.objects:
        print(f"    After Save Snack: {obj.snack_brand} {obj.snack_name} \n", file=sys.stdout)
    return 'Hello World!'


@app.route('/register/', methods=["GET","POST"])
def register():
    # IMPORTANT: The user password should always be encripted for increased security
    encrypt_pw = lambda pw_str : bcrypt.generate_password_hash(pw_str)
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        email = form.email.data
        # Add user to database
        try:
            new_user = User(email=form.email.data, first_name=form.first_name.data,
                last_name=form.last_name.data, password=encrypt_pw(form.password.data))
            new_user.save()
        except Exception as e:
            print(f"Error {e}. \n Couldn't add user {new_user},\n with following registration form: {form}")
            exit()
        print(f"A new user submited the registration form: {email}", file=sys.stdout)
        for u in User.objects[:10]:
            print(u)
        print(url_for('index'))
        return redirect(url_for('index'))
    return render_template("register.html", title="Register", form=form)

@app.route("/create-snack")
@login_required
def create_snack():
    # TODO: This is an example of a route which requires the user to authenticate, not a complete implementation
    # Gets snacks from database
    snacks = Snack.objects
    for snk in snacks:
        print(snacks)
    return "The front-end of this isn't implemented! D:"


""" Routes and methods related to user login and authentication """

@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()

@app.route("/login", methods=["GET", "POST"])
def login():
    """For GET requests, display the login form.
    For POSTS, login the current user by processing the form."""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(email=form.email.data).first()
        if user is None or not user.check_password(bcrypt, form.password.data):
            flash("Invalid username or password")
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()

from flask import Flask, render_template, request, flash, session, redirect, url_for
from forms import RegistrationForm
from flask_bcrypt import Bcrypt
from werkzeug.contrib.fixers import ProxyFix
import mongoengine as mg
import urllib
import sys
from mongoengine import *
import datetime
from schema import *

# You need to create a mongo account and let Jayde know your mongo email address to add you to the db system
# Then you need to create a password.txt and username.txt each storing the password and username of your mongo account
# If the above doesn't work try setting mongo_uri directly to mongodb+srv://your_first_name_with_first_letter_capitalized:your_first_name_with_first_letter_capitalized@csc301-v3uno.mongodb.net/test?retryWrites=true
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
    normal_user = User(email="jayde.yue@mail.utoronto.ca",first_name="Jayde", last_name="Yue")
    company_user = CompanyUser(email="JaydeYue@jaydeyue.com", first_name="Jayde", last_name="Yue",
                               company_name="The Amazing Jayde Yue Company")
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
def register_page():
    try:
        form = RegistrationForm(request.form)
        if request.method == "POST" and form.validate():
            username  = form.username.data
            email = form.email.data
            print(f"A new user submited the registration form: {username} with email {email}", file=sys.stdout)
            password = bcrypt.generate_password_hash((str(form.password.data))).decode("utf-8")
            flash(f"Thanks for registering! {username}")
            # Register that someone logged into our system
            #TODO: Use flask-login package for security and reliability
            session['logged_in'] = True
            session['username'] = username
            print(url_for('index'))
            return redirect(url_for('index'))
        else:
            flash("ERROR")
        return render_template("register.html", form=form)
    except Exception as e:
        return(str(e))

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/logout")
def logout():
    session['logged_in'] = False
    session['username'] = None
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()

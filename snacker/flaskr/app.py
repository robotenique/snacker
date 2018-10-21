from flask import Flask, render_template, request, flash, session, redirect, url_for
from forms import  RegistrationForm
from flask_bcrypt import Bcrypt
import mongoengine as mg
import urllib
import sys

# You need to create a mongo account and let Jayde know your mongo email address to add you to the db system
# Then you need to create a password.txt and username.txt each storing the password and username of your mongo account
# Don't worry password.txt and username.txt are already added to gitignore so your private info won't be exposed
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
    mongo_uri = f"mongodb+srv://{username}:{pw}@{MONGO_SERVER}/{DATABASE}?retryWrites=true"
    app.config["MONGO_URI"] = mongo_uri
    mongo = mg.connect(host=mongo_uri)
except Exception as inst:
    print("Error in database connection:", inst)
    exit()
# TODO: Need to change this to an env variable later
app.config["SECRET_KEY"] = "2a0ca44c88db3d509085f32f2d4ed2e6"
bcrypt = Bcrypt(app)

@app.route("/index")
def home():
    return render_template('index.html')


@app.route("/about")
def about():
    return render_template('about.html', title=f'About {APP_NAME}')


@app.route('/')
def hello_world():
    print('This is standard output', file=sys.stdout)
    # Selecting the database we want to work with
    my_database = mongo[DATABASE]
    print((f"All collections in the database '{DATABASE}':"
           f"\n\t{my_database.list_collection_names()}"), file=sys.stdout)
    # This prints all collections inside the database with name DATABASE
    print("Documents inside all collections: ", file=sys.stdout)
    for collec in my_database.list_collection_names():
        print(f"    {collec}", file=sys.stdout)
        for doc in my_database[collec].find({}):
            print(f"        {doc}", file=sys.stdout)
    print("", file=sys.stdout)
    return 'Hello World!'


@app.route('/register/', methods=["GET","POST"])
def register_page():
    print("processing the user registration", file=sys.stdout)
    try:
        form = RegistrationForm(request.form)
        if request.method == "POST" and form.validate():
            username  = form.username.data
            email = form.email.data
            password = bcrypt.generate_password_hash((str(form.password.data))).decode("utf-8")
            flash(f"Thanks for registering! {username}")
            # Register that someone logged into our system
            #TODO: User Login_manager package for security and reliability
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash("ERROR")
        return render_template("register.html", form=form)
    except Exception as e:
        return(str(e))

@app.route("/login")
def login():
    return render_template("login.html")

if __name__ == '__main__':
    app.run()


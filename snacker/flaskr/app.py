import sys
import urllib

import mongoengine as mg
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_table import *
from werkzeug.contrib.fixers import ProxyFix

from forms import RegistrationForm, LoginForm
from schema import *

"""
You need to create a mongo account and let Jayde know your mongo email address to add you to the db system
Then you need to create a password.txt and username.txt each storing the password and username of your mongo account
If the above doesn't work try setting mongo_uri directly to:
mongodb+srv://your_first_name_with_first_letter_capitalized:your_first_name_with_first_letter_capitalized@csc301-v3uno.mongodb.net/test?retryWrites=true
If the above works, it should be a parsing problem try updating Python
If not ask for troubleshoot help in group chat
"""

app = Flask(__name__)

# With these constant strings, we can connect to generic databases
USERNAME_FILE = "username.txt"
PASSWORD_FILE = "password.txt"
DATABASE = "test"
MONGO_SERVER = "csc301-v3uno.mongodb.net"
APP_NAME = "Snacker"

try:
    username = open(USERNAME_FILE, 'r').read().strip().replace("\n", "")
    pw = urllib.parse.quote(open(PASSWORD_FILE, 'r').read().strip().replace("\n", ""))
    print("hello")
    mongo_uri = f"mongodb+srv://{username}:{pw}@{MONGO_SERVER}/{DATABASE}?retryWrites=true"
    app.config["MONGO_URI"] = mongo_uri
    mongo = mg.connect(host=mongo_uri)
    # This is necessary for user tracking
    app.wsgi_app = ProxyFix(app.wsgi_app, num_proxies=1)
except Exception as inst:
    raise Exception("Error in database connection:", inst)

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
# See below for use cases of different schema objects
@app.route('/')
def hello_world():
    print('This is standard output', file=sys.stdout)
    # Selecting the database we want to work withf
    my_database = mongo[DATABASE]
    for obj in User.objects:
        print(f"   Before Save User: {obj.email} \n", file=sys.stdout)
    for obj in CompanyUser.objects:
        print(f"   Before Save CompanyUser: {obj.email} \n", file=sys.stdout)
    normal_user = User(email="jayde.yue@mail.utoronto.ca", first_name="Jayde", last_name="Yue", password="123123")
    company_user = CompanyUser(email="JaydeYue@jaydeyue.com", first_name="Jayde", last_name="Yue",
                               company_name="The Amazing Jayde Yue Company", password="123123")
    try:
        normal_user.save()
    except Exception as e:
        print("Error \n %s" % e, file=sys.stdout)
    try:
        company_user.save()
    except Exception as e:
        print("Error \n %s" % e, file=sys.stdout)
    # If without error, then both the normal user and company user should display in User collection
    # And only company user should display in CompanyUser collection
    print(f"afaan\n", file=sys.stdout)
    for obj in User.objects:
        print(f"   After Save User: {obj.email} \n", file=sys.stdout)
    for obj in CompanyUser.objects:
        print(f"   After Save CompanyUser: {obj.email} \n", file=sys.stdout)

    # Test Snack
    for obj in Snack.objects:
        print(f"    Before Save Snack: {obj.snack_brand} {obj.snack_name} \n", file=sys.stdout)
    # To test it yourself, create a snack with different name and brand from the exisiting snacks in the db
    snack = Snack(snack_name="Crunchy Cheese Flavoured", available_at_locations=["Canada"], snack_brand="Cheetos")
    snack.description = "Yummy yummy"
    try:
        snack.save()
    except Exception as e:
        print("Error \n %s" % e, file=sys.stdout)
    # Display existing snacks in db, your new snack should be here if it has been saved without error
    for obj in Snack.objects:
        print(f"    After Save Snack: {obj.snack_brand} {obj.snack_name} \n", file=sys.stdout)

    # Test MetricReview
    for obj in MetricReview.objects:
        print(f"    Before Save MetricReview: {obj.user_id} {obj.snack_id} {obj.description}\n", file=sys.stdout)
    metric_review = MetricReview(user_id="5bd1377387bec222cc6e6025", snack_id="5bd1377387bec222cc6e6027",
                                 description="ok", geolocation="Canada", overall_rating="3", sourness="1",
                                 spiciness="1")
    try:
        metric_review.save()
    except Exception as e:
        print("Error \n %s" % e, file=sys.stdout)
    for obj in MetricReview.objects:
        print(f"    After Save MetricReview: {obj.user_id} {obj.snack_id} {obj.description}\n", file=sys.stdout)

    # Test Review
    # Display existing reviews in the db
    print(f"a\n", file=sys.stdout)
    for obj in Review.objects:
        print(f"    Before Save Review: {obj.user_id} {obj.snack_id} {obj.description}\n", file=sys.stdout)
    review = Review(user_id="5bd1377387bec222cc6e6026", snack_id="5bd1377387bec222cc6e6027", description="like it",
                    geolocation="Canada", overall_rating="5")
    try:
        review.save()
    except Exception as e:
        print("Error \n %s" % e, file=sys.stdout)
    for obj in Review.objects:
        print(f"    After Save Review: {obj.user_id} {obj.snack_id} {obj.description}\n", file=sys.stdout)
    return 'Hello World!'


@app.route('/register/', methods=["GET", "POST"])
def register():
    # IMPORTANT: Encrypt the password for the increased security.
    encrypted_password = lambda password_as_string: bcrypt.generate_password_hash(password_as_string)
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        email = form.email.data
        # Add user to database.
        try:
            new_user = User(email=form.email.data, first_name=form.first_name.data,
                            last_name=form.last_name.data, password=encrypted_password(form.password.data))
            new_user.save()
        except Exception as e:
            raise Exception(f"Error {e}. \n Couldn't add user {new_user},\n with following registration form: {form}")
        print(f"A new user submitted the registration form: {email}", file=sys.stdout)
        for u in User.objects[:10]:
            print(u)
        print(url_for('index'))
        return redirect(url_for('index'))
    return render_template("register.html", title="Register", form=form)


@app.route("/create-snack")
@login_required
def create_snack():
    # TODO: This is an example of a route which requires the user to authenticate, not a complete implementation.
    # Get snacks from the database.
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
    # For GET requests, display the login form; for POST, log in the current user by processing the form.
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


@app.route("/snack_reviews/<string:snack_id>", methods=['GET'])
def find_reviews_for_snack(snack_id):
    """
    Find all the reviews for a snack.
    To display a table of reviews for a snack_id, enter local/_url/snack_reviews/snack_id in your browser.
    """
    reviews = Review.objects(snack_id=snack_id)
    print(f"snack_reviews: {reviews}", file=sys.stdout)
    if not reviews:
        return "No reviews found"
    else:
        display = ReviewResults(reviews)
        display.border = True
        return render_template('reviews_for_snack.html', table=display)


# TODO: remove after implementing the front end.
class ReviewResults(Table):
    """
    Test class that helps to display the readable snacks data to the front end in the format of a table.
    It allows us to test the backend and html rendering, without having to wait for the implementation
    of the final front end.
    """
    id = Col('Review Id')
    user_id = Col('User ID')
    snack_id = Col('Snack ID')
    description = Col('Description')
    overall_rating = Col('Overall Rating')
    geolocation = Col('Geolocation')
    sourness = Col('sourness')
    spiciness = Col('spiciness')
    bitterness = Col('bitterness')
    sweetness = Col('sweetness')
    saltiness = Col('saltiness')


# TODO: test this
@app.route("/find_snacks?<string:filter>", methods=['GET'])
def find_snack_by_filter(filters):
    """
    Find all snacks given a filter
    /find_snacks?snack_name=abc&available_at_locations=a+b+c&...
    """
    filter_query = {}
    all_filters = filters.split("&")
    available_basic_filters = ['snack_name', 'snack_brand', 'snack_company_name', 'is_verified', 'category']

    for individual_filter in all_filters:
        filter = individual_filter.split("=")
        filter_name = filter[0]
        filter_variable = filter[1]
        if filter_name in available_basic_filters:
            filter_query[filter_name] = filter_variable
        elif filter_name == "available_at_locations":
            filter_query['available_at_locations'] = {"$elemMatch": filter_variable}

    snacks = Snack.objects.find(filter_query)
    print(f"snack_reviews: {snacks}", file=sys.stdout)
    if not snacks:
        return "No snacks founds"
    else:
        display = SnackResults(snacks)
        display.border = True
        # Return the same template as for the review, since it only needs to display a table.
        return render_template('reviews_for_snack.html', table=display)


# TODO: remove after implementing the front end.
class SnackResults(Table):
    """
    Test class that helps to display the readable snacks data to the front end in the format of a table.
    It allows us to test the backend and html rendering, without having to wait for the implementation
    of the final front end.
    """
    id = Col('Snack Id')
    snack_name = Col('snack_name')
    available_at_locations = Col('Location')
    snack_brand = Col('Brand')
    snack_company_name = Col('Company Name')
    photo_files = Col('Photo')
    description = Col('Description')
    is_verified = Col('if verified')
    category = Col('Category')


if __name__ == '__main__':
    app.run()

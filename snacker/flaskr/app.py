import sys
import urllib

import mongoengine as mg
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_bcrypt import Bcrypt
from werkzeug.contrib.fixers import ProxyFix

from forms import RegistrationForm, LoginForm, CreateReviewForm
from schema import *
from util import *

from geodata import get_geodata

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
    mongo_uri = f"mongodb+srv://Jayde:Jayde@csc301-v3uno.mongodb.net/test?retryWrites=true"
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


@app.route("/create-review", methods=["GET", "POST"])
@login_required
def create_review():
    # Create a review and insert it into database.

    # check authenticated
    if current_user.is_authenticated:
        print("is_authenticated")

        review_form = CreateReviewForm(request.form)
        # post to db
        if request.method == "POST" and review_form.validate_on_submit():
            user_id = current_user.id
            # should probably check if user_id is in db

            # snack name and brand
            # query for it
            snacks = Snack.objects
            snack_id = snacks.filter(snack_name=request.snack_name).filter(snack_brand=request.snack_brand)

            # geolocation stuff
            # ip_address = request.access_route[0] or request.remote_addr
            # geodata = get_geodata(ip_address)
            # location = "{}, {}".format(geodata.get("city"),
            #                            geodata.get("zipcode"))

            try:
                # user_id comes from current_user
                # snack_id should come from request sent by frontend
                # geolocation is found by request
                new_review = Review(user_id=user_id, snack_id=snack_id,
                                    description=review_form.description.data,
                                    geolocation="Default", overall_rating=review_form.overall_rating.data)
                new_review.save()

            except Exception as e:
                raise Exception(
                    f"Error {e}. \n Couldn't add review {new_review},\n with following review form: {review_form}")

            print(f"A new user submitted the review form: {user_id}", file=sys.stdout)

            for u in User.objects[:10]:
                print(u)

            return redirect(url_for('index'))
        return render_template("create_review.html", title="Create Review", form=review_form) #frontend stuff

    else:
        return redirect(url_for('index'))


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
    print("LOGGING IN")
    if current_user.is_authenticated:
        print("is_authenticated")
        return redirect(url_for('index'))

    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate_on_submit():
        print("posting")
        user = User.objects(email=form.email.data).first()
        print("user is ", user)
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


# Finished and tested
@app.route("/snack_reviews/<string:filters>", methods=['GET'])
def find_reviews_for_snack(filters):
    """
    Find all reviews given filter
    For overall rating, and the metrics, all reviews with greater or equal to the given value will be returned
    Results currently ordered by descending overall rating
    /snack_reviews/snack_id=abc+overall_rating=3...
    """
    all_filters = filters.split("+")
    print(f"{all_filters}\n", file=sys.stdout)
    queryset = Review.objects
    # all reviews will be returned if nothing specified
    if "=" in filters:
        for individual_filter in all_filters:
            this_filter = individual_filter.split("=")
            if this_filter[0] == "user_id":
                queryset = queryset.filter(user_id=this_filter[1])
            elif this_filter[0] == "snack_id":
                queryset = queryset.filter(snack_id=this_filter[1])
            elif this_filter[0] == "overall_rating":
                queryset = queryset.filter(overall_rating__gte=this_filter[1])
            elif this_filter[0] == "geolocation":
                queryset = queryset.filter(geolocation=this_filter[1])
            elif this_filter[0] == "sourness":
                queryset = queryset.filter(sourness__gte=this_filter[1])
            elif this_filter[0] == "spiciness":
                queryset = queryset.filter(spiciness__gte=this_filter[1])
            elif this_filter[0] == "bitterness":
                queryset = queryset.filter(bitterness__gte=this_filter[1])
            elif this_filter[0] == "sweetness":
                queryset = queryset.filter(sweetness__gte=this_filter[1])
            elif this_filter[0] == "saltiness":
                queryset = queryset.filter(saltiness__gte=this_filter[1])
    queryset = queryset.order_by("-overall_rating")
    print(f"snack_reviews: {queryset}", file=sys.stdout)
    display = ReviewResults(queryset)
    display.border = True
    # Return results in a table, the metrics such as sourness are not displayed because if they are null, they give
    #   the current simple front end table an error, but it is there for use
    return render_template('reviews_for_snack.html', table=display)


# Finished and tested
@app.route("/find_snacks/<string:filters>", methods=['GET'])
def find_snack_by_filter(filters):
    """
    Find all snacks given filter
    Only support searching for one location at a time now (i.e. can't find snacks both in USA and Canada)
    For is verfied, false for false and true for true
    Results currently ordered by snack name
    /find_snacks/snack_name=abc+available_at_locations=a+...
    /find_snacks/all if we want to get all snacks
    """
    all_filters = filters.split("+")
    print(f"{all_filters}\n", file=sys.stdout)
    queryset = Snack.objects

    # the search string should be all if we want to get all snacks, but we can type anything that doesn't include = to
    #   get the same results
    if "=" in filters:
        for individual_filter in all_filters:
            this_filter = individual_filter.split("=")
            if this_filter[0] == "snack_name":
                queryset = queryset.filter(snack_name=this_filter[1])
            elif this_filter[0] == "available_at_locations":
                # Note for this, say if they enter n, they will still return snacks in Canada because their contains
                #   is based on string containment. If order to solve this, we can let force users to select countries
                #   instead of typing countries
                queryset = queryset.filter(available_at_locations__contains=this_filter[1])
            elif this_filter[0] == "snack_brand":
                queryset = queryset.filter(snack_brand=this_filter[1])
            elif this_filter[0] == "snack_company_name":
                queryset = queryset.filter(snack_company_name=this_filter[1])
            elif this_filter[0] == "is_verified":
                if this_filter[1] == "false":
                    queryset = queryset.filter(is_verified=False)
                else:
                    queryset = queryset.filter(is_verified=True)
            elif this_filter[0] == "category":
                queryset = queryset.filter(category=this_filter[1])
    queryset = queryset.order_by("snack_name")
    print(f"snack_reviews: {queryset}", file=sys.stdout)
    display = SnackResults(queryset)
    display.border = True
    # Return the same template as for the review, since it only needs to display a table.
    return render_template('reviews_for_snack.html', table=display)


if __name__ == '__main__':
    app.run()
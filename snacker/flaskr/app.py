import json
import mimetypes
import sys
import urllib

from flask import Flask, render_template, request, flash, redirect, url_for, make_response, Response
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_required, current_user, logout_user, login_user
from mongoengine import connect
from mongoengine.queryset.visitor import Q
from werkzeug.contrib.fixers import ProxyFix

from forms import RegistrationForm, LoginForm, CreateReviewForm, CreateSnackForm, CompanyAddBrandForm, \
    CompanySearchBrandForm, UpdateUserForm, UpdatePasswordForm, CreateBrandForm
from schema import Snack, Review, CompanyUser, User, MetricReview

app = Flask(__name__)

# With these constant strings, we can connect to generic databases
USERNAME_FILE = "username.txt"
PASSWORD_FILE = "password.txt"
DATABASE = "test"
MONGO_SERVER = "csc301-v3uno.mongodb.net"
APP_NAME = "Snacker"

# For snack images
UPLOAD_FOLDER = ""
ALLOWED_FILE_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']

try:
    username = open(USERNAME_FILE, 'r').read().strip().replace("\n", "")
    pw = urllib.parse.quote(open(PASSWORD_FILE, 'r').read().strip().replace("\n", ""))
    print("hello")
    mongo_uri = f"mongodb+srv://Jayde:Jayde@csc301-v3uno.mongodb.net/test?retryWrites=true"
    # mongo_uri = "mongodb://localhost:27017/"
    app.config["MONGO_URI"] = mongo_uri
    mongo = connect(host=mongo_uri)
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
app.url_map.strict_slashes = False


@app.route('/render-img/<string:snack_id>')
def serve_img(snack_id):
    """ Given a snack id, get the image and render it
        Example in file display_snack.html"""
    placeholder = "static/images/CrunchyCheesyFlavouredCheetos.jpg"
    get_mimetype = lambda filename: mimetypes.MimeTypes().guess_type(filename)[0]
    sample_snack = Snack.objects(id=snack_id)[0]
    if sample_snack.photo_files == []:
        return Response(open(placeholder, "rb").read(), mimetype=get_mimetype(placeholder))
    photo = sample_snack.photo_files[0].img
    # resp=Response(photo.read(), mimetype=mimetype)
    # Returning the thumbnail for now
    resp = Response(photo.thumbnail.read(), mimetype=get_mimetype(photo.filename))
    return resp

@app.route("/topkek")
@login_required
def topkek():
    print(current_user.id)
    print(User.objects(pk=current_user.id).first());
    return "Topkek"



@app.route("/")
@app.route("/index")
def index():
    if current_user.is_authenticated:
        print("ok")
    max_show = 5  # Maximum of snacks to show
    snacks = Snack.objects
    popular_snacks = snacks.order_by("-review_count")[:max_show]
    top_snacks = snacks.order_by("-avg_overall_rating")
    featured_snacks = []
    # Getting snacks that have some image to display
    for snack in top_snacks:
        if snack.photo_files:
            featured_snacks.append(snack)
            if len(featured_snacks) == max_show:
                break
    # TODO: Recommend snacks tailored to user
    # featured_snacks = top_snacks

    # Use JS Queries later
    # Needs to be a divisor of 12
    interesting_facts = []
    interesting_facts.append(("Snacks", snacks.count()))
    interesting_facts.append(("Reviews", Review.objects.count()))
    interesting_facts.append(("Five stars given", Review.objects(overall_rating=5).count()))

    snack_names = sorted(list(set(snacks.all().values_list('snack_name'))))
    snack_brands = sorted(list(set(snacks.all().values_list('snack_brand'))))

    context_dict = {"title": "Index",
                    "featured_snacks": featured_snacks,
                    "top_snacks": snacks.order_by("-avg_overall_rating")[:5],
                    "popular_snacks": snacks.order_by("-review_count")[:5],
                    "interesting_facts": interesting_facts,
                    "user": current_user,
                    "snack_names": snack_names,
                    "snack_brands": snack_brands}
    return render_template('index.html', **context_dict)


@app.route("/about")
def about():
    context_dict = {"title": 'About Snacker',
                    "user": current_user}
    return render_template('about.html', **context_dict)


@app.route("/contact")
def contact():
    context_dict = {"title": 'Contact Us',
                    "user": current_user}
    return render_template('contact.html', **context_dict)

""" Routes and methods related to user login and authentication """


@app.route('/register', methods=["GET", "POST"])
def register():
    # IMPORTANT: Encrypt the password for the increased security.
    encrypted_password = lambda password_as_string: bcrypt.generate_password_hash(password_as_string)
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm(request.form)
    if request.method == "POST":
        # Add user to database.
        if request.form['company_name'] != "":
            print(f"company user {form} \n")
            try:
                new_user = CompanyUser(email=request.form['email'], first_name=request.form['first_name'],
                                       last_name=request.form['last_name'], company_name=request.form['company_name'],
                                       password=encrypted_password(request.form['password']))
                new_user.save()
            except Exception as e:
                raise Exception\
                    (f"Error {e}. \n Couldn't add company user {new_user},\n with following registration form: {form}")
        else:
            print(f"normal user {form} \n")
            try:
                new_user = User(email=request.form['email'], first_name=request.form['first_name'],
                                last_name=request.form['last_name'], password=encrypted_password(request.form['password']))
                new_user.save()
            except Exception as e:
                raise Exception\
                    (f"Error {e}. \n Couldn't add user {new_user},\n with following registration form: {form}")
        login_user(new_user, remember=True)
        user = {
            'email': new_user.email,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'company_name': new_user.last_name
        }
        response = make_response(json.dumps(user))
        response.status_code = 200
        print(f"register {response}\n")
        return response

    if request.args.get("email"):
        form.email.data = request.args.get("email")
    context_dict = {"title": "Register",
                    "form": form,
                    "user": current_user}
    return render_template("register.html", **context_dict)


@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()


@app.route("/login", methods=["GET", "POST"])
def login():
    # For GET requests, display the login form; for POST, log in the current user by processing the form.
    print(f"LOGGING IN\n", file=sys.stdout)
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm(request.form)

    if request.method == 'POST':
        user = User.objects(email=request.form['email']).first()
        print(f"user is {user}\n", file=sys.stdout)
        if user is None or not user.check_password(bcrypt, request.form['password']):
            flash("Invalid username or password")
            return redirect(url_for('login'))
        login_user(user, remember=True)
        user = {
            'email': current_user.email,
            'first_name': current_user.first_name,
            'last_name': current_user.last_name,
        }
        if isinstance(current_user, CompanyUser):
            user['company_name'] = current_user.company_name
        else:
            user['company_name'] = None
        response = make_response(json.dumps(user))
        response.status_code = 200
        print(f"login {response}\n")
        return response

    context_dict = {"title": "Sign In",
                    "form": form,
                    "user": current_user}

    return render_template('login.html', **context_dict)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/account", methods=["GET", "POST"])
def account():
    if not current_user.is_authenticated:
        return redirect(url_for("index"))

    context_dict = {"title": "Account",
                    "user": current_user,
                    "edit_user_form": UpdateUserForm(),
                    "edit_password_form": UpdatePasswordForm()}

    if hasattr(current_user, 'company_name'):
        all_snack_brands = []
        company_brands = []
        query_set = []

        for snack in Snack.objects:
            if snack.snack_brand not in all_snack_brands:
                all_snack_brands.append(snack.snack_brand)

        # Remove duplicates
        all_snack_brands = list(set(all_snack_brands))
        company_brands = current_user.company_snackbrands
        all_snack_brands = list(filter(lambda a: a not in company_brands, all_snack_brands))

        all_snack_brands_temp = []
        for snack in all_snack_brands:
            all_snack_brands_temp.append((snack, snack))

        search_company_brands = []
        for snack in company_brands:
            search_company_brands.append((snack, snack))

        all_snack_brands = all_snack_brands_temp
        all_snack_brands.sort()
        search_company_brands.sort()

        default = [("Can't find my brand, create a new brand!", "Can't find my brand, create a new brand!")]
        search_company_brands = default + search_company_brands
        all_snack_brands = default + all_snack_brands

        search_form = CompanySearchBrandForm()
        search_form.search_snack_brand.choices = search_company_brands

        add_form = CompanyAddBrandForm()
        add_form.add_snack_brand.choices = all_snack_brands

        if request.method == "POST" and add_form.validate_on_submit():
            add_snack_brand = add_form.add_snack_brand.data

            if add_snack_brand != "Can't find my brand, create a new brand!":
                try:
                    current_user.update(add_to_set__company_snackbrands=add_snack_brand)
                except Exception as e:
                    raise Exception(
                        f"Error {e}. \n Couldn't add {add_snack_brand},\n with following creation form: {account_form}")
                print(f"A new snack_brand added to company user", file=sys.stdout)

                return redirect(url_for('account'))
            else:
                return redirect(url_for("create_brand"))

        if request.method == "POST" and search_form.validate_on_submit():

            search_snack_brand = search_form.search_snack_brand.data

            if search_snack_brand != "Nothing Selected":
                for snack in Snack.objects:
                    if snack.snack_brand == search_snack_brand:
                        query_set.append(snack)

        context_dict.update({"company_brands": company_brands,
                            "search_form": search_form,
                            "add_form": add_form,
                            "query_set": query_set})

        return render_template('account.html', **context_dict)

    else:
        print("User is not a company user")

        return render_template('account.html', **context_dict)


# Tested
@app.route("/create-brand", methods=["GET", "POST"])
@login_required
def create_brand():
    if current_user.is_authenticated and hasattr(current_user, 'company_name'):
        print(f"User is authenticated", file=sys.stdout)
        create_brand_form = CreateBrandForm(request.form)
        if request.method == "POST":
            snack_brand = create_brand_form.add_snack_brand.data
            try:
                current_user.update(add_to_set__company_snackbrands=snack_brand)
            except Exception as e:
                raise Exception(
                    f"Error {e}. \n Couldn't add {snack_brand},\n with following creation form: {create_brand_form}")
            return redirect(url_for('account'))
        else:
            # For frontend purposes
            context_dict = {"title": "Add Brand",
                            "form": create_brand_form,
                            "user": current_user}

            return render_template("create_brand.html", **context_dict)
    else:
        # Go back to index if not authenticated or if user is not company user
        return redirect(url_for('index'))

#Tested
@app.route("/verify-snack", methods=["POST"])
@login_required
def verify_snack():
    if current_user.is_authenticated and hasattr(current_user, 'company_name'):
        print(f"User is authenticated", file=sys.stdout)

        if request.method == "POST":
            snack_id = request.form["snack_id"]
            snack_object = Snack.objects(id=snack_id)

            company_user_object = CompanyUser.objects(id=current_user.id)
            snack = "snack_id=" + str(snack_id)

            print(snack_id)

            if company_user_object[0].company_name == snack_object[0].snack_company_name:
                try:
                    snack_object.update(set__is_verified=True)
                    print("ayyyyy")

                except Exception as e:
                    raise Exception(
                        f"Error {e}. \n Couldn't verify {snack_id}")
                print(f"The company user verified this snack: {snack_id}", file=sys.stdout)
                return redirect(url_for('find_reviews_for_snack', filters=snack))
            else:
                print(f"User is not the snack's company: {current_user.id}", file=sys.stdout)
                #we want to give the user an error message
                return redirect(url_for('find_reviews_for_snack', filters=snack))

        else:

            return redirect(url_for('find_reviews_for_snack'))
    else:
        # Go back to index if not authenticated or if user is not company user
        return redirect(url_for('index'))

# Tested
# TODO: Need to still add image element
@app.route("/create-snack/<string:selected_brand>", methods=["GET", "POST"])
@login_required
def create_snack(selected_brand):
    # Get snacks from the database.

    if current_user.is_authenticated:
        print(f"User is authenticated", file=sys.stdout)
        create_snack_form = CreateSnackForm(request.form)
        new_snack = None

        selected_brand = selected_brand.split("=")[1]
        print(selected_brand)

        if request.method == "POST":
            snack_brand = request.form['snack_brand']
            snack_name = request.form['snack_name']

            print(f"{snack_name}", file=sys.stdout)

            # Add snack to db
            print(f"{current_user}", file=sys.stdout)
            try:
                new_snack = Snack(snack_name=request.form['snack_name'],
                                  available_at_locations=[request.form['available_at_locations']],
                                  snack_brand=request.form['snack_brand'],
                                  category=request.form['category'],
                                  description=request.form['description'],
                                  is_verified=hasattr(current_user, 'company_name'),
                                  avg_overall_rating=0,
                                  avg_sourness=0,
                                  avg_spiciness=0,
                                  avg_bitterness=0,
                                  avg_sweetness=0,
                                  avg_saltiness=0,
                                  review_count=0
                                  )
                new_snack.save()
            except Exception as e:
                raise Exception(
                    f"Error {e}. \n Couldn't add {new_snack},\n with following creation form: {create_snack_form}")
            print(f"A new snack submitted the creation form: {snack_brand} => {snack_name}", file=sys.stdout)

            return redirect(url_for('index'))

        # For frontend purposes
        context_dict = {"title": "Add Snack",
                        "selected_snack_brand": selected_brand,
                        "form": create_snack_form,
                        "user": current_user}

        return render_template("create_snack.html", **context_dict)
    else:
        # Go back to index if not authenticated
        return redirect(url_for('index'))


@app.route("/create-review/<string:snack>", methods=["POST"])
@login_required
def create_review(snack):

    # check authenticated
    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    print(f"is_authenticated\n", file=sys.stdout)

    review_form = CreateReviewForm(request.form)

    # post to db
    if request.method == "POST":
        user_id = current_user.id
        snack_id = snack.split('=')[1]
        snackObject = Snack.objects(id=snack_id)

        saltiness_review = request.form['saltiness']
        sweetness_review = request.form['sweetness']
        spiciness_review = request.form['spiciness']
        bitterness_review = request.form['bitterness']
        sourness_review = request.form['sourness']
        overall_rating_review = request.form['overall_rating']

        # check if metric review
        if saltiness_review == 0 and sourness_review == 0 and spiciness_review == 0 \
            and bitterness_review == 0 and sweetness_review == 0:

            try:
                # user_id comes from current_user
                # snack_id should come from request sent by frontend
                # geolocation is found by request
                new_review = Review(user_id=user_id, snack_id=snack_id,
                                    description=request.form['description'],
                                    geolocation=request.form['review_country'],
                                    overall_rating=overall_rating_review
                                    )
                new_review.save()

                avg_overall_rating = Review.objects.filter(snack_id=snack_id).average(
                    'overall_rating')

                snackObject.update(set__avg_overall_rating=avg_overall_rating)

                review_count = snackObject[0].review_count + 1
                snackObject.update(set__review_count=review_count)
                if review_count > 10:
                    snackObject.update(set__is_verified=True)
                snackObject.update(add_to_set__available_at_locations=request.form['review_country'])

            except Exception as e:
                raise Exception(
                    f"Error {e}. \n Couldn't add review {new_review},\n with following review form: {review_form}")

            print(f"A new user submitted the review form: {user_id}", file=sys.stdout)
            return redirect(url_for('find_reviews_for_snack', filters=snack))

        else:
            try:
                # user_id comes from current_user
                # snack_id should come from request sent by frontend
                # geolocation is found by request
                snack_metric_review = MetricReview(user_id=user_id, snack_id=snack_id,
                                                   description=request.form['description'],
                                                   geolocation=request.form['review_country'],
                                                   overall_rating=overall_rating_review,
                                                   sourness=sourness_review,
                                                   spiciness=spiciness_review,
                                                   saltiness=saltiness_review,
                                                   bitterness=bitterness_review,
                                                   sweetness=sweetness_review)
                snack_metric_review.save()

                avg_overall_rating = Review.objects.filter(snack_id=snack_id).average('overall_rating')
                avg_sourness = Review.objects.filter \
                    (Q(snack_id=snack_id) & Q(sourness__exists=True)).average("sourness")
                avg_spiciness = Review.objects.filter \
                    (Q(snack_id=snack_id) & Q(spiciness__exists=True)).average("spiciness")
                avg_bitterness = Review.objects.filter \
                    (Q(snack_id=snack_id) & Q(bitterness__exists=True)).average("bitterness")
                avg_sweetness = Review.objects.filter \
                    (Q(snack_id=snack_id) & Q(sweetness__exists=True)).average("sweetness")
                avg_saltiness = Review.objects.filter \
                    (Q(snack_id=snack_id) & Q(saltiness__exists=True)).average("saltiness")

                snackObject.update(set__avg_overall_rating=avg_overall_rating)
                snackObject.update(set__avg_sourness=avg_sourness)
                snackObject.update(set__avg_spiciness=avg_spiciness)
                snackObject.update(set__avg_bitterness=avg_bitterness)
                snackObject.update(set__avg_sweetness=avg_sweetness)
                snackObject.update(set__avg_saltiness=avg_saltiness)

                review_count = snackObject[0].review_count + 1
                snackObject.update(set__review_count=review_count)
                if review_count > 10:
                    snackObject.update(set__is_verified=True)
                snackObject.update(add_to_set__available_at_locations=request.form['review_country'])

            except Exception as e:
                raise Exception(
                    f"Error {e}. \n Couldn't add metric review {snack_metric_review},\n with following review form: {review_form}")

            print(f"A new user submitted the review form: {user_id}", file=sys.stdout)
            return redirect(url_for('find_reviews_for_snack', filters=snack))

    context_dict = {"title": "Create Review",
                    "form": review_form,
                    "user": current_user}
    # frontend stuff
    return render_template("reviews_for_snack.html", **context_dict)


# Finished and tested
@app.route("/snack_reviews/<string:filters>", methods=['GET', 'POST'])
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
    snack_query = None
    reviewed = False
    verified = False
    # all reviews will be returned if nothing specified
    if "=" in filters:
        for individual_filter in all_filters:
            this_filter = individual_filter.split("=")
            query_index = this_filter[0]
            query_value = this_filter[1]
            if query_index == "user_id":
                queryset = queryset.filter(user_id=query_value)
            elif query_index == "snack_id":
                queryset = queryset.filter(snack_id=query_value)
                snack_query = Snack.objects(id=query_value)
                if Snack.objects(id=query_value)[0].is_verified:
                    verified = True
            elif query_index == "overall_rating":
                queryset = queryset.filter(overall_rating__gte=query_value)
            elif query_index == "geolocation":
                queryset = queryset.filter(geolocation=query_value)
            elif query_index == "sourness":
                queryset = queryset.filter(sourness__gte=query_value)
            elif query_index == "spiciness":
                queryset = queryset.filter(spiciness__gte=query_value)
            elif query_index == "bitterness":
                queryset = queryset.filter(bitterness__gte=query_value)
            elif query_index == "sweetness":
                queryset = queryset.filter(sweetness__gte=query_value)
            elif query_index == "saltiness":
                queryset = queryset.filter(saltiness__gte=query_value)
    queryset = queryset.order_by("-overall_rating")
    print(f"snack_reviews: {queryset}", file=sys.stdout)
    print(f"snack_reviews: {snack_query}", file=sys.stdout)
    review_form = CreateReviewForm(request.form)

    if current_user.is_authenticated:
        if len(queryset.filter(user_id=current_user.id)):
            reviewed = True

    # Return results in a table, the metrics such as sourness are not displayed because if they are null, they give
    #   the current simple front end table an error, but it is there for use

    context_dict = {"title": "Delicious Snack",
                    "form": review_form,
                    "query": snack_query,
                    "reviews": queryset,
                    "reviewed": reviewed,
                    "verified": verified,
                    "user": current_user}
    return render_template('reviews_for_snack.html', **context_dict)


# Finished and tested
@app.route("/find_snacks/<string:filters>", methods=['GET'])
def find_snack_by_filter(filters):
    """
    Find all snacks given filter
    Only support searching for one location at a time now (i.e. can't find snacks both in USA and Canada)
    For is verfied, false for false and true for true
    Results currently ordered by snack name
    For snack name, it will return all snacks that contain the string given by snack_name instead of only returning the
        snacks with exactly the same name
    /find_snacks/snack_name=abc+available_at_locations=a+...
    /find_snacks/all if we want to get all snacks
    """
    all_filters = filters.split("+")
    print(f"{all_filters}\n", file=sys.stdout)
    queryset = Snack.objects

    # the search string should be all if we want to get all snacks, but we can type anything that doesn't include '='
    # to get the same results
    if "=" in filters:
        for individual_filter in all_filters:
            this_filter = individual_filter.split("=")
            query_index = this_filter[0]
            query_value = this_filter[1]
            if query_index == "snack_name":
                # Change to contain so that snacks with similar name to inputted name will be returned too
                if query_value != "":
                    queryset = queryset.filter(snack_name__contains=query_value)
            elif query_index == "available_at_locations":
                # Note for this, say if they enter n, they will still return snacks in Canada because their contains
                #   is based on string containment. If order to solve this, we can let force users to select countries
                #   instead of typing countries
                if query_value != "all":
                    queryset = queryset.filter(available_at_locations__contains=query_value)
            elif query_index == "snack_brand":
                if query_value != "":
                    queryset = queryset.filter(snack_brand=query_value)
            elif query_index == "snack_company_name":
                queryset = queryset.filter(snack_company_name=query_value)
            elif query_index == "is_verified":
                if query_value == "false":
                    queryset = queryset.filter(is_verified=False)
                else:
                    queryset = queryset.filter(is_verified=True)
            elif query_index == "category":
                queryset = queryset.filter(category=query_value)
    queryset = queryset.order_by("snack_name")
    print(f"snack_reviews: {queryset}", file=sys.stdout)
    # TODO: What are the comments below?!
    # display = SnackResults(queryset)
    # display.border = True

    context_dict = {"title": "Search Results",
                    "query": queryset,
                    "user": current_user}
    # Return the same template as for the review, since it only needs to display a table.
    return render_template('search_query.html', **context_dict)


@app.route("/my_list", methods=['GET'])
def find_wishlist():
    """
    Return all snacks in wishlist of current user
    """
    result = []
    for i in range(len(current_user.wish_list)):
        result.extend(Snack.objects(id=current_user.wish_list[i]))
    print(f"{result}\n", file=sys.stdout)
    title = "Wishlist"

    if hasattr(current_user, 'company_name'):
        title = "Watchlist"

    context_dict = {"title": title,
                    "query": result,
                    "user": current_user}
    # Return the same template as for the review, since it only needs to display a table.
    return render_template('my_list.html', **context_dict)


if __name__ == '__main__':
    app.run()

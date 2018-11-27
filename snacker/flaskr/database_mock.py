import json
import string
import random as rnd
#import requests as req
#import matplotlib.pyplot as plt
#import matplotlib.mlab as mlab
import math
import numpy as np

#@app.route("/add-snacks")
def add_snacks():
    # Open database and parse json
    my_database = mongo[DATABASE]
    my_file = open("snacks/snacks.json", "rb")
    parsed = json.loads(my_file.read().decode('unicode-escape'))
    snacks = parsed
    s = snacks
    # For demonstration purposes, this delete every entry in the Snack collection
    for s in snacks:
        new_snack = Snack(snack_name=s["title"],
                          available_at_locations=[s["country"]])
        if s.get("description"):
            new_snack.description = s["description"]
        if s.get("company"):
            new_snack.snack_brand = s["company"]
        else:
            continue
        new_snack.avg_overall_rating = 0
        new_snack.avg_bitterness = 0
        new_snack.avg_saltiness = 0
        new_snack.avg_sourness = 0
        new_snack.avg_spiciness = 0
        new_snack.avg_sweetness = 0
        new_snack.review_count = 0
        # Insert images read from folder (snacks/image/snack_name)
        if s.get("folder_name"):
            i = SnackImage()
            for entry in os.scandir("snacks/image/"+s.get("folder_name")):
                with open(entry.path, "rb") as image_file:
                    img_name = os.path.basename(image_file.name)
                    i.img.put(image_file, filename=img_name)

                new_snack.photo_files.append(i)
        # Save the new snacks into the database
        try:
            new_snack.save()
        except Exception as e:
            print("Error \n %s" % e, file=sys.stdout)
    # Retrieving snacks from database
    max_show = 100  # Maximum number of snacks to send to view
    sl = []
    for s in Snack.objects[:max_show]:
        if s.photo_files:
            sl.append(s)
            for file in s.photo_files:
                photo = file.img
                # Guess the type of the mimetype to send a good response
                # mimetype = mimetypes.MimeTypes().guess_type(photo.filename)[0]
                # resp=Response(photo.read(), mimetype=mimetype)
                # photo.read() # This is image itself
                # photo.filename # This is the name of the image
                # photo.format # This is the format of the image (png, jpg, etc)
                # photo.thumbnail.read() # This is the thumbnail of the image
    print("Finished.")
    print(f"{len(sl)}")
    return str(sl[:10])

#@app.route("/add-reviews")
def add_reviews():
    """add_reviews
    Get all snacks from the database, clusterized by category.
    Get all users from the database.
    Generate ~400k of reviews and commit them to the database,
    according to a specific user profile (the predefined user behavior).
    Then, saves the user behavior in a file in snacks/users_snack_profiles.json
    
    """

    snack_from_db = Snack.objects
    cluster = dbmock.cluster_snacks(snack_from_db)
    salty  = cluster["salty"]
    spicy  = cluster["spicy"]
    sour   = cluster["sour"]
    sweet  = cluster["sweet"]
    bitter = cluster["bitter"]
    remaining_snacks = cluster["remaining_snacks"]
    def get_random_category():
        return cluster[rnd.choice(("salty", "spicy", "sour", "sweet", "bitter", "remaining_snacks"))]
    users = list(User.objects)
    rnd.shuffle(users)
    num_users = len(users)
    # Comparators for the user profile
    is_salty = lambda idx : idx < num_users*.14
    is_spicy = lambda idx : idx < num_users*(.14*2)
    is_sour = lambda idx : idx < num_users*(.14*3)
    is_sweet = lambda idx : idx < num_users*(.14*4)
    is_bitter = lambda idx : idx < num_users*(.14*5)
    is_mixed_spicy_sweet = lambda idx : idx < num_users*.8
    is_mixed_sweet_sour = lambda idx : idx < num_users*.9
    is_mixed_salty_sour = lambda idx : True
    user_profile = { "salty" : [],
                      "spicy" : [],
                      "sour" : [],
                      "sweet" : [],
                      "bitter" : [],
                      "mixed_spicy_sweet" : [],
                      "mixed_sweet_sour" : [],
                      "mixed_salty_sour" : []}
    for user, idx in zip(users, range(num_users)):
        if is_salty(idx):
            add_custom_reviews(user, salty, num=60, snack_type="salty")
            add_custom_reviews(user, get_random_category(), num=22)
            user_profile["salty"].append((user.id, user.email, user.first_name, user.last_name))
        elif is_spicy(idx):
            add_custom_reviews(user, salty, num=60, snack_type="spicy")
            add_custom_reviews(user, get_random_category(), num=22)
            user_profile["spicy"].append((user.id, user.email, user.first_name, user.last_name))
        elif is_sour(idx):
            add_custom_reviews(user, salty, num=60, snack_type="sour")
            add_custom_reviews(user, get_random_category(), num=22)
            user_profile["sour"].append((user.id, user.email, user.first_name, user.last_name))
        elif is_sweet(idx):
            add_custom_reviews(user, salty, num=60, snack_type="sweet")
            add_custom_reviews(user, get_random_category(), num=22)
            user_profile["sweet"].append((user.id, user.email, user.first_name, user.last_name))
        elif is_bitter(idx):
            add_custom_reviews(user, salty, num=60, snack_type="bitter")
            add_custom_reviews(user, get_random_category(), num=22)
            user_profile["bitter"].append((user.id, user.email, user.first_name, user.last_name))
        elif is_mixed_spicy_sweet(idx):
            add_custom_reviews(user, spicy, num=25, snack_type="salty")
            add_custom_reviews(user, sweet, num=25, snack_type="sweet")
            add_custom_reviews(user, remaining_snacks, num=30)
            user_profile["mixed_spicy_sweet"].append((user.id, user.email, user.first_name, user.last_name))
        elif is_mixed_sweet_sour(idx):
            add_custom_reviews(user, spicy, num=25, snack_type="sweet")
            add_custom_reviews(user, sweet, num=25, snack_type="sour")
            add_custom_reviews(user, remaining_snacks, num=30)
            user_profile["mixed_sweet_sour"].append((user.id, user.email, user.first_name, user.last_name))
        elif is_mixed_salty_sour(idx):
            add_custom_reviews(user, spicy, num=25, snack_type="salty")
            add_custom_reviews(user, sweet, num=25, snack_type="sour")
            add_custom_reviews(user, remaining_snacks, num=30)
            user_profile["mixed_salty_sour"].append((user.id, user.email, user.first_name, user.last_name))
        if idx%100 == 0:
            print(f"Finish user {user.first_name}, index = {idx} out of {len(users)}")
    print(f"Number of users = {len(users)}")
    print(f"Number of snacks = {len(users)}")
    # Save user list profile to a json file
    with open("snacks/users_snack_profiles.json", "rb") as user_prof_file:
        json.dump(user_profile, user_prof_file)
    return "no reviews added!"

def add_custom_reviews(user, list_of_snacks, num=1, snack_type="", good_rating=True):
    # Considering that this user is loves snacks of the current list
    # Will add 'num' of new reviews, from 3.5 to 4, following a normal distribution, kinda
    # Round numbers to valid range, in a norm distr. (with normal distribution, we never know :] )
    def round_valid(mu, sigma):
        val = int(round(rnd.normalvariate(mu, sigma)))
        val = val if val <= 5 else 5
        val = val if val >= 1 else 1
        return val
    list_of_snacks = rnd.sample(list_of_snacks, num)
    for snack in list_of_snacks:
        if good_rating:
            rating = round_valid(4.2, .6) # Give a good rating
        else:
            rating = round_valid(3, 1.1) # Give a more uniform rating
        # Keeps the geolocation the same of the first available location at the snack
        if snack.available_at_locations:
            geoloc = snack.available_at_locations[0]
        else:
            geoloc = "Canada"
        if snack_type == "salty":
            saltiness_review = round_valid(4.4, .7) # is salty
            spiciness_review = round_valid(3, 1.1) # not very related
            sourness_review = round_valid(1, 1.1) # Not so much sour
            sweetness_review = round_valid(2, .6) # Things which are salty tend not to be sweet
            bitterness_review = round_valid(2, 1.1) # Less bitter
        elif snack_type == "spicy":
            saltiness_review = round_valid(3, 1.1) # not very related
            spiciness_review = round_valid(4.4, .7) # is spicy
            sourness_review = round_valid(2, 1.1) # Not so much sour
            sweetness_review = round_valid(2, .6) # Not so much sweet
            bitterness_review = round_valid(2, 1.1) # Less bitter
        elif snack_type == "sour":
            saltiness_review = round_valid(1, 1.1) # Not so much salty
            spiciness_review = round_valid(2, 1.1) # Not so much spicy
            sourness_review = round_valid(4.4, .7) # is sour
            sweetness_review = round_valid(3, 1.1) # not very related but can vary
            bitterness_review = round_valid(4, 1.1) # Tend to be bitter
        elif snack_type == "sweet":
            saltiness_review = round_valid(2, .6) # Things which are sweet tend not to be salty
            spiciness_review = round_valid(2, .6) # Not so much spicy
            sourness_review = round_valid(3, 1.1) # not very related but can vary
            sweetness_review = round_valid(4.4, .7) # is sweet
            bitterness_review = round_valid(2, 1.1) # Less bitter
        elif snack_type == "bitter":
            saltiness_review = round_valid(2, 1.1) # Less bitter
            spiciness_review = round_valid(3, 1.1) # Can be spicy
            sourness_review = round_valid(4, 1) # Tend to somewhat relate to sour
            sweetness_review = round_valid(2, 1.1) # Not so much sweet
            bitterness_review = round_valid(4.4, .7) # is bitter
        else:
            # add normal review to the database if it's not any particular profile
            commit_normal_review_database(user, snack, geoloc=geoloc, rating=rating)
            continue
        #print(f"{user}, {snack}, geoloc={geoloc}, rating={rating}, saltiness_review={saltiness_review}, spiciness_review={spiciness_review}, sourness_review={sourness_review},sweetness_review={sweetness_review}, bitterness_review={bitterness_review}")
        commit_metric_review_database(user, snack, geoloc=geoloc, rating=rating, saltiness_review=saltiness_review,
                               spiciness_review=spiciness_review, sourness_review=sourness_review,
                               sweetness_review=sweetness_review, bitterness_review=bitterness_review)


def commit_normal_review_database(user, snack, geoloc="Canada", rating=1):
    user_id = user.id
    snack_id = snack.id
    """ Commit a given review to the database, and don't raise any exceptions
        if it fails (only print a notification message).
        IMPORTANT: The review should be a normal (without metrics) review!"""
    try:
        new_review = Review(user_id=user_id, snack_id=snack_id,
                            geolocation=geoloc,
                            overall_rating=rating)
        new_review.save()

        avg_overall_rating = Review.objects.filter(snack_id=snack_id).average('overall_rating')

        snack.update(set__avg_overall_rating=avg_overall_rating)

        review_count = snack.review_count + 1
        snack.update(set__review_count=review_count)
        if review_count > 10:
            snack.update(set__is_verified=True)
        snack.update(add_to_set__available_at_locations=geoloc)

    except:
        print(f" Couldn't add review {new_review}")

def commit_metric_review_database(user, snack, geoloc="Canada", rating=1, saltiness_review=1,
                      spiciness_review=1, sourness_review=1, sweetness_review=1,
                      bitterness_review=1):
    """ Commit a given review to the database, and don't raise any exceptions
        if it fails (only print a notification message).
        IMPORTANT: The review should be a metric review!"""
    user_id = user.id
    snack_id = snack.id
    try:
        snack_metric_review = MetricReview(user_id=user_id, snack_id=snack_id,
                                            geolocation=geoloc,
                                            overall_rating=rating,
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

        snack.update(set__avg_overall_rating=avg_overall_rating)
        snack.update(set__avg_sourness=avg_sourness)
        snack.update(set__avg_spiciness=avg_spiciness)
        snack.update(set__avg_bitterness=avg_bitterness)
        snack.update(set__avg_sweetness=avg_sweetness)
        snack.update(set__avg_saltiness=avg_saltiness)

        review_count = snack.review_count + 1
        snack.update(set__review_count=review_count)
        if review_count > 10:
            snack.update(set__is_verified=True)
        snack.update(add_to_set__available_at_locations=geoloc)
    except:
        print(f"Couldn't add metric review {snack_metric_review}!!")



def cluster_snacks(all_snacks):
    """
    Receives the list of all snacks from the database, them cluster them
    using predefined key words!
    """
    country2snacks = {}
    salty = []  # ~943
    spicy = []  # ~525
    sour = []  # ~453
    sweet = []  # ~967
    bitter = []  # ~307
    # Snacks that don't pertain to any category
    remaining_snacks = [] # ~516
    salty_kwords = ("salty", "chips", "cracker", "grain", "grains",
                    "cheese", "cheddar", "doritos", "potato", "bacon", "sticks")
    spicy_kwords = ("spicy",  "pepper", "onion", "jalapeno", "chipotle", "salsa", "hummus", "dip", "quesadillas", "chilli"
                    "tacos", "sriracha", "hot", "garlic", "pimiento", "guacamole", "spice", "salsa", "wasabi",
                    "pimenta", "apimentado", "taco")
    sour_kwords = ("sour", "almold", "cranberry", "cherry", "lemon", "citric", "orange", "vinegar", "apple", "limes", "kimchi",
                   "tamarind", "mustard", "guava", "gooseberry", "pickles", "yogurt", "soy", "popcorn", "garlic", "fire", "angry",
                   "limón", "limão")
    sweet_kwords = ("sweet", "cream", "chocolate", "tart", "berry", "peanut", "nut", "oreo", "cookie", "macadamia", "cake", "cherry",
                    "pretzel", "frosted", "treats", "pumpkin", "sugar", "candy", "doce", "butter", "cinnamon", "caramel", "fruit",
                    "glazed", "toffee")
    bitter_kwords = ("bitter", "coffee", "tomato", "dill", "ginger", "gengibre", "peppermint", "mint", "citrus", "aspargus", "lemon",
                     "lime", "cocoa", "cacao", "cacau", "dark", "wine", "beer", "dandelion", "eggplant", "karela",
                     "gourd")
    for s in all_snacks:
        found_category = False
        for country in s["available_at_locations"]:
            if country2snacks.get(country) == None:
                country2snacks[country] = [s]
            else:
                country2snacks[country].append(s)
        if s.description and any((kword in s.description.lower()+" "+s.snack_name.lower() for kword in salty_kwords)):
            salty.append(s)
            found_category = True
        if s.description and any((kword in s.description.lower()+" "+s.snack_name.lower() for kword in spicy_kwords)):
            spicy.append(s)
            found_category = True
        if s.description and any((kword in s.description.lower()+" "+s.snack_name.lower() for kword in sour_kwords)):
            sour.append(s)
            found_category = True
        if s.description and any((kword in s.description.lower()+" "+s.snack_name.lower() for kword in sweet_kwords)):
            sweet.append(s)
            found_category = True
        if s.description and any((kword in s.description.lower()+" "+s.snack_name.lower() for kword in bitter_kwords)):
            bitter.append(s)
            found_category = True
        if not found_category:
            remaining_snacks.append(s)
    # Sort by quantity
    """ sorted_country2snacks = sorted(
        country2snacks.items(), key=lambda el: -len(el[1]))
    for s in sorted_country2snacks[0][:10]:
        print(s)

    for s in sorted_country2snacks:
        print(f"{s[0]} - {len(s[1])}") """

    return {"salty": salty,
            "spicy": spicy,
            "sour": sour,
            "sweet": sweet,
            "bitter": bitter,
            "remaining_snacks": remaining_snacks}

def process_user_api():
    api_url = "https://randomuser.me/api/?results=5000&nat=AU,BR,CA,CH,DE,DK,ES,FI,FR,GB,IE,NO,NL,NZ,US&inc=name,nat,email&noinfo"
    header = {'User-Agent': 'Mozilla/5.0'}
    # Get list of users from the api and parse json
    response_json = req.get(api_url, headers=header).json()["results"]
    def update_name(el):
        el["name"]["first"] = el["name"]["first"][0].upper() + el["name"]["first"][1:]
        el["name"]["last"] = el["name"]["last"][0].upper() + el["name"]["last"][1:]
        return el
    response_json = list(map(update_name, response_json))
    with open("snacks/users.json", "w") as user_file:
        json.dump(response_json, user_file)
    print("Finished")


def format_mocked_users():
    my_file = open("snacks/users.json", "rb")
    users = json.loads(my_file.read().decode('unicode-escape'))
    parsed_users = []
    printable = set(string.printable) # valid chars for a filename, to filter email
    for u in users:
        user_formatted = {"first_name": u["name"]["first"],
         "last_name": u["name"]["last"],
         "email": "".join(list(filter(lambda x: x in printable, u["email"]))),
         "password": 123456,
         "is_verified": True
        }
        parsed_users.append(user_formatted)
    return parsed_users

def gen_normal_plot(mu, variance, label=""):
    """ Given a mean and a variance, plot the normal distribution
        in matplotlib, filling the space below the curve, and
        adding the correct label to the plot"""
    sigma = math.sqrt(variance)
    x = np.linspace(-4*sigma + mu, 4*sigma + mu, 100)
    y = mlab.normpdf(x, mu, sigma)
    if label:
        plt.plot(x, y, label=label)
    ax = plt.gca()
    ax.fill_between(x, 0, y, alpha=0.5)
    plt.legend()

def generate_graph():
    """ Generate all 5 base user profile normal distribution plots!"""
    gen_normal_plot(4.4, .7, "Saltiness")
    gen_normal_plot(3, 1.1,  "Spiciness")
    gen_normal_plot(1, 1.1,  "Sourness")
    gen_normal_plot(2, .6,   "Sweetness")
    gen_normal_plot(2, 1.1,  "Bitterness")
    plt.title("Salty user profile")
    plt.show()
    gen_normal_plot(3, 1.1, "Saltiness")
    gen_normal_plot(4.4, .7, "Spiciness")
    gen_normal_plot(2, 1.1, "Sourness")
    gen_normal_plot(2, .6, "Sweetness")
    gen_normal_plot(2, 1.1, "Bitterness")
    plt.title("Spicy user profile")
    plt.show()
    gen_normal_plot(1, 1.1, "Saltiness")
    gen_normal_plot(2, 1.1, "Spiciness")
    gen_normal_plot(4.4, .7, "Sourness")
    gen_normal_plot(3, 1.1, "Sweetness")
    gen_normal_plot(4, 1.1, "Bitterness")
    plt.title("Sour user profile")
    plt.show()
    gen_normal_plot(2, .6, "Saltiness")
    gen_normal_plot(2, .6, "Spiciness")
    gen_normal_plot(3, 1.1, "Sourness")
    gen_normal_plot(4.4, .7, "Sweetness")
    gen_normal_plot(2, 1.1, "Bitterness")
    plt.title("Sweet user profile")
    plt.show()
    gen_normal_plot(2, 1.1, "Saltiness")
    gen_normal_plot(3, 1.1, "Spiciness")
    gen_normal_plot(4, 1, "Sourness")
    gen_normal_plot(2, 1.1, "Sweetness")
    gen_normal_plot(4.4, .7, "Bitterness")
    plt.title("Bitter user profile")
    plt.show()

if __name__ == "__main__":
    pass

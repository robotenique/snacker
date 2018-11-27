import json
import string
import random as rnd
import requests as req

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
""" ''
        user_id = current_user.id
        snack_id = snack.split('=')[1]
        snackObject = Snack.objects(id=snack_id)
        saltiness_review = 1
        sweetness_review = 1
        spiciness_review = 1
        bitterness_review = 1
        sourness_review = 1
        overall_rating_review = 3.2

        # check if metric review

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
 """
if __name__ == "__main__":
    format_mocked_users()

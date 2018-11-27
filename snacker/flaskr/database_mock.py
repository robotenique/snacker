import json
import random as rnd


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
        for country in s["available_at_locations"]:
            if country2snacks.get(country) == None:
                country2snacks[country] = [s]
            else:
                country2snacks[country].append(s)
        if s.description and any((kword in s.description.lower()+" "+s.snack_name.lower() for kword in salty_kwords)):
            salty.append(s)
        if s.description and any((kword in s.description.lower()+" "+s.snack_name.lower() for kword in spicy_kwords)):
            spicy.append(s)
        if s.description and any((kword in s.description.lower()+" "+s.snack_name.lower() for kword in sour_kwords)):
            sour.append(s)
        if s.description and any((kword in s.description.lower()+" "+s.snack_name.lower() for kword in sweet_kwords)):
            sweet.append(s)
        if s.description and any((kword in s.description.lower()+" "+s.snack_name.lower() for kword in bitter_kwords)):
            bitter.append(s)
    print(len(salty))
    print(len(spicy))
    print(len(sour))
    print(len(sweet))
    print(len(bitter))
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
            "bitter": bitter}

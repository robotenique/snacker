Using mongoengine ImageField - Snacks
========================
How to: 
1. Parse json snack object
2. open the image and add the image into the Model
3. save the new data
4. Iterate and access the snacks and images from the mongodb


```python
@app.route("/display-snack")
@login_required
def display_snack():
    # Open database and parse json
    my_database = mongo[DATABASE]
    my_file = open("snacks/snacks.json", "rb")
    parsed = json.loads(my_file.read().decode('unicode-escape'))
    snacks = parsed
    s = snacks
    # For demonstration purposes, this delete every entry in the Snack collection
    Snack.objects.delete()
    for s in snacks:
        new_snack = Snack(snack_name=s["title"], available_at_locations=[s["country"]])
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
    max_show = 100 # Maximum number of snacks to send to view
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
                # photo.thumbnail.read() # This is the thumbnail of the image """
    print("Finished.")
    print(f"{len(sl)}")
    return render_template('display_snack.html', snack_list=sl)
```
The snack image (the first one) is served through the route ```serve_img(snack_id)```, which receives a snack id and return the first **thumbnail** stored in that snack (if it has one).

In the view (*.html file) you call it like this, assuming you have a ```snack``` object (from class Snack):

```html
<!-- You can use it in the CSS -->
<a href="#" class="" style="background-image: url({{ url_for('serve_img', snack_id=snack.id) }})">
<!-- You can use it in the img tag directly -->
 <img class="query-img" src={{ url_for('serve_img', snack_id=snack.id) }} style="float: left">
```


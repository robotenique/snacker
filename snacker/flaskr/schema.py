from flask_login import UserMixin
from mongoengine import Document, EmailField, StringField, ImageField, BooleanField, ListField, IntField, DecimalField, \
    ObjectIdField, EmbeddedDocument, EmbeddedDocumentListField

# An unique ID (user.id) is automatically created.
# Date of registration comes with automatic _id (automatic timestamp: getTimestamp()).

""" Model classes for the User """


class User(UserMixin, Document):
    email = EmailField(required=True, unique=True)
    first_name = StringField(required=True)
    last_name = StringField(required=True)

    # Image size can be specified in ImageField().
    avatar_file = ImageField(upload_to='avatars')

    # User has to verify his email address, before he becomes a verified user.
    is_verified = BooleanField(required=True, default=False)
    password = StringField(max_length=255, required=True, db_field='password')
    wish_list = ListField(IntField())
    authenticated = BooleanField(default=False)
    meta = {'allow_inheritance': True}

    def is_authenticated(self):
        return self.authenticated

    def __str__(self):
        return f"[\n\tEmail: {self.email}\n\tfirst_name: {self.first_name}\n\tpw: {self.password}\n]"

    def __repr__(self):
        return f"[\n\tEmail: {self.email}\n\tfirst_name: {self.first_name}\n\tpw: {self.password}\n]"

    def check_password(self, bcrypt, password):
        return bcrypt.check_password_hash(self.password, password)


# Every CompanyUser is a User as well.
# We can directly get all the CompanyUsers.
class CompanyUser(User):
    company_name = StringField(required=True, unique=True, sparse=True)
    company_snackbrands = ListField(StringField(max_length=100))


""" Model classes for the Snacks """


class SnackImage(EmbeddedDocument):
    # Image size can be specified in ImageField().
    img = ImageField(thumbnail_size=(260, 300, True), upload_to='snack_photos')


# An unique ID is automatically created (snack.id).
class Snack(Document):
    snack_name = StringField(required=True)
    # Countries where the snacks have been reviewed in or is available at.
    available_at_locations = ListField(StringField(), required=True)
    snack_brand = StringField(required=True, unique_with="snack_name")
    snack_company_name = StringField()
    photo_files = EmbeddedDocumentListField(SnackImage)
    description = StringField()
    is_verified = BooleanField(required=True, default=False)
    category = StringField()
    review_count = IntField()
    avg_overall_rating = DecimalField()
    avg_sourness = DecimalField()
    avg_spiciness = DecimalField()
    avg_bitterness = DecimalField()
    avg_sweetness = DecimalField()
    avg_saltiness = DecimalField()


# An unique ID is automatically created (review.id).
# Timestamp comes with the automatic id (getTimestamp()).
class Review(Document):
    # ID of user who wrote the review.
    user_id = ObjectIdField(required=True)
    # ID of snack that the review is being written for. User can review a snack only once.
    snack_id = ObjectIdField(required=True)
    description = StringField()
    overall_rating = IntField(required=True)
    # Name of the country, where the snack is being reviewed.
    geolocation = StringField(required=True)
    meta = {'allow_inheritance': True}


# Every MetricReview is a Review as well.
# We can directly get all the MetricReviews.
class MetricReview(Review):
    sourness = IntField()
    spiciness = IntField()
    bitterness = IntField()
    sweetness = IntField()
    saltiness = IntField()

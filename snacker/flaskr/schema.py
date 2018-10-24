from mongoengine import *


# An user of our app
# An unique ID should be automatically created, should be able to refer to it as user._id
# Date of registration is not needed since with automatic _id, it comes with automatic timestamp: getTimestamp()
class User(Document):
    email = EmailField(required=True, unique=True)
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    # You can mess with img size here
    avatar_file = ImageField()
    # If the email has been verified, even for regular users we need to verify email
    is_verified = BooleanField(required=True, default=False)
    wish_list = ListField(IntField())
    meta = {'allow_inheritance': True}


# Every CompanyUser will be user as well, we can also directly get all CompanyUsers
class CompanyUser(User):
    company_name = StringField(required=True, unique=True)
    company_snackbrands = ListField(StringField(max_length=100))


# A snack
# An unique ID should be automatically created, should be able to refer to it as snack._id
class Snack(Document):
    snack_name = StringField(required=True, unique_with='snack_brand')
    # Countries where the snacks have been reviewed
    available_at_locations = ListField(StringField(), required=True)
    snack_brand = StringField(required=True, unique_with='snack_name')
    snack_company_name = StringField()
    # Can mess with img size here
    photo_files = ListField(ImageField())
    description = StringField()
    is_verified = BooleanField(required=True, default=False)
    category = StringField()


# A review of a snack
# An unique ID should be automatically created, should be able to refer to it as review._id
# Timestamp is not needed since with automatic _id, it comes with automatic timestamp: getTimestamp()
class Review(Document):
    # ID of user who wrote the review
    user_id = ObjectIdField(required=True)
    # ID of snack that the review is being written about
    snack_id = ObjectIdField(required=True)
    description = StringField()
    overall_rating = IntField(required=True)
    # Name of country
    geolocation = StringField(required=True)
    meta = {'allow_inheritance': True}


# Every MetricReview will be review as well, we can also directly get all metric reviews
class MetricReview(Review):
    sourness = IntField()
    spiciness = IntField()
    bitterness = IntField()
    sweetness = IntField()
    saltiness = IntField()

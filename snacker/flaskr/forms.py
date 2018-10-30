import pycountry
from flask_wtf import FlaskForm
from mongoengine import IntField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError, NumberRange

from schema import User


class RegistrationForm(FlaskForm):
    first_name = StringField("First Name", [DataRequired(), Length(min=2, max=100)])
    last_name = StringField("Last Name", [DataRequired(), Length(min=2, max=100)])
    email = StringField("Email Address", [
        Email("Invalid email address provided"),
        Length(min=6, max=100),
        DataRequired("Please provide an email address"),
    ])
    is_company = BooleanField("Are you a company or a distributor?")
    password = PasswordField("New Password (maximum length is 50)", [
        DataRequired(),
        Length(max=50),
        EqualTo("confirm", message="Passwords don't match")
    ])
    confirm = PasswordField("Repeat Password", [DataRequired()])
    accept_tos = BooleanField("I accept the Terms of Service and Privacy Notice", [DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_email(self, field):
        """Prevent multiple users from having the same email address"""
        user = User.objects(email=field.data).first()
        if user is not None:
            raise ValidationError("This email is already registered, please use another email address")


class LoginForm(FlaskForm):
    email = StringField("Email Address", [
        Email("Invalid email address provided"),
        Length(min=6, max=100),
        DataRequired("Please use your email address to login")
    ])
    password = PasswordField("Password", [DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class CreateReviewForm(FlaskForm):
    # user_id = ObjectIdField("User Id", [DataRequired(), ])
    # snack_id = ObjectIdField("Snack Id", [DataRequired(), ])
    # geolocation = ("First Name", [DataRequired(), Length(min=2, max=100)])
    # above comes from backend

    description = StringField("Review Description", [Length(min=2, max=255)])
    overall_rating = IntField("Overall Rating", [DataRequired(), NumberRange(min=1, max=5)])
    sourness = IntField(NumberRange(min=1, max=5))
    spiciness = IntField(NumberRange(min=1, max=5))
    bitterness = IntField(NumberRange(min=1, max=5))
    sweetness = IntField(NumberRange(min=1, max=5))
    saltiness = IntField(NumberRange(min=1, max=5))
    submit = SubmitField('Submit Review')


class CreateSnackForm(FlaskForm):
    snack_name = StringField("Snack Name", [DataRequired(), Length(min=2, max=50)])

    default = [("Nothing Selected", "Nothing Selected")]
    countries = []
    for country in pycountry.countries:
        countries.append((country.name, country.name))

    countries.sort()
    country_choices = default + countries

    available_at_location = SelectField('Available at Locations', choices=country_choices)
    snack_brand = StringField("Snack Brand", [DataRequired(), Length(min=2, max=50)])

    categories = [("Cookies", "Cookies"), ("Chocolate", "Chocolate"), ("Candy", "Candy"), ("Chips", "Chips")]

    category = SelectField('Snack Category', choices=categories)
    description = StringField("Snack Description", [Length(min=2, max=255)])
    submit = SubmitField('Create Snack')

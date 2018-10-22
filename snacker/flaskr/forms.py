from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class RegistrationForm(FlaskForm):
    username = TextField("Username", [
        DataRequired("You must provide a username"),
         Length(min=4, max=20)
    ])
    first_name = TextField("First Name", [DataRequired(), Length(min=2, max=100)])
    last_name = TextField("Last Name", [DataRequired(), Length(min=2, max=100)])
    email = TextField("Email Address", [
        Email("Invalid email provided"),
        Length(min=6, max=50)
    ])
    is_company = BooleanField("Are you a company or distributor?")
    password = PasswordField("New Password", [
        DataRequired(),
        EqualTo("confirm", message="Passwords don't match")
    ])
    confirm = PasswordField("Repeat Password")
    accept_tos = BooleanField("I accept the Terms of Service and Privacy Notice", [DataRequired()])
    submit = SubmitField('Sign Up')




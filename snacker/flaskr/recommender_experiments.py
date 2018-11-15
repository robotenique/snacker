import urllib
from flask import Flask, render_template, request, flash, redirect, url_for, make_response, Response
from mongoengine import connect
from mongoengine.queryset.visitor import Q
from werkzeug.contrib.fixers import ProxyFix

from forms import RegistrationForm, LoginForm, CreateReviewForm, CreateSnackForm
import schema
"""
The purpose of this file is to be used for experiments for the recommendation
algorithm of our application.

Important: Check the docs in deliverable/doc/recommender.md
"""
app = Flask(__name__)

# With these constant strings, we can connect to generic databases
USERNAME_FILE = "username.txt"
PASSWORD_FILE = "password.txt"
MONGO_SERVER = "csc301-v3uno.mongodb.net"
APP_NAME = "Snacker"


try:
    print("hello")
    #mongo_uri = f"mongodb+srv://Jayde:Jayde@csc301-v3uno.mongodb.net/test?retryWrites=true"
    mongo_uri = "mongodb://localhost:27017/"
    app.config["MONGO_URI"] = mongo_uri
    mongo = connect(host=mongo_uri)
    # This is necessary for user tracking
    app.wsgi_app = ProxyFix(app.wsgi_app, num_proxies=1)
except Exception as inst:
    raise Exception("Error in database connection:", inst)

# TODO: Need to change this to an env variable later
app.config["SECRET_KEY"] = "2a0ca44c88db3d509085f32f2d4ed2e6"
app.config['DEBUG'] = True
app.url_map.strict_slashes = False


@app.route('/rec_test')
def rec_test():
	DATABASE = "test"
	my_db = mongo[DATABASE]
    return "Recommender test"

if __name__ == '__main__':
    app.run()

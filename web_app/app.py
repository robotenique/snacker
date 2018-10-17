from flask import Flask
from flask_pymongo import PyMongo
import urllib
import sys

# You need to create a mongo account and let Jayde know your mongo email address to add you to the db system
# Then you need to create a password.txt and username.txt each storing the password and username of your mongo account
app = Flask(__name__)
mongo_uri = "mongodb+srv://" + open('username.txt', 'r').read() + ":" + urllib.parse.quote(open('password.txt', 'r').read()) + "@csc301-v3uno.mongodb.net/test?retryWrites=true"
app.config["MONGO_URI"] = mongo_uri
mongo = PyMongo(app)


@app.route('/')
def hello_world():
    print('This is standard output', file=sys.stdout)
    # The one item in the testCollection db should be printed in console after refreshing page
    for x in mongo.db.testCollection.find({}):
        print(x, file=sys.stdout)
    return 'Hello World!'


if __name__ == '__main__':
    app.run()

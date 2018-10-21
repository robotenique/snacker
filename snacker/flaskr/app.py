from flask import Flask, render_template
from flask_pymongo import PyMongo
import urllib
import sys

# You need to create a mongo account and let Jayde know your mongo email address to add you to the db system so you can see stats online in mongo website
# Then you need to create a password.txt and username.txt each storing Your first name with the first letter capitalized, it has been set up that your first name is your username and password for the particular test cluster
app = Flask(__name__)

# With these constants strings, we can connect to generic databases
USERNAME_FILE = "username.txt"
PASSWORD_FILE = "password.txt"
DATABASE = "test"
MONGO_SERVER = "csc301-v3uno.mongodb.net"

try:
    username = open(USERNAME_FILE,  'r').read().strip().replace("\n","")
    pw = urllib.parse.quote(open(PASSWORD_FILE, 'r').read().strip().replace("\n", ""))
except Exception as inst:
    print("Error while reading username and password for database connection:", inst)
    exit()
mongo_uri = f"mongodb+srv://{username}:{pw}@{MONGO_SERVER}/{DATABASE}?retryWrites=true"
app.config["MONGO_URI"] = mongo_uri
mongo = PyMongo(app)

@app.route('/titlepage')
def titlepage():
    return render_template('index.html')

@app.route('/')
def hello_world():
    print('This is standard output', file=sys.stdout)
    print((f"All collections in the database '{DATABASE}':"
           f"\n\t{mongo.db.list_collection_names()}"), file=sys.stdout)
    # This prints all collections inside the database with name DATABASE
    print("Documents inside all collections: ", file=sys.stdout)
    for collec in mongo.db.list_collection_names():
        print(f"    {collec}", file=sys.stdout)
        for doc in mongo.db[collec].find({}):
            print(f"        {doc}", file=sys.stdout)
    print("", file=sys.stdout)
    return 'Hello World!'


if __name__ == '__main__':
    app.run()

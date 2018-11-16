import urllib
from mongoengine import connect
from mongoengine.queryset.visitor import Q
import schema
"""
The purpose of this file is to be used for experiments for the recommendation
algorithm of our application.

Important: Check the docs in deliverable/doc/recommender.md
"""

def recsys():
    DATABASE = "test"
    my_db = mongo[DATABASE]
    print(f"Collections found in the current database: {my_db.collection_names()}")
    generate_training_data(my_db)

def generate_training_data(my_db):
    """Given a database, generate training data from that specific database
       and return the data generated"""
    collection_names = my_db.collection_names()
    # Check that we have the collections that we need
    assert "snack" in collection_names
    assert "review" in collection_names
    assert "user" in collection_names
    snackID_to_index = {}
    cursor = schema.User.objects.aggregate(*[
         {
          '$lookup': {
              'from': schema.Review._get_collection_name(),
              'localField': '_id',
              'foreignField': 'user_id',
              'as': 'review'}
         }])
    for c in cursor:
        # If this user has made a review
        if c['review']:
            print(str(c['_id']))
            print(c['first_name'])
    print(type(cursor))


if __name__ == '__main__':
    try:
        mongo_uri = "mongodb://localhost:27017/"
        mongo = connect(host=mongo_uri)
        print("Connected to mongo db...\n")
    except Exception as inst:
        raise Exception("Error in database connection:", inst)
    recsys()


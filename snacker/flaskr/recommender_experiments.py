import urllib
from mongoengine import connect
from mongoengine.queryset.visitor import Q
import schema
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import svds
"""
The purpose of this file is to be used for experiments for the recommendation
algorithm of our application.

Important: Check the docs in deliverable/doc/recommender.md
"""

def recsys():
    DATABASE = "test"
    my_db = mongo[DATABASE]
    print(f"Collections found in the current database: {my_db.collection_names()}\n")
    tr_data = generate_training_data(my_db)
    training_recc_engine(tr_data)

def generate_training_data(my_db):
    """Given a database, generate training data from that specific database
       and return the data generated in a matrix in the form:
       user_index X snack_index, where:
       X[i][j] is the overall rating that user i gave to snack j."""
    collection_names = my_db.collection_names()
    # Check that we have the collections that we need
    assert "snack" in collection_names
    assert "review" in collection_names
    assert "user" in collection_names
    # Create mappers to map snack id to an index, and the reverse too
    snackID_to_index = {}
    index_to_snackID = {}
    index_snack = 0
    # Mapper for user
    userID_to_index = {}
    index_to_userID = {}
    index_user = 0
    # User ratings
    # user_index -> [(snack_index, ratingValue), (snack_index, ratingValue)]
    user_ratings = {}
    cursor = schema.User.objects.aggregate(*[
         {
          '$lookup': {
              'from': schema.Review._get_collection_name(),
              'localField': '_id',
              'foreignField': 'user_id',
              'as': 'review'}
         }])
    for c in cursor:
        # Add current user into the
        if not userID_to_index.get(str(c["_id"])):
            userID_to_index[str(c["_id"])] = index_user
            index_to_userID[index_user] =  str(c["_id"])
            # Empty list at first
            user_ratings[index_user] = []
        # If this user made a review, we need to add the ratings
        if c['review']:
            for review in c['review']:
                # Add current snack to the mapping if not already there
                if not snackID_to_index.get(str(review["snack_id"])):
                    snackID_to_index[str(review["snack_id"])] = index_snack
                    index_to_snackID[index_snack] =  str(review["snack_id"])
                    index_snack += 1
                user_ratings[index_user].append([snackID_to_index[str(review["snack_id"])], float(review["overall_rating"])])
            print(c['first_name'])
        index_user += 1
    # Create our training data
    row = []
    col = []
    data = []
    for user in user_ratings.keys():
        for rating in user_ratings[user]:
            #This is the logic: X[user, rating[0]] = rating[1]
            row.append(user)
            col.append(rating[0])
            data.append(rating[1])
    row = np.array(row).reshape(-1, 1).astype(float)
    col = np.array(col).reshape(-1, 1).astype(float)
    data = np.array(data).reshape(-1, 1).astype(float)
    """
    rating_data matrix, in this format (all float to keep type consistent):
    USER_ID  | SNACK_ID  | OVERALL_RATING
       2.    |     33.   |       5.
       1.    |     353.  |       2.5
    """
    rating_data = np.concatenate((row, col, data), axis=1)
    print(rating_data)
    #print(f"Sparse matrix: \n{X_sparse}\n")
    #print(f"Common rep. matrix: \n{X_sparse.toarray()}\n")
    # Returning an object with all the important information
    return {
        "rating_data": rating_data, # rating_data matrix, info above
        "snackID_to_index" : snackID_to_index, # SnackID (database id) to index in matrix
        "index_to_snackID": index_to_snackID, # index in matrix to SnackID (database id)
        "index_snack" :index_snack, # Number of snacks
        "userID_to_index" : userID_to_index, # UserID(database id) to index in matrix
        "index_to_userID" : index_to_userID, # index in matrix to UserID (database id)
        "index_user" : index_user, # Number of users
        "user_ratings" : user_ratings # Internal value of each user
    }

def training_recc_engine(train_data, K=2, train_size=.70):
    # IMPORTANT: 'K' (num latent features) Should be <= min(len(rows), len(cols))

    # Supress scientific notation
    np.set_printoptions(suppress=True, linewidth=300)
    all_data = train_data["rating_data"]
    num_users = train_data["index_user"]
    num_snacks = train_data["index_snack"]
    """ Data preparation (train and test data) """
    # Divide into train and test data
    rnd_permutation = np.random.permutation(all_data)
    last_pos = int(train_size*len(df.values)) + 1
    assert last_pos < len(all_data)
    X_train = rnd_permutation[:last_pos]
    X_test = rnd_permutation[last_pos:]
    new = np.zeros((num_users, num_snacks))
    # Populate our matrix with ONLY training data. The rest is 0 ==> Not available
    new[X_train[:, 0].astype(int), X_train[:, 1].astype(int)] = X_train[:, 2]
    #X_sparse = training_data["X_sparse"]

if __name__ == '__main__':
    try:
        mongo_uri = "mongodb://localhost:27017/"
        mongo = connect(host=mongo_uri)
    except Exception as inst:
        raise Exception("Error in database connection:", inst)
    recsys()


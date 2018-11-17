import urllib
import schema
import pickle
import numpy as np
from mongoengine import connect
"""
The purpose of this file is to be used for the recommendation
algorithm training of our application.

Important: Check the docs in deliverable/doc/recommender.md
"""

# MF class from A. Yeung, at http://www.albertauyeung.com/post/python-matrix-factorization/
class MF(object):
    def __init__(self, R, K, alpha, beta, iterations):
        """
        Perform matrix factorization to predict empty
        entries in a matrix.

        Arguments
        - R (ndarray)   : user-item rating matrix
        - K (int)       : number of latent dimensions
        - alpha (float) : learning rate
        - beta (float)  : regularization parameter
        """

        self.R = R
        self.num_users, self.num_items = R.shape
        self.K = K
        self.alpha = alpha
        self.beta = beta
        self.iterations = iterations

    def train(self):
        # Initialize user and item latent feature matrice
        self.P = np.random.normal(scale=1./self.K, size=(self.num_users, self.K))
        self.Q = np.random.normal(scale=1./self.K, size=(self.num_items, self.K))

        # Initialize the biases
        self.b_u = np.zeros(self.num_users)
        self.b_i = np.zeros(self.num_items)
        self.b = np.mean(self.R[np.where(self.R != 0)])

        # Create a list of training samples
        self.samples = [
            (i, j, self.R[i, j])
            for i in range(self.num_users)
            for j in range(self.num_items)
            if self.R[i, j] > 0
        ]

        # Perform stochastic gradient descent for number of iterations
        training_process = []
        for i in range(self.iterations):
            np.random.shuffle(self.samples)
            self.sgd()
            mse = self.mse()
            training_process.append((i, mse))
            if (i+1) % 10 == 0:
                print("Iteration: %d ; error = %.4f" % (i+1, mse))

        return training_process

    def mse(self):
        """
        A function to compute the total mean square error
        """
        xs, ys = self.R.nonzero()
        predicted = self.full_matrix()
        error = 0
        for x, y in zip(xs, ys):
            error += pow(self.R[x, y] - predicted[x, y], 2)
        return np.sqrt(error)

    def sgd(self):
        """
        Perform stochastic gradient descent
        """
        for i, j, r in self.samples:
            # Computer prediction and error
            prediction = self.get_rating(i, j)
            e = (r - prediction)

            # Update biases
            self.b_u[i] += self.alpha * (e - self.beta * self.b_u[i])
            self.b_i[j] += self.alpha * (e - self.beta * self.b_i[j])

            # Update user and item latent feature matrices
            self.P[i, :] += self.alpha * (e * self.Q[j, :] - self.beta * self.P[i,:])
            self.Q[j, :] += self.alpha * (e * self.P[i, :] - self.beta * self.Q[j,:])

    def get_rating(self, i, j):
        """
        Get the predicted rating of user i and item j
        """
        prediction = self.b + self.b_u[i] + self.b_i[j] + self.P[i, :].dot(self.Q[j, :].T)
        return prediction

    def full_matrix(self):
        """
        Computer the full matrix using the resultant biases, P and Q
        """
        return self.b + self.b_u[:,np.newaxis] + self.b_i[np.newaxis:,] + self.P.dot(self.Q.T)

def prepare_mongodb(mongo_uri="mongodb://localhost:27017/"):
    try:
        # TODO: change the mongo_uri to the production database when ready...
        mongo = connect(host=mongo_uri)
    except Exception as inst:
        raise Exception("Error in database connection:", inst)
    return mongo

def recsys(mongo, db_name="test"):
    if not mongo:
        raise ValueError("Mongo instance is invalid!")
    my_db = mongo[db_name]
    print(f"Collections found in the current database: {my_db.collection_names()}\n")
    tr_data = generate_training_data(my_db)
    recc = training_recc_engine(tr_data)
    # Create a dict with all the relevant model information
    model = {"model": recc,
             "snackID_to_index": tr_data["snackID_to_index"],
             "index_to_snackID": tr_data["index_to_snackID"],
             "index_snack": tr_data["index_snack"],
             "userID_to_index": tr_data["userID_to_index"],
             "index_to_userID": tr_data["index_to_userID"],
             "index_user": tr_data["index_user"]}
    print(model["index_to_snackID"])
    # Save model to file
    with open("recc_model.pickle", "wb") as f:
        # Pickle the 'model' dictionary using the highest protocol available
        pickle.dump(model, f, pickle.HIGHEST_PROTOCOL)
    print("\nTrained model saved in file 'recc_model.pickle'.")



    """ num_recommendations = 10
    ratings = recc[0]
    # Negative because we want the max
    ind = np.argpartition(ratings, -num_recommendations)[-num_recommendations:]
    print(f"Recommendations for user [0]:")
    print(f"Indexes: {ind}")
    print(f"Ratings: {ratings[ind]}") """


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
        if userID_to_index.get(str(c["_id"])) == None:
            userID_to_index[str(c["_id"])] = index_user
            index_to_userID[index_user] =  str(c["_id"])
            # Empty list at first
            user_ratings[index_user] = []
        # If this user made a review, we need to add the ratings
        if c['review']:
            for review in c['review']:
                # Add current snack to the mapping if not already there
                if snackID_to_index.get(str(review["snack_id"])) == None:
                    print("Adicionando: ", str(review["snack_id"]))
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

    #=====================Test example (comment to disable)=====================
    row = np.arange(10).reshape(-1, 1).astype(float)                          #
    col = np.arange(10).reshape(-1, 1).astype(float)                          #
    data = (np.random.rand(10)*10 + 1).reshape(-1, 1)                         #
    index_user = len(row)                                                     #
    index_snack = len(col)                                                    #
    #=====================Test example (comment to disable)=====================


    """
    RATING_DATA:
    =================
    rating_data matrix, in this format (all float to keep type consistent):
    USER_ID  | SNACK_ID  | OVERALL_RATING
       2.    |     33.   |       5.
       1.    |     353.  |       2.5
    """
    rating_data = np.concatenate((row, col, data), axis=1)
    print(f"\nRating data:\n{rating_data}\n")
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

def training_recc_engine(train_data, K=2, train_size=.70, alpha=0.001, beta=0.01, iterations=30):
    # IMPORTANT: 'K' (num latent features) Should be <= min(len(rows), len(cols))

    # Supress scientific notation
    np.set_printoptions(suppress=True, linewidth=300)
    all_data = train_data["rating_data"]
    num_users = train_data["index_user"]
    num_snacks = train_data["index_snack"]
    """ Data preparation (train and test data) """
    # Divide into train and test data
    rnd_permutation = np.random.permutation(all_data)
    last_pos = int(train_size*len(all_data)) + 1
    assert last_pos < len(all_data)
    X_train = rnd_permutation[:last_pos]
    X_test = rnd_permutation[last_pos:]
    new = np.zeros((num_users, num_snacks))
    # Populate our matrix with ONLY training data. The rest is 0 (this means it's Not available)
    new[X_train[:, 0].astype(int), X_train[:, 1].astype(int)] = X_train[:, 2]
    R = new
    """ Data training """
    mf = MF(R, K=K, alpha=alpha, beta=beta, iterations=iterations)
    training_process = mf.train()
    recc = mf.full_matrix()
    print("Finished training.")
    """ Data evaluation """
    # Calculate the MSE using the Frobenius norm
    # Correct indexes from the training
    u_id = X_test[:, 0].astype(int)
    m_id = X_test[:, 1].astype(int)
    # Compute the Frobenius norm
    mse = np.mean((X_test[:, 2] - recc[u_id, m_id])**2)
    print(f"Mean Squared Error: {mse}")
    # Return the trained model
    return recc

if __name__ == '__main__':
    mongo = prepare_mongodb()
    recsys(mongo)


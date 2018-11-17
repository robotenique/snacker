import pickle
import numpy as np
class Recommender(object):
    def __init__(self, model_filename="recc_model.pickle"):
        with open(model_filename, 'rb') as f:
            self.model = pickle.load(f)
            self.recc = self.model["model"]
            self.snackID_to_index = self.model["snackID_to_index"]
            self.index_to_snackID = self.model["index_to_snackID"]
            self.index_snack = self.model["index_snack"]
            self.userID_to_index = self.model["userID_to_index"]
            self.index_to_userID = self.model["index_to_userID"]
            self.index_user = self.model["index_user"]

    def recommend_snacks(self, user, review_from_user, num_snacks=10):
        """recommend_snacks

        Keyword Arguments:
            user {User} -- A user instance from mongoengine
            review_from_user {list} -- All reviews made by that user
            num_snacks {int} -- Number of new snacks to recommend (default: {10})
        """

        user_id = str(user.id)
        calculated_recommendation = False
        while not calculated_recommendation:
            # Check if the current user is in the trained model
            if user_id in self.userID_to_index.keys():
                pass
            else:
                self._retrain_model()

    def _retrain_model(self):
        """ Retrain a model if the information of the new user is inconsistent """


if __name__ == "__main__":
    rec = Recommender()

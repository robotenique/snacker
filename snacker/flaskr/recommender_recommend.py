import pickle
import numpy as np
from pathlib import Path
from recommender_training import recsys, prepare_mongodb
class Recommender(object):
    def __init__(self, model_filename="recc_model.pickle"):
        self.model_filename = model_filename
        self.update_model()

    def recommend_snacks(self, user, review_from_user, country, num_snacks=10):
        """recommend_snacks

        Keyword Arguments:
            user {User} -- A user instance from mongoengine
            review_from_user {list} -- All reviews made by that user
            num_snacks {int} -- Number of new snacks to recommend (default: {10})
        """

        user_id = str(user.id)
        calculated_recommendation = []
        while not calculated_recommendation:
            # Check if the current user is in the trained model
            user_is_trained = user_id in self.userID_to_index.keys()
            # Check if all the snacks the user reviewed are in the trained model (they should be)
            snacks_are_trained = all((str(r["snack_id"]) in self.snackID_to_index.keys() for r in review_from_user))
            # Check if user has reviewed at least 10 snacks!
            user_review_at_least_10 = len(review_from_user) >= 10
            if user_review_at_least_10 and user_is_trained and snacks_are_trained:
                """Remember: Have to make snacks which are not from the same current country
                   have rating = -Math.inf or something like that, to ignore other snacks
                """
                pass # TODO: Generate and return new recommendations from the user
            else: # Retrain the model if the current user is not
                self._retrain_model()

    def _retrain_model(self):
        """ Retrain a model if the information of the new user is inconsistent """
        mongo = prepare_mongodb(mongo_uri="mongodb://localhost:27017/")
        recsys(mongo, db_name="test")
        self.update_model()
    
    def update_model(self):
        model_file = Path(self.model_filename)
        if not model_file.is_file():
            raise FileNotFoundError(f"The model file does not exists ({self.model_filename})")
        # Update current model attributes from the file
        with open(self.model_filename, 'rb') as f:
            self.model = pickle.load(f)
            self.recc = self.model["model"]
            self.snackID_to_index = self.model["snackID_to_index"]
            self.index_to_snackID = self.model["index_to_snackID"]
            self.index_snack = self.model["index_snack"]
            self.userID_to_index = self.model["userID_to_index"]
            self.index_to_userID = self.model["index_to_userID"]
            self.index_user = self.model["index_user"]

if __name__ == "__main__":
    rec = Recommender()

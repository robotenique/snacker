import pickle
import numpy as np
import random as rnd
from pathlib import Path
from recommender_training import recsys, prepare_mongodb
from schema import Snack
from mongoengine.queryset.visitor import Q
class Recommender(object):
    def __init__(self, mongo, model_filename="recc_model.pickle"):
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
        # Get snacks from the current country
        snacks_in_current_country = Snack.objects(Q(available_at_locations__in=[country]))
        calculated_recommendation = []
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
            # User index in the model matrix
            user_idx = self.userID_to_index[user_id]
            # Get idx of all snacks the current user already reviewed (to be removed)
            snacks_idx_already_reviewed = set(self.snackID_to_index[str(r["snack_id"])] for r in review_from_user)
            # Get idx of all snacks from the current country
            snacks_idx_current_country = set(self.snackID_to_index[str(s.id)] for s in snacks_in_current_country)
            # The snacks to be KEPT in the matrix is the set difference of them:
            to_be_kept = np.array(list(snacks_idx_current_country - snacks_idx_already_reviewed))
            to_be_kept_other_countries = np.array(list(set(range(self.index_snack)) - snacks_idx_already_reviewed))
            # To recommend, we will sort all snacks which are 'to_be_kept':
            # TODO: check that this is a NUMPY matrix!!
            # Snacks which are not reviewed by the current user, but are from the same country
            temp_argindex_from_country = np.argsort(self.recc[user_idx][to_be_kept])[::-1]
            recommended_snacks_from_country = to_be_kept[temp_argindex_from_country]
            recommended_snacks_from_country = [self.index_to_snackID[s_idx] for s_idx in recommended_snacks_from_country]
            # FROM HERE, I have list of snack ids: [qsduaiu12312. 12en1j23u12o]
            # TODO: CHECK BELOW RECOMMENDATION WORKS!!
            recommended_snacks_from_country = Snack.objects(Q(id__in=recommended_snacks_from_country))
            # TODO: Only do below step IF we need to get more recommended snacks!
            # Snacks which are not reviewed by the current user, but are not bound by the country
            temp_argindex_outside_country = np.argsort(self.recc[user_idx][to_be_kept_other_countries])[::-1]
            recommended_snacks_outside_country = to_be_kept_other_countries[temp_argindex_outside_country]
            recommended_snacks_outside_country = [self.index_to_snackID[s_idx] for s_idx in recommended_snacks_outside_country]
            recommended_snacks_outside_country = Snack.objects(Q(id__in=recommended_snacks_outside_country))

            # Finally, generate the user snack recommendation!
            calculated_recommendation = recommended_snacks_from_country[:num_snacks]
            num_remaining = num_snacks - len(calculated_recommendation)

            if num_remaining > 0: # If we need to get more snacks to recommend, get from outside_country
                calculated_recommendation + recommended_snacks_outside_country[:num_remaining]
            return calculated_recommendation
        else:            
            # If we have enough snacks from the current country, just return random snacks from current country
            if len(snacks_in_current_country) >= num_snacks:
                # TODO: Check this list
                return rnd.sample(snacks_in_current_country, num_snacks)
            else: # TODO: If you changed the definition of the list above, need to re-check that the below case is working
                calculated_recommendation = snacks_in_current_country
                num_remaining = num_snacks - len(calculated_recommendation)
                # We need to get 'num_remaining' more snacks to recomend to the user, from other countries
                snacks_notin_current_country = Snack.objects(Q(available_at_locations__nin=[country]))
                # Concatenate both lists and return them
                return calculated_recommendation + rnd.sample(snacks_notin_current_country, num_remaining)

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

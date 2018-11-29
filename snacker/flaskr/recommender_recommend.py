import pickle
import numpy as np
import random as rnd
from pathlib import Path
from recommender_training import recsys, prepare_mongodb
from schema import Snack, User, Review #TODO: Maybe remove some of this things
from mongoengine.queryset.visitor import Q

class Recommender(object):
    def __init__(self, model_filename="recc_model.pickle"):
        self.model_filename = model_filename
        self.update_model()

    def recommend_snacks(self, user, review_from_user, country, num_snacks=10, msgs=list()):
        """recommend_snacks

        Keyword Arguments:
            user {User} -- A user instance from mongoengine
            review_from_user {list} -- All reviews made by that user
            country {str} -- The country in which the user last logged in
            num_snacks {int} -- Number of new snacks to recommend (default: {10})
        """
        # Remove 'none' from a set, to prevent 'None' errors in the dictionary
        filt_none = lambda set_obj: set(filter(None, set_obj))
        user_id = str(user.id)
        # Get snacks from the current country
        # If no country provided, search for everything!
        snacks_in_current_country = Snack.objects(Q(available_at_locations__in=[country])) if country else Snack.objects
        calculated_recommendation = []
        # Check if the current user is in the trained model
        user_is_trained = user_id in self.userID_to_index.keys()
        # Check if all the snacks the user reviewed are in the trained model (they should be)
        snacks_are_trained = all((str(r["snack_id"]) in self.snackID_to_index.keys() for r in review_from_user))
        # Check if user has reviewed at least 10 snacks!
        user_review_at_least_10 = len(review_from_user) >= 10
        num_remaining = num_snacks
        if user_review_at_least_10 and user_is_trained and snacks_are_trained:
            """ Need to ignore irrelevant snacks to make the correct recommendation!"""
            # User index in the model matrix
            user_idx = self.userID_to_index[user_id]
            # Get idx of all snacks the current user already reviewed (to be removed)
            snacks_idx_already_reviewed = set(self.snackID_to_index.get(str(r["snack_id"])) for r in review_from_user)
            snacks_idx_already_reviewed = filt_none(snacks_idx_already_reviewed)
            # Get idx of all snacks from the current country
            snacks_idx_current_country = set(self.snackID_to_index.get(str(s.id)) for s in snacks_in_current_country)
            snacks_idx_current_country = filt_none(snacks_idx_current_country)
            # Snacks with no image don't go to recommendation :)
            snacks_without_image = set(self.snackID_to_index.get(str(s.id)) for s in snacks_in_current_country if not s.photo_files)
            snacks_without_image = filt_none(snacks_without_image)

            # The snacks to be KEPT in the matrix is the set difference of them:
            to_be_kept = np.array(list((snacks_idx_current_country - snacks_idx_already_reviewed) - snacks_without_image))

            # To recommend, we will sort all snacks which are 'to_be_kept':
            # Snacks which are not reviewed by the current user, but are from the same country
            if len(to_be_kept) != 0:
                temp_argindex_from_country = np.argsort(self.recc[user_idx][to_be_kept])[::-1]
                recommended_snacks_from_country = to_be_kept[temp_argindex_from_country]
                recommended_snacks_from_country = [self.index_to_snackID[s_idx] for s_idx in recommended_snacks_from_country]
                # FROM HERE, I have list of snack ids: e.g. [qsduaiu12312. 12en1j23u12o]
                recommended_snacks_from_country = Snack.objects(Q(id__in=recommended_snacks_from_country))
                # Finally, generate the user snack recommendation!
                calculated_recommendation = list(recommended_snacks_from_country[:num_snacks])
                num_remaining = num_snacks - len(calculated_recommendation)
                # If we need to get more snacks to recommend, get from outside_country
            if num_remaining > 0:
                snacks_without_image = set(self.snackID_to_index.get(str(s.id)) for s in Snack.objects if not s.photo_files)
                snacks_without_image = filt_none(snacks_without_image)
                # Snacks which are not reviewed by the current user, but are not bound by the country
                to_be_kept_other_countries = set(range(self.index_snack)) - snacks_idx_already_reviewed
                to_be_kept_other_countries = np.array(list(to_be_kept_other_countries - snacks_without_image))
                if len(to_be_kept_other_countries) != 0:
                    temp_argindex_outside_country = np.argsort(self.recc[user_idx][to_be_kept_other_countries])[::-1]
                    recommended_snacks_outside_country = to_be_kept_other_countries[temp_argindex_outside_country]
                    recommended_snacks_outside_country = [self.index_to_snackID[s_idx] for s_idx in recommended_snacks_outside_country]
                    recommended_snacks_outside_country = Snack.objects(Q(id__in=recommended_snacks_outside_country))
                    calculated_recommendation += list(recommended_snacks_outside_country[:num_remaining])

            return calculated_recommendation
        else:
            if not user_is_trained or not snacks_are_trained:
                msgs.append("your recommendations aren't ready yet, check these snacks instead!")
            elif not user_review_at_least_10:
                msgs.append(f"your need to review at least {10 - len(review_from_user)} more snacks to get recommendations!")
            # If we have enough snacks from the current country, just return best snacks from current country
            if len(snacks_in_current_country) >= num_snacks:
                return rnd.sample(list(snacks_in_current_country), num_snacks)
            else: # Not enough snacks in current country
                calculated_recommendation = list(snacks_in_current_country)
                num_remaining = num_snacks - len(calculated_recommendation)
                # We need to get 'num_remaining' more snacks to recomend to the user, from other countries
                snacks_notin_current_country = Snack.objects(Q(available_at_locations__nin=[country]))
                # Concatenate both lists and return them
                return calculated_recommendation + rnd.sample(list(snacks_notin_current_country), num_remaining)

    def _retrain_model(self):
        # TODO: REMOVE LOCAL DATABASE
        """ Retrain a model if the information of the new user is inconsistent """
        mongo = prepare_mongodb(mongo_uri="")
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
    # TESTING with:
    # Salty user Katrina beck, ID: 5bfcc6e767afee10a880f8f5
    mongo = prepare_mongodb(mongo_uri="mongodb+srv://Jayde:Jayde@csc301-v3uno.mongodb.net/test?retryWrites=true")
    salty_user_id = "5bfcc6e767afee10a880f8f5"
    katrina = User.objects(id=salty_user_id)[0]
    country_katrina = "Vietnam"
    review_from_katrina = Review.objects(user_id=salty_user_id)
    print(katrina)
    print(f"Katrina has done {len(review_from_katrina)} reviews!!")
    # Create a new recommender
    rec = Recommender()
    print(rec.recommend_snacks(katrina, review_from_katrina, country_katrina))


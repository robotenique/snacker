Recommender System dev - Snacker
========================
Do experiments in the file recommender_training.py.
It's recommended to use a **local** database for experiments! For that, make sure you've downloaded mongodb,
and use this to save and restore databases:
- Save a database to a dump: [mongodump](https://docs.mongodb.com/manual/reference/program/mongodump/#bin.mongodump):
```bash
$ mongodump --uri "mongodb+srv://Jayde:Jayde@csc301-v3uno.mongodb.net/test?retryWrites=true"
```
- Restore a database from a dump: [mongorestore](https://docs.mongodb.com/manual/reference/program/mongorestore/#bin.mongorestore)

* Start a localdatabase

```bash
$ sudo service mongod start
```

* Enter the shell with ```bash $ mongo ``` , check commands for reference [here](https://docs.mongodb.com/manual/reference/mongo-shell/)


## Recommender System - Approach

This [link](https://towardsdatascience.com/various-implementations-of-collaborative-filtering-100385c6dfe0) has some useful insight about
general recommender algorithms.


### Data

**Objective:** Given a user + that user geolocation (country), recommend new snacks to that user which are available in that country.
Our current model of reviews include these 6 measures:

- overall_rating

- sourness

- spiciness

- bitterness

- sweetness

- saltiness

### Matrix Factorization (overall_rating)

![visualization](https://cdn-images-1.medium.com/max/1600/1*Zhm1NMlmVywn0G18w3exog.png)


The first recommender algorithm uses Matrix Factorization, optimizing using SGD (Stochastic Gradient Descent). MF is very stable and have good performance, and is very utilized because it's highly scalable, differently than other neighbor comparing metrics such as the *Cosine Distance*, *Pearson Coefficient*, etc. More information about this procedure can be found [here](http://www.albertauyeung.com/post/python-matrix-factorization/).

This is the basic procedure done by **recommender_training.py**:

* Query the database and get all tuples of the form: (user_id, snack_id, overall_rating), and form a list;
* Separate one portion of this list to be the training data. The remaining data is the test data;
* Create a matrix with zeroes, and fill only the data from the training data. i.e., given that the training data is a list of tuples in the form (**user_id**, **snack_id**, **overall_rating**), this new matrix will be in the form R\[**user_id**\]\[**snack_id**\] = overall_rating from **user_id** to **snack_id**. The ids of the user and the snacks are converted and encoded through 2 different maps (mapping from the database id to an index in the matrix!);
* The training is basically using the SVD idea to use [latent features/variables](https://en.wikipedia.org/wiki/Latent_variable) to approximate the matrix built in the last step. Every entry in the last step matrix which has a value of 0 is considered as 'missing data'. This means that the SGD won't use this data to optimize (minimize [MSE](https://en.wikipedia.org/wiki/Mean_squared_error)). The conditions and hyperparameters of this training can be changed in the file.
* The result of the training is a matrix **recc**, which predicts the rating that every user would give to every item. The model can be evaluated by calculating the Frobenius norm over the **test** list. [More info about evaluation here!](https://stats.stackexchange.com/questions/97411/evaluating-matrix-factorization-algorithms-for-netflix)
* Now the model, along with all the mapping dictionaries and relevant information, is saved in a file using Pickle.

**Current mock idea:**

* 5000 Users, no demographic division. Users were generated using [RandomUser API](https://randomuser.me)
* Approx. 2200 Snacks from all over the world
* Total = 2mi of possible reviews. Going to generate: 408 000 (.2 times of the data) => ~82 review per user >:D;
* All users have the same password: 123456
* The user group will be saved at 'usergroup.json'
* The base profiles are: salty, spicy, sour, sweet, bitter. Then I put three more: mix(spicy, sweet), mix(sweet, sour), mix(salty, sour)
* For the base class, the user will rate 60 snacks of that category (salty, sweet, etc) with rating from 4 to 5. Then, choose random snacks from all the snacks, and give them ratings following a more uniform normal distribution for the 22 snacks left to review.
* For the mixed classes, first there is 1/2 chance of choosing each category, and the user will rate 50 randomly choosen snacks which belongs to one of those categories. Then,it will choose snacks from the 'remaining_snacks' category, and give them ratings from 0 to 4 following a normal distribution.
* Distribution of classes are like this:

The division of the user profiles will be like this:
* 14% - Salty
* 14% - Spicy
* 14% - Sour
* 14% - Sweet
* 14% - Bitter
* 10% - mix(spicy, sweet) + remaining_snacks
* 10% - mix(sweet, sour) + remaining_snacks
* 10% - mix(salty, sour) + remaining_snacks


Each user profile will rate the metrics following a collection of normal distributions. These are the normal distributions patterns for each basic profile. The mixed classes will combine two of those.

![salty-profile](../resources/d3/salty_profile.png)
![spicy-profile](../resources/d3/spicy_profile.png)
![sour-profile](../resources/d3/sour_profile.png)
![sweet-profile](../resources/d3/sweet_profile.png)
![bitter-profile](../resources/d3/bitter_profile.png)


### Machine Learning model - Learning curve
Below is the learning curve of the model. The mean squared error displayed is in the trained data itself.
The final MSE on the TEST data was approx. **0.5**.

![learning-curve](../resources/d3/learning_curve.png)


IMPORTANT: Procedures when adding information to the production database
===

1. Remove the 'delete' from the routes to add new things into the database!
2. Get app.py from github, then add the new methods there!
* FOR THE TA to run: Create username.txt, and password.txt!! (Will the TA actually run the project??)
* Change db to remote database
* DELETE all unnecessary routes
Recommender System dev - Snacker
========================
Do experiments in the file recommender_experiments.py.
Use a **local** database! For that, make sure you've downloaded mongodb,
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

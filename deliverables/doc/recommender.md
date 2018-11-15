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

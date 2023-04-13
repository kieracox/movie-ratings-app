"""Script to seed database."""

#import external libraries
import os
import json
from random import choice, randint
from datetime import datetime

#import other python files in folder
import crud
import model
import server

#drop and create new db called ratings
os.system("dropdb ratings")

os.system('dropdb ratings')
os.system('createdb ratings')

#connect to the database and call create_all
model.connect_to_db(server.app)
model.db.create_all()


#open json file with movie data
with open('data/movies.json') as f:
    movie_data = json.loads(f.read())
    movies_in_db = []
    # loop through movies and create Movie objects, add to empty lsist
    for movie in movie_data:
        title = movie["title"]
        overview = movie["overview"]
        poster_path = movie["poster_path"]
        release_date = datetime.strptime(movie["release_date"], "%Y-%m-%d")

        db_movie = crud.create_movie(title, overview, release_date, poster_path)
        movies_in_db.append(db_movie)
    # add movie list to db and commit
    model.db.session.add_all(movies_in_db)
    model.db.session.commit()

#create user email and passwords
for n in range(10):
    email = f'user{n}@test.com'
    password = 'test'

    #create User objects and add to database
    db_user = crud.create_user(email, password)
    model.db.session.add(db_user)
    # create random ratings for each user and add to db
    for _ in range(10):
        random_movie = choice(movies_in_db)
        score = randint(1, 5)
        rating = crud.create_rating(db_user, random_movie, score)
        model.db.session.add(rating)

model.db.session.commit()
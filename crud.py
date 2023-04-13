"""CRUD operations."""
#import from model.py
from model import db, User, Movie, Rating, connect_to_db

def create_user(email, password):
    """Create and return a new user."""
    user = User(email=email, password=password)

    return user

def return_all_users():
    """Return all users."""
    return User.query.all()

def get_user_by_id(user_id):
    """Get and return a user by their id."""
    return User.query.get(user_id)

def get_user_by_email(email):
    """Get and return a user by their email."""
    return User.query.filter(User.email == email).first()

def create_movie(title, overview, release_date, poster_path):
    """Create and return a new movie."""
    movie = Movie(title=title, overview=overview, release_date=release_date, poster_path=poster_path)

    return movie

def return_all_movies():
    """Get and return all movies."""
    return Movie.query.all()

def get_movie_by_id(movie_id):
    """Get and return a movie by its id."""
    return Movie.query.get(movie_id)

def create_rating(user, movie, score):
    """Create and return a new rating."""
    rating = Rating(user=user, movie=movie, score=score)

    return rating

def change_rating(rating_id, new_score):
    """Update a user's rating."""
    rating = Rating.query.get(rating_id)
    rating.score = new_score




if __name__ == '__main__':
    from server import app
    connect_to_db(app)


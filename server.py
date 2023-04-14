"""Server for movie ratings app."""
# import external libraries and other python files
from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db, User, Movie, Rating
import crud

from jinja2 import StrictUndefined

#configure the Flask instance
app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """View homepage."""
    return render_template('homepage.html')

@app.route('/movies')
def all_movies():
    """View all movies."""
    movies = crud.return_all_movies()
    return render_template('all_movies.html', movies=movies)

@app.route("/movies/<movie_id>")
def show_movie(movie_id):
    """Show details on a particular movie."""
    movie = crud.get_movie_by_id(movie_id)
    return render_template("movie_details.html", movie=movie)

@app.route("/users")
def all_users():
    """View all users."""
    users = crud.return_all_users()
    return render_template('all_users.html', users=users)

@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user."""
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)

    if user:
        flash("You can't create an account with that email. Try again.")
    else: 
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")
    
    return redirect("/")

@app.route("/users/<user_id>")
def show_user(user_id):
    """Show details on a particular user."""
    user = crud.get_user_by_id(user_id)
    return render_template("user_details.html", user=user)

@app.route("/login", methods=["POST"])
def log_in_user(): 
    """Log in a user."""
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect. Please try again.")
    else:
        session["user_email"] = user.email
        flash(f"Welcome back, {user.email}!")
    return redirect("/")

@app.route("/movies/<movie_id>/ratings", methods=["POST"])
def create_rating(movie_id):
    """Add a movie rating."""
    user_email = session.get("user_email")
    user_rating = request.form.get("rating")

    if user_email is None:
        flash("Please log in to rate your movie.")
    else:
        user = crud.get_user_by_email(user_email)
        movie = crud.get_movie_by_id(movie_id)
        rating = crud.create_rating(user, movie, int(user_rating))
        db.session.add(rating)
        db.session.commit()
        flash(f"Movie rated! Your score is {user_rating}")
    
    return redirect(f"/movies/{movie_id}")

@app.route("/update_rating", methods=["POST"])
def update_rating():
    """Update a movie rating."""
    rating_id = request.json["rating_id"]
    updated_score = request.json["updated_score"]
    crud.change_rating(rating_id, updated_score)
    db.session.commit()
    return "Success"

#connect to db
if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

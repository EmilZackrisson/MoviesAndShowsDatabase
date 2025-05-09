from flask import *
from Db import Db

app = Flask(__name__)

database = Db()


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route("/movies")
def get_highest_rated_movies():
    movies = database.get_highest_rated_movies()
    return str(movies)


@app.route("/shows")
def get_highest_rated_shows():
    shows = database.get_highest_rated_shows()
    return str(shows)


@app.route("/movieOrShow/<string:movShowId>")
def movie(movShowId):
    movieOrShow = database.get_movie_or_show(movShowId)
    if movie:
        # movie_obj = MovieOrShow(movie)
        return str(movieOrShow)
    else:
        return "Movie or show not found", 404


@app.route("/rate/<string:movShowId>", methods=["GET", "POST"])
def rate(movShowId: str):
    if request.method == "POST":
        # Call rate procedure
        print(request.form)
        database.rate(movShowId, request.form["rating"])
        return "Rating was successfull"
    else:
        return render_template("rate.html")


# @app.route("/movies/new", methods=["GET", "POST"])
# def new_movie():
#     if request.method == "POST":
#         print(request.form)
#         return "Movie added successfully"
#     else:
#         return render_template("home.html")

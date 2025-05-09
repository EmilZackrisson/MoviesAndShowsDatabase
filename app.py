from flask import *
from Db import Db

app = Flask(__name__)

database = Db()


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route("/movies")
def get_highest_rated_movies():
    movies = database.get_highest_rated_movies()
    return render_template("titleTable.html", titles=movies, type="Movies")


@app.route("/shows")
def get_highest_rated_shows():
    shows = database.get_highest_rated_shows()
    return render_template("titleTable.html", titles=shows, type="Shows")


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
        database.rate(movShowId, request.form["rating"])
        return "Rating was successfull"
    else:
        title = database.get_movie_or_show(movShowId)
        return render_template("rate.html", title=title)

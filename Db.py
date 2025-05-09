import mysql.connector


class Db:
    def __init__(self):

        self.mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="mysql",
        )

        self.cursor = self.mydb.cursor()
        self.cursor.execute("USE MovieTvDatabase")

    def get_highest_rated_movies(self):
        sql = "SELECT Title, avgRating FROM MoviesAndShows INNER JOIN Ratings ON MoviesAndShows.id = Ratings.movShowId WHERE Type = 'movie' ORDER BY avgRating DESC LIMIT 100"

        self.cursor.execute(sql)
        ret = self.cursor.fetchall()
        return ret

    def get_highest_rated_shows(self):
        sql = "SELECT Title, avgRating FROM MoviesAndShows INNER JOIN Ratings ON MoviesAndShows.id = Ratings.movShowId WHERE Type = 'tvSeries' ORDER BY avgRating DESC LIMIT 100"

        self.cursor.execute(sql)
        ret = self.cursor.fetchall()
        return ret

    def get_movie_or_show(self, movShowId: str):
        sql = "SELECT * FROM MoviesAndShows WHERE id = %s"
        val = (movShowId,)
        self.cursor.execute(sql, val)
        return self.cursor.fetchone()

    def rate(self, movShowId: str, rating: float):
        print(movShowId, rating)
        self.cursor.callproc("rate", [movShowId, rating,])
        ret = self.cursor.stored_results()
        for result in ret:
            print(result.fetchall())

import mysql.connector
from Title import Title


class Db:
    def __init__(self):

        self.mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="mysql",
        )

        self.cursor = self.mydb.cursor()
        self.cursor.execute("USE MovieTvDatabase")

    def get_highest_rated_movies(self) -> dict:
        sql = "SELECT id, Title, avgRating FROM MoviesAndShows INNER JOIN Ratings ON MoviesAndShows.id = Ratings.movShowId WHERE Type = 'movie' ORDER BY avgRating DESC LIMIT 100"

        self.cursor.execute(sql)
        ret = self.cursor.fetchall()
        lista = []
        for title in ret:
            lista.append(self._title_summary_to_dict(title))

        return lista

    def get_highest_rated_shows(self) -> list[Title]:
        sql = "SELECT id, Title, avgRating FROM MoviesAndShows INNER JOIN Ratings ON MoviesAndShows.id = Ratings.movShowId WHERE Type = 'tvSeries' ORDER BY avgRating DESC LIMIT 100"

        self.cursor.execute(sql)
        ret = self.cursor.fetchall()

        lista = []
        for title in ret:
            lista.append(self._title_summary_to_dict(title))

        return lista

    def get_movie_or_show(self, movShowId: str) -> dict:
        sql = "SELECT * FROM MoviesAndShows WHERE id = %s"
        val = (movShowId,)
        self.cursor.execute(sql, val)
        ret = self.cursor.fetchone()
        return {
            "id": ret[0],
            "Title": ret[1],
            "StartYear": ret[2],
            "EndYear": ret[3],
            "Runtime": ret[4],
            "Type": ret[5]
        }

    def rate(self, movShowId: str, rating: float):
        print(movShowId, rating)
        self.cursor.callproc("rate", [movShowId, rating,])
        ret = self.cursor.stored_results()
        for result in ret:
            print(result.fetchall())

    def _title_summary_to_dict(self, data):
        return {
            "id": data[0],
            "title": data[1],
            "rating": data[2]
        }

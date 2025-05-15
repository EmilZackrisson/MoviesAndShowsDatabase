import mysql.connector
from Models import Character, Title


class Db:
    def __init__(self):

        self.mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="mysql",
        )

        self.cursor = self.mydb.cursor()
        self.cursor.execute("USE MovieTvDatabase")

    def get_highest_rated_movies(self) -> list[dict]:
        sql = "SELECT id, Title, avgRating FROM MoviesAndShows INNER JOIN Ratings ON MoviesAndShows.id = Ratings.movShowId WHERE Type = 'movie' ORDER BY avgRating DESC LIMIT 1000"

        self.cursor.execute(sql)
        ret = self.cursor.fetchall()
        lista = []
        for title in ret:
            lista.append(self._title_summary_to_dict(title))

        return lista

    def get_highest_rated_shows(self) -> list[Title]:
        sql = "SELECT id, Title, avgRating FROM MoviesAndShows INNER JOIN Ratings ON MoviesAndShows.id = Ratings.movShowId WHERE Type = 'tvSeries' ORDER BY avgRating DESC LIMIT 1000"

        self.cursor.execute(sql)
        ret = self.cursor.fetchall()

        lista = []
        for title in ret:
            lista.append(self._title_summary_to_dict(title))

        return lista

    def get_title(self, type="movie", order_by="avgRating", desc=True, limit=1000) -> list[dict]:
        order = ""
        if desc:
            order = "DESC"

        sql = f"SELECT id, Title, avgRating FROM MoviesAndShows INNER JOIN Ratings ON MoviesAndShows.id = Ratings.movShowId WHERE Type = '{type}' ORDER BY {order_by} {order} LIMIT {limit}"

        self.cursor.execute(sql)
        ret = self.cursor.fetchall()

        lista = []
        for title in ret:
            lista.append(self._title_summary_to_dict(title))

        return lista

    def get_movie_or_show(self, movShowId: str) -> Title:
        sql = "SELECT * FROM MoviesAndShows WHERE id = %s"
        val = (movShowId,)
        self.cursor.execute(sql, val)
        ret = self.cursor.fetchone()
        title = Title(ret)
        title.rating = self.get_rating(movShowId)
        return title

    def get_persons_from_title(self, movShowId: str) -> list[Character]:
        sql = "SELECT id, name, Roles.category, Roles.character FROM People INNER JOIN Roles ON People.id = Roles.peopleId WHERE Roles.movShowId = %s ORDER BY Roles.ordering"
        val = (movShowId,)
        self.cursor.execute(sql, val)
        all = self.cursor.fetchall()

        return [Character(char[0], char[1], char[3]) for char in all]

    def rate(self, movShowId: str, rating: float):
        print(movShowId, rating)
        self.cursor.callproc("rate", [movShowId, rating,])
        ret = self.cursor.stored_results()
        for result in ret:
            print(result.fetchall())

    def get_rating(self, movShowId: str) -> float:
        sql = "SELECT avgRating FROM Ratings WHERE movShowId = %s"
        val = (movShowId,)
        self.cursor.execute(sql, val)
        ret = self.cursor.fetchone()
        if ret:
            return ret[0]
        else:
            return None

    def get_actors(self) -> list[dict]:
        sql = "SELECT id, name FROM People LIMIT 1000"
        self.cursor.execute(sql)
        ret = self.cursor.fetchall()
        lista = []
        for actor in ret:
            lista.append({
                "id": actor[0],
                "name": actor[1]
            })

        return lista

    def get_actor(self, personId: str) -> dict:
        sql = "SELECT * FROM People WHERE id = %s"
        val = (personId,)
        self.cursor.execute(sql, val)
        ret = self.cursor.fetchone()
        titleCount = self.getActorTitleCount(personId)
        if ret:
            return {
                "id": ret[0],
                "name": ret[1],
                "birthYear": ret[2],
                "deathYear": ret[3],
                "titleCount": titleCount
            }
        else:
            return None

    def getActorTitleCount(self, personId: str) -> int:
        sql = "SELECT `MovieTvDatabase`.`getActorTitleCount`(%s)"
        val = (personId,)
        self.cursor.execute(sql, val)
        ret = self.cursor.fetchone()
        if ret:
            return ret[0]
        else:
            return None

    def _title_summary_to_dict(self, data):
        return {
            "id": data[0],
            "title": data[1],
            "rating": data[2]
        }

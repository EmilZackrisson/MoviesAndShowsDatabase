import json
import mysql.connector
import pandas as pd
from alive_progress import alive_bar
import urllib.request
import os
import gzip
import shutil
import numpy as np
from getMostImportantData import get_most_important_data
import subprocess

IMDB_BASE_URL = "https://datasets.imdbws.com/"
IMDB_FILES = ["name.basics.tsv.gz", "title.akas.tsv.gz",
              "title.basics.tsv.gz", "title.ratings.tsv.gz", "title.principals.tsv.gz"]

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="mysql"
)

cursor = mydb.cursor()


def download_dataset():
    os.makedirs("./data", exist_ok=True)
    for file in IMDB_FILES:
        new_path = os.path.join("./data", file)
        if os.path.exists(new_path) or os.path.exists(new_path.replace(".gz", "")):
            print(file, "already downloaded")
            continue
        url = IMDB_BASE_URL + file
        urllib.request.urlretrieve(url, new_path)


def uncompress_gz_file(input_path, output_path):
    """
    Uncompress a .gz file and save the uncompressed content to a new file.

    :param input_path: Path to the .gz file
    :param output_path: Path to save the uncompressed file
    """
    with gzip.open(input_path, 'rb') as f_in:
        with open(output_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


def unpack_dataset_files():
    for file in IMDB_FILES:
        compressed_path = os.path.join("./data", file)
        uncompressed_path = compressed_path.replace(".gz", "")

        if os.path.exists(compressed_path) and not os.path.exists(uncompressed_path):
            uncompress_gz_file(compressed_path, uncompressed_path)
            print(f"Uncompressed {compressed_path} to {uncompressed_path}")


def executeScriptsFromFile(filename):
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()
    sqlCommands = sqlFile.split(';')

    for command in sqlCommands:
        try:
            if command.strip() != '':
                cursor.execute(command)
        except IOError as msg:
            print("Command skipped: ", msg)


def run_mysql_cli_import(filename):
    with open(filename, 'r') as f:
        proc = subprocess.run(
            ['mysql', '-h', '127.0.0.1', '-P', '3306',
                '-u', 'root', '-pmysql', 'MovieTvDatabase'],
            stdin=f
        )
        print("exit code mysql:", proc.returncode)


def add_professions(person_id: str, professions: list[str]):
    sql = "INSERT INTO Professions (type, PeopleId) VALUES (%s, %s)"
    for profession in professions:
        val = (profession, person_id)
        cursor.execute(sql, val)
        mydb.commit()


def add_known_for(person_id: str, known_for: list[str]):
    sql = "INSERT IGNORE INTO KnownFor (peopleId, movShowId) VALUES (%s, %s)"
    for x in known_for:
        val = (person_id, x)
        cursor.execute(sql, val)
        mydb.commit()


def import_persons():
    persons_df = pd.read_csv("data/top_movies_and_shows_persons_details.csv")
    persons_df = persons_df.replace(np.nan, None)
    with alive_bar(len(persons_df), title="Importing persons") as bar:
        for _, row in persons_df.iterrows():
            sql = "INSERT INTO People (id, Name, BirthYear, DeathYear) VALUES (%s, %s, %s, %s)"

            # Deathyear is \n if alive
            deathYear = row["DeathYear"]
            if deathYear == '\\N':
                deathYear = None

            # Birthyear can be \\N for some reason
            birthYear = row["BirthYear"]
            if birthYear == '\\N':
                birthYear = None

            if row["Name"] == '\\N':
                print(row["Name"], "is wierd")
                continue

            val = (row["personId"], row["Name"],
                   birthYear, deathYear)

            cursor.execute(sql, val)
            mydb.commit()

            # Add professions
            if row["Profession"] is not None:
                professions = row["Profession"].split(",")
                if len(professions) > 0:
                    add_professions(row["personId"], professions)

            if row["KnownForTitles"] is not None:
                known_for = row["KnownForTitles"].split(",")
                if len(known_for) > 0:
                    add_known_for(row["personId"], known_for)

            bar()


def import_roles():
    persons_df = pd.read_csv("data/top_movies_and_shows_persons.csv")
    persons_df = persons_df.replace(np.nan, None)
    with alive_bar(len(persons_df), title="Importing roles") as bar:
        for _, row in persons_df.iterrows():
            sql = "INSERT INTO Roles (movShowId, peopleId, category, `character`, ordering) VALUES (%s, %s, %s, %s, %s)"

            characters = row["characters"]
            if characters is None or characters == '\\N':
                bar()
                continue

            try:
                characters = json.loads(characters)
            except json.JSONDecodeError:
                print(f"Invalid JSON in characters: {characters}")
                bar()
                continue

            if len(characters) == 0:
                bar()
                continue

            for character in characters:

                val = (row["id"], row["personId"],
                       row["Category"], character, row["ordering"],)
                cursor.execute(sql, val)
                mydb.commit()
            bar()


def import_movies_and_shows():
    titles_df = pd.read_csv("data/top_movies_and_shows_titles.csv")
    titles_df = titles_df[["id", "Title", "StartYear",
                           "EndYear", "Runtime", "Type"]]
    titles_df = titles_df.replace(np.nan, None)

    sql = "INSERT INTO MoviesAndShows (id, Title, StartYear, EndYear, Runtime, Type) VALUES (%s, %s, %s, %s, %s, %s)"
    with alive_bar(len(titles_df), title="Importing movies and shows") as bar:
        for _, row in titles_df.iterrows():
            val = (row["id"], row["Title"],
                   row["StartYear"], row["EndYear"],
                   row["Runtime"], row["Type"])

            cursor.execute(sql, val)
            mydb.commit()
            bar()


def import_ratings():
    ratings_df = pd.read_csv("data/top_movies_and_shows.csv")
    ratings_df = ratings_df[["tconst", "averageRating", "numVotes"]]
    ratings_df = ratings_df.replace(np.nan, None)

    sql = "INSERT INTO Ratings (movShowId, avgRating, numVotes) VALUES (%s, %s, %s)"
    with alive_bar(len(ratings_df), title="Importing ratings") as bar:
        for _, row in ratings_df.iterrows():
            val = (row["tconst"], row["averageRating"], row["numVotes"])
            cursor.execute(sql, val)
            mydb.commit()
            bar()


if __name__ == "__main__":
    # download_dataset()
    # unpack_dataset_files()
    # get_most_important_data()

    executeScriptsFromFile("sql/createTables.sql")
    mydb.commit()

    run_mysql_cli_import("sql/addRating.sql")

    cursor.execute("USE `MovieTvDatabase`;")

    import_movies_and_shows()
    import_ratings()
    import_persons()
    import_roles()

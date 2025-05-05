import pandas as pd


def get_most_important_data():
    ratings_df = pd.read_csv("data/title.ratings.tsv", sep="\t")
    ratings_df = ratings_df.sort_values(by="numVotes", ascending=False)
    ratings_df = ratings_df.reset_index(drop=True)
    ratings_df = ratings_df[["tconst", "averageRating", "numVotes"]]

    # Get the top 10000 movies and shows
    top_n_titles = ratings_df.head(10000)

    # Save to CSV
    top_n_titles.to_csv("data/top_movies_and_shows.csv", index=False)

    # Get the most rated movies and shows
    titles_df = pd.read_csv("data/title.basics.tsv", sep="\t")
    titles_df = titles_df[["tconst", "primaryTitle", "startYear",
                           "endYear", "runtimeMinutes", "titleType"]]
    titles_df = titles_df[titles_df["tconst"].isin(top_n_titles["tconst"])]
    titles_df = titles_df.reset_index(drop=True)
    titles_df = titles_df.rename(columns={
        "tconst": "id",
        "primaryTitle": "Title",
        "startYear": "StartYear",
        "endYear": "EndYear",
        "runtimeMinutes": "Runtime",
        "titleType": "Type"
    })

    # Replace "\N" with N/A
    titles_df = titles_df.replace("\\N", "NULL")

    # Save to CSV
    titles_df.to_csv("data/top_movies_and_shows_titles.csv", index=False)

    # Get persons involved in the movies and shows
    title_principals = pd.read_csv(
        "data/title.principals.tsv", delimiter="\t")
    title_principals = title_principals[title_principals["tconst"].isin(
        top_n_titles["tconst"])]
    title_principals = title_principals.reset_index(drop=True)
    title_principals = title_principals.rename(columns={
        "tconst": "id",
        "nconst": "personId",
        "category": "Category",
        "job": "Job"
    })

    # Replace "\N" with N/A
    title_principals = title_principals.replace("\\N", "NULL")

    # Save to CSV
    title_principals.to_csv(
        "data/top_movies_and_shows_persons.csv", index=False)

    # Get personal details
    name_df = pd.read_csv("data/name.basics.tsv", sep="\t")
    name_df = name_df[["nconst", "primaryName", "birthYear",
                       "deathYear", "primaryProfession", "knownForTitles"]]
    name_df = name_df[name_df["nconst"].isin(
        title_principals["personId"])]
    name_df = name_df.reset_index(drop=True)
    name_df = name_df.rename(columns={
        "nconst": "personId",
        "primaryName": "Name",
        "birthYear": "BirthYear",
        "deathYear": "DeathYear",
        "primaryProfession": "Profession",
        "knownForTitles": "KnownForTitles"
    })
    # Replace "\N" with N/A
    name_df = name_df.replace("\\N", "NULL")

    # Save to CSV
    name_df.to_csv(
        "data/top_movies_and_shows_persons_details.csv", index=False)

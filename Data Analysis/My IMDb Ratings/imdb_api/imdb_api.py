# ------------------------------------ imports ----------------------------- #

import requests
import pandas as pd
from dataclasses import dataclass, asdict


# ------------------------------------ variables --------------------------- #

file_api_key:str = "imdb_api/api_key.txt"

file_ratings:str = "import_files/ratings.csv"

api_endpoint:str = "http://www.omdbapi.com/"


# ------------------------------------ functions & classes ----------------- #

@dataclass
class Film:
    film_id:str
    title:str
    director:str
    writer:str
    actors:str
    box_office:str
    title_type:str
    genre:str
    year:int
    rated:str
    released:str
    runtime:str
    language:str
    country:str
    awards:str
    imdb_rating:str
    imdb_votes:str


class GetFilms:
    """ This class will handle the API retrieving of data """
    
    def __init__(self,
                 api_key:str, 
                 films:list,
                 url:str = api_endpoint,
                 plot:str = "short",
                 r = "json"):
        
        self.api_key = api_key
        self.films = films
        self.url = url
        self.plot = plot
        self.r = r

    def __str__(self):
        return f"api_key:{self.api_key}, films:{self.films}, url:{self.url}, plot:{self.plot}, r:{self.r}"
    
    def get_film(self):

        output_films:list[Film] = []
        
        for film in self.films:
            
            payload = {"i": film, 
                        "plot": self.plot, 
                        "r": self.r, 
                        "apikey": self.api_key}
            
            retrieved_film:dict = requests.get(self.url, params=payload).json()

            current_film:Film = Film(
                film_id=retrieved_film.get("imdbID"),
                title=retrieved_film.get("Title"),
                director=retrieved_film.get("Director"),
                writer=retrieved_film.get("Writer"),
                actors=retrieved_film.get("Actors"),
                box_office=retrieved_film.get("BoxOffice"),
                title_type=retrieved_film.get("Type"),
                genre=retrieved_film.get("Genre"),
                year=retrieved_film.get("Year"),
                rated=retrieved_film.get("Rated"),
                released=retrieved_film.get("Released"),
                runtime=retrieved_film.get("Runtime"),
                language=retrieved_film.get("Language"),
                country=retrieved_film.get("Country"),
                awards=retrieved_film.get("Awards"),
                imdb_rating=retrieved_film.get("imdbRating"),
                imdb_votes=retrieved_film.get("imdbVotes")
            )
            output_films.append(current_film)
        
        return output_films


def import_file_txt(filename:str):
    file = open(filename, "r")
    file_ouptut = file.read()
    file.close()
    return file_ouptut


def import_file_csv(filename:str):
    file_ouptut = pd.read_csv(filename)
    return file_ouptut


def dataclass_to_csv(film:list, ratings, filename:str):
    df = pd.json_normalize(asdict(obj) for obj in film)
    df = df.merge(ratings, how="left", on="film_id")
    df = df[~df["film_id"].isnull()]
    df.to_csv(f"{filename}.csv", index=False)


def titles_to_export(df):
    list_title_type:list = ["tvMovie", "movie"]
    df = df[df["Title Type"].isin(list_title_type)].reset_index(drop = True)
    df = df[["Const", "Your Rating", "Date Rated"]]
    df = df.rename(columns = {"Const": "film_id", "Your Rating": "my_rating",
                    "Date Rated": "rated_date"})
    
    return df


def titles_list(df):
    lst:list = []
    lst = df["film_id"].tolist()

    return lst


# ------------------------------------ main --------------------------------- #

api_key = import_file_txt(file_api_key)

raw_ratings = import_file_csv(file_ratings)

ratings = titles_to_export(raw_ratings)

titles = titles_list(ratings)

film_output = GetFilms(api_key=api_key, films=titles)

films = film_output.get_film()

dataclass_to_csv(films, ratings, "import_files/films")

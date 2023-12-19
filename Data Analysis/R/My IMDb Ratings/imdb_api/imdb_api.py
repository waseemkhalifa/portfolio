# ------------------------------------ imports ----------------------------- #

import requests
import pandas as pd
from dataclasses import dataclass, astuple, fields, asdict
import csv


# ------------------------------------ variables --------------------------- #

file_api_key:str = "imdb_api/api_key.txt"

file_films:str = "imdb_analysis/ratings.csv"

api_endpoint:str = "http://www.omdbapi.com/"


# ------------------------------------ functions & classes ----------------- #

def import_file_txt(filename:str):
    file = open(filename, "r")
    file_ouptut = file.read()
    file.close()
    return file_ouptut


def import_file_csv(filename:str):
    file_ouptut = pd.read_csv(filename)
    return file_ouptut


def dataclass_to_csv(film:list, filename:str):
    df = pd.json_normalize(asdict(obj) for obj in film)
    df.to_csv(f"{filename}.csv", index=False)


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

    def __iter__(self):
        return iter(astuple(self))


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


# ------------------------------------ main --------------------------------- #

api_key = import_file_txt(file_api_key)

films = import_file_csv(file_films)

test = ["tt0100150", "tt0100157"]

film_output = GetFilms(api_key=api_key, films=test)

film = film_output.get_film()

dataclass_to_csv(film, "film")






# ------------------------------------ imports ----------------------------- #
import requests
import pandas as pd


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


class Films:
    """ This class will handle the API retrieving of data """
    
    def __init__(self,
                 api_key:str, 
                 films:list,
                 url:str = api_endpoint,
                 plot:str = "short",
                 r = "json"):
        
        self.api_key = api_key, 
        self.films = films,
        self.url = url,
        self.plot = plot,
        self.r = r
    
    def get_film(self):
        
        for film in self.films:
            
            payload = {"i": film, 
                        "plot": self.plot, 
                        "r": self.r, 
                        "apikey": self.api_key}
            
            self.retrieved_film = requests.get(self.url, params=payload).json()

            self.output_films = self.output_films + self.retrieved_film
        
        return self.output_films




# ------------------------------------ main --------------------------------- #
api_key = import_file_txt(file_api_key)

films = import_file_csv(file_films)

test = ["tt0100150", "tt0100157"]

film_output = Films(api_key=api_key, films=test)

film_output.get_film()





















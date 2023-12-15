# ------------------------------------ imports ----------------------------- #
import requests
import pandas as pd


# ------------------------------------ variables --------------------------- #
file_api_key:str = "imdb_api/api_key.txt"
file_films:str = "imdb_analysis/ratings.csv"

api_endpoint:str = "http://www.omdbapi.com/"


# ------------------------------------ functions --------------------------- #
def import_file_txt(filename:str):
    file = open(filename, "r")
    file_ouptut = file.read()
    file.close()
    return file_ouptut

def import_file_csv(filename:str):
    file_ouptut = pd.read_csv(filename)
    return file_ouptut


class Films:
    """ This class will handle the API import and retrieving of data """
    
    def __init__(self,
                 api_key:str, 
                 films:list,
                 url:str = api_endpoint,
                 plot:str = "short",
                 r = "json"):
        

payload = {"i": "tt0099685", "plot": "short", "r": "json", 'apikey': api_key}
data = requests.get("http://www.omdbapi.com/", params=payload).json()



# ------------------------------------ main --------------------------------- #
api_key = import_file_txt(file_api_key)

films = import_file_csv(file_films)




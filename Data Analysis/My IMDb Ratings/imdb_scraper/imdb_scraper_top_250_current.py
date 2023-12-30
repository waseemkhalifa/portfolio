# ------------------------------------ imports ----------------------------- #

import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd


# ------------------------------------ variables --------------------------- #
# URL of the website to scrape
url = "https://www.imdb.com/chart/top/"

request = Request(url , headers={"User-Agent": "Mozilla/5.0"})

films:dict = {
    "film_id":[],
    "title":[],
    "ranking":[],
    "year":[],
    "imdb_rating":[],
    "my_rating":[]
}

file_name:str = "import_files/imdb_top_250_current"


# ------------------------------------ functions & classes ----------------- #

def get_request(request):
    """ Scrapes the raw data from the provided URL """
    response = urlopen(request).read()
    return response


def parse_request(response):
    """ Parses the scraped raw data """
    parsed = BeautifulSoup(response, "html.parser")
    return parsed


def get_films(parsed, films:dict) -> dict:
    """ Gets the film_ids, titles and ranking and appends to a dict """
    for film in parsed.find_all(class_="ipc-title-link-wrapper"):
        if "title" in film.attrs.get("href", "Not Found"):
            films["film_id"].append(film.attrs.get("href", "Not Found").split("/")[2].split("/")[0])
        
        if "." in film.get_text():
            films["ranking"].append(film.get_text().split(".")[0].strip())

        if "." in film.get_text():
            films["title"].append(film.get_text().split(".")[1].strip())
    
    for film in parsed.find_all(class_="sc-43986a27-8 jHYIIK cli-title-metadata-item"):
        if any(i.isdigit() for i in film):
            if len(film.get_text()) == 4:
                films["year"].append(film.get_text())
    
    for film in parsed.find_all(class_="ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb sc-9ab53865-1 iXEijC ratingGroup--imdb-rating"):
        films["imdb_rating"].append(film.get_text()[0:3])

    return films


def dict_to_csv(films:dict, filename:str):
    """ Creates a dataframe from the dictionary and exports as a csv """
    df = pd.DataFrame.from_dict(films)
    df.to_csv(f"{filename}.csv", index=False)


# ------------------------------------ main --------------------------------- #
def main(request:str, films:dict, file_name:file_name):

    response = get_request(request)

    parsed = parse_request(response)

    films = get_films(parsed, films)

    dict_to_csv(films, file_name)


main(request, films, file_name)


# this gets year
for film in parsed.find_all("aria-label"):
    film


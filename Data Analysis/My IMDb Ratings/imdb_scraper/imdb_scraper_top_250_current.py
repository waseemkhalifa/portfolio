# ------------------------------------ imports ----------------------------- #

import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd


# ------------------------------------ variables --------------------------- #
# URL of the website to scrape
url = "https://www.imdb.com/chart/top/"

req = Request(url , headers={'User-Agent': 'Mozilla/5.0'})

film_ids = []
titles = []


# ------------------------------------ functions & classes ----------------- #

def get_request(req):
    """ Scrapes the raw data from the provided URL """
    response = urlopen(req).read()
    return response


def parse_request(response):
    """ Parses the scraped raw data """
    parsed = BeautifulSoup(response, "html.parser")
    return parsed


def get_film_id(parsed, film_ids:list):
    """ Gets the film_ids on the current page and appends to a list """
    for t in parsed.find(class_="list-data").find_all("td", style="width: 90%;"):
        text:str = t.find("a").attrs.get("href", "Not Found")
        text = text.split("/",2)[2]
        film_ids.append(text)
    return film_ids

def get_title(parsed, titles:list):
    """ Gets the titles on the current page and appends to a list """
    for t in parsed.find(class_="list-data").find_all("td", style="width: 90%;"):
        text:str = t.find("a").get_text()
        titles.append(text)
    return titles


def lists_to_csv(film_ids:list, titles:list, years:list, highest_ranks:list, 
                 first_entry_dates:list, filename:str):
    """ Creates a dataframe from the lists and exports as a csv """
    df = pd.DataFrame(list(zip(film_ids, titles, years, highest_ranks, 
                               first_entry_dates)),
                        columns =["film_id", "title", "year", 
                                  "highest_rank", "first_entry_date"])
    df.to_csv(f"{filename}.csv", index=False)


# ------------------------------------ main --------------------------------- #
def main(url:str, film_ids:list, titles:list):

    response = get_request(req)

    parsed = parse_request(response)

    parsed.find_all(class_="ipc-title__text")
    parsed.find_all(class_="ipc-title-link-wrapper")

    film_ids = get_film_id(parsed, film_ids)

    titles = get_title(parsed, titles)

    lists_to_csv(film_ids, titles, "import_files/imdb_top_250_all")


main(url, film_ids, titles)


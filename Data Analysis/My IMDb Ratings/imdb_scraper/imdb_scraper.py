# ------------------------------------ imports ----------------------------- #

import requests
from bs4 import BeautifulSoup
import pandas as pd


# ------------------------------------ variables --------------------------- #
# URL of the website to scrape
url = "https://250.took.nl/titles/index/page:"

current_page = 1
current_titles = 0
max_titles = 1

film_ids = []
titles = []
years = []
highest_ranks = []
first_entry_dates = []


# ------------------------------------ functions & classes ----------------- #

def get_request(url:str, current_page:int):
    """ Scrapes the raw data from the provided URL """
    response = requests.get(f"{url}{current_page}")
    return response


def parse_request(response):
    """ Parses the scraped raw data """
    parsed = BeautifulSoup(response.content, "html.parser")
    return parsed


def get_max_titles(parsed):
    """ Gets the maximum number of titles on the site """
    max_titles = parsed.find(class_="text-center space-above").find("p").get_text()
    max_titles = max_titles.strip()
    max_titles = max_titles.split(" ")[-2]
    return max_titles


def get_current_titles(parsed):
    """ Gets the maximum number of titles on the current page """
    current_titles = parsed.find(class_="text-center space-above").find("p").get_text()
    current_titles = current_titles.strip()
    current_titles = current_titles.split(" ")[1].split("-")[1]
    return current_titles


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


def get_year(parsed, years:list):
    """ Gets the year of release on the current page and appends to a list """
    for t in parsed.find(class_="list-data").find_all(class_="hidden-links"):
        text:str = t.find("a").get_text()
        years.append(text)
    return years


def get_highest_rank(parsed, highest_ranks:list):
    """ Gets the highest rank on the current page and appends to a list """
    for t in parsed.find(class_="list-data").find_all(class_="tac hidden-xs hidden-sm"):
        text:str = t.find("span").get_text()
        highest_ranks.append(text)
    return highest_ranks


def get_first_entry_date(parsed, first_entry_dates:list):
    """ Gets the first entry dates on the current page and appends to a list """
    for t in parsed.find(class_="list-data").find_all("td", class_="nowrap tac hidden-xs"):
        if t.find("a") != None:
            text:str = t.find("a").attrs.get("href", "Not Found")
            text = text.split("/",2)[2]
            first_entry_dates.append(text)
    return first_entry_dates


def lists_to_csv(film_ids:list, titles:list, years:list, highest_ranks:list, 
                 first_entry_dates:list, filename:str):
    """ Creates a dataframe from the lists and exports as a csv """
    df = pd.DataFrame(list(zip(film_ids, titles, years, highest_ranks, 
                               first_entry_dates)),
                        columns =["film_id", "title", "year", 
                                  "highest_rank", "first_entry_date"])
    df.to_csv(f"{filename}.csv", index=False)


# ------------------------------------ main --------------------------------- #
def main(url:str, 
         current_page:int, 
         current_titles:int, 
         max_titles:int,
         film_ids:list,
         titles:list,
         years:list,
         highest_ranks:list, 
         first_entry_dates:list):
    
    while current_titles != max_titles:

        response = get_request(url, current_page)

        parsed = parse_request(response)
        
        current_page+=1

        current_titles = get_current_titles(parsed)

        max_titles = get_max_titles(parsed)

        film_ids = get_film_id(parsed, film_ids)
        titles = get_title(parsed, titles)
        years = get_year(parsed, years)
        highest_ranks = get_highest_rank(parsed, highest_ranks)
        first_entry_dates = get_first_entry_date(parsed, first_entry_dates)

    lists_to_csv(film_ids, titles, years, highest_ranks, first_entry_dates, 
                 "My IMDb Ratings/imdb_analysis/imdb_top_250_all")


main(url, current_page, current_titles, max_titles, film_ids, titles, years, 
     highest_ranks, first_entry_dates)

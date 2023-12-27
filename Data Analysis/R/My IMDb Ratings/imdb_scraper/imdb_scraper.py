import requests

from bs4 import BeautifulSoup
import pandas as pd


# URL of the website to scrape
url = "https://250.took.nl/titles/index/page:1"


# Send an HTTP GET request to the website
response = requests.get(url)


# Parse the HTML code using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')


# Extract the relevant information from the HTML code
films = []
for row in soup.find(class_='list-data'):
    print(row)
    break


    title = row.find('td', class_='titleColumn').find('a').get_text()
    films.append([title])

    soup.find(class_='list-data').find('a').get_text()


# shows film_id and title
for title in soup.find(class_='list-data').find_all('a'):
    print(title)


# shows title
for title in soup.find(class_='list-data').find_all('td', style="width: 90%;"):
    print(title.find('a').get_text())


# shows year
for title in soup.find(class_='list-data').find_all(class_="hidden-links"):
    print(title.find('a').get_text())






# Store the information in a pandas dataframe
df = pd.DataFrame(films, columns=['Title', 'Year', 'Rating'])




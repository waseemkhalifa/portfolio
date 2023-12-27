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


# shows film_id
for title in soup.find(class_='list-data').find_all('td', style="width: 90%;"):
    text:str = title.find('a').attrs.get('href', 'Not Found')
    text = text.split("/",2)[2]
    print(text)


# shows title
for title in soup.find(class_='list-data').find_all('td', style="width: 90%;"):
    print(title.find('a').get_text())


# shows year
for title in soup.find(class_='list-data').find_all(class_="hidden-links"):
    print(title.find('a').get_text())


# shows the highest rank
for title in soup.find(class_='list-data').find_all(class_="tac hidden-xs hidden-sm"):
    print(title.find('span').get_text())


# shows first entry date
for title in soup.find(class_='list-data').find_all("td", class_="nowrap tac hidden-xs"):
    if title.find("a") != None:
        text:str = title.find('a').attrs.get('href', 'Not Found')
        text = text.split("/",2)[2]
        print(text)
    






# Store the information in a pandas dataframe
df = pd.DataFrame(films, columns=['Title', 'Year', 'Rating'])




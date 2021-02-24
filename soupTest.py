import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

start_url = 'https://en.wikipedia.org/wiki/Tesla,_Inc.'

downloaded_html = requests.get(start_url)

soup = BeautifulSoup(downloaded_html.text)

with open('downloaded.html', 'w') as file:
    file.write(soup.prettify())

for link in soup.findAll('a', href=True):
    print(link['href'])
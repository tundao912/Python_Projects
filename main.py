import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

#start_url = 'https://en.wikipedia.org/wiki/Tesla,_Inc.'

#downloaded_html = requests.

soup = BeautifulSoup(open('downloaded.html'),'html.parser')

with open('downloaded.html', 'w') as file:
    file.write(soup.prettify())

full_table = soup.select('a')
print(full_table)
#
# for element in table_head:
#     column_label = element.get_text(separator=" ", strip=True)
#     column_label = column_label.replace(' ', '_')
#     column_label = regex.sub('', column_label)
#     table_columns.append(column_label)

# table_rows = full_table.select('tr')
# table_data =[]
# for index, element in enumerate(table_rows):
#     if index > 0:
#         row_list = []
#         values = element.select('td')
#         for value in values:
#             row_list.append(value.text.strip())
#         table_data.append(row_list)
#
#
# df = pd.DataFrame(table_data, columns=table_columns)
#
# print(df)
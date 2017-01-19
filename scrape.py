# coding: utf-8

import requests
from bs4 import BeautifulSoup as bs
import re


request = requests.get('http://www.bbc.com/sport/football/premier-league/table')
page = request.text
soup = bs(page, 'lxml')
table_html = soup.find("table", "table-stats")
table = table_html.find("tbody")

# empty list for table data
data = []

rows = table.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele])

output = []
output.append(['Pos:',' -------------Team---------------- ','G:  ','W:  ','L:  ', 'GF: ', 'GA: ', 'GD: ', 'Pt: ', 'Form: ', 'Last 6:'])

print data[0]

print ''.join(output[0])
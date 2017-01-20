# coding: utf-8

import requests
from bs4 import BeautifulSoup as bs
import re


request = requests.get('http://www.bbc.com/sport/football/premier-league/table')
page = request.text
soup = bs(page, 'html.parser')
table_html = soup.find("table", "table-stats")
table = table_html.find("tbody")

# empty list for table data
data = []

rows = table.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele])

header = []
header.append(['Pos:',' -------------Team----------------- ','G:  ','W:  ','D:  ','L:  ', 'GF:  ', 'GA:  ', 'GD:  ', 'Pt:  ', 'Form: ', 'Last 6:'])

print(''.join(header[0]))

output = []

i = 1
for line in data:
    last10 = line[10].replace('\n','').replace('Win','W').replace('Loss', 'L').replace('Draw', 'D')
    last6 = last10[:6]
    form = str(last6.count('W') * 3 + last6.count('D'))
    output.append([str(i).ljust(4),line[1].ljust(36), line[2].ljust(4), line[3].ljust(4), line[4].ljust(4),line[5].ljust(4),line[6].ljust(5),line[7].ljust(5), line[8].ljust(5), line[9].ljust(5), form.ljust(6), last6[:6].ljust(9)])

    i += 1

for line in output:
    print(''.join(line))

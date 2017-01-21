#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
# coding: utf-8

import requests
from bs4 import BeautifulSoup as bs
import re
import datetime
from dateutil import tz

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
header.append(['Pos: ','Team:                               ','G:  ','W:  ','D:  ','L:  ', 'GF:  ', 'GA:  ', 'GD:  ', 'Pt:  ', 'Form: ', 'Last 6:'])

print 'Current Table:\n'
print ''.join(header[0])

output = []

i = 1
for line in data:
    last10 = line[10].replace('\n','').replace('Win','W').replace('Loss', 'L').replace('Draw', 'D')
    last6 = last10[:6]
    form = str(last6.count('W') * 3 + last6.count('D'))
    output.append([str(i).ljust(5),line[1].ljust(36), line[2].ljust(4), line[3].ljust(4), line[4].ljust(4),line[5].ljust(4),line[6].ljust(5),line[7].ljust(5), line[8].ljust(5), line[9].ljust(5), form.ljust(6), last6[:6].ljust(9)])

    i += 1

for line in output:
    print ''.join(line)


print '----------------------------------------------------------------------------------------------------------------'
print 'Next 10 Games Are:\n'
print 'Home:'.ljust(37),'Away:'.ljust(30),'Date:'.ljust(12), 'Time:'

request = requests.get('http://www.bbc.com/sport/football/premier-league/fixtures')
page = request.text
soup = bs(page, 'html.parser')
table_html = soup.find_all('table', 'table-stats')

data = []
#get fixture row

for tables in table_html:
    table = tables.find_all("tbody")
    # get match date
    cap = str(tables.caption).split()
    year = cap[9][:4]
    if year.isdigit():
        month = cap[8]
        day = cap[7][:-2].zfill(2)

        for i in table:
            rows = i.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                cols.append(year)
                cols.append(month)
                cols.append(day)
                data.append([ele for ele in cols if ele])
    else:
        pass

for j in range(len(data)):
    if j<10:
        home = data[j][1].replace('\n','').split(' V ')[0]
        away = data[j][1].replace('\n','').split(' V ')[1]

        hh = data[j][2].split(':')[0].zfill(2)
        mm = data[j][2].split(':')[1].zfill(2)

        yyyymmdd = data[j][-3] + data[j][-2] + data[j][-1] + hh + mm
        matchdate = datetime.datetime.strptime(yyyymmdd, "%Y%B%d%H%M")

        HERE = tz.tzlocal()
        GMT = tz.gettz('GMT')

        now = matchdate.replace(tzinfo=GMT).astimezone(HERE)
        # only print if less than 10
        print home.ljust(32),'vs', away.ljust(32), now.date(),' ', now.time().strftime('%H:%M')
    else:
        break
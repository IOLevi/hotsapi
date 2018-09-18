#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup

r = requests.get('http://hotslogs.com')
pagehtml = r.text

# # write the file just in case
# with open('hotsdump.html', 'w', encoding='utf-8') as f:
#     f.write(pagehtml)

soup = BeautifulSoup(pagehtml, 'html.parser')

for row in soup.find('tbody').find_all('tr'):
    heroName = row.find('a')['title']
    fields = row.find_all('td')
    gamesPlayed = int(fields[2].string) 
    gamesBanned = float(fields[3].string) 
    participation = float(fields[4].string)
    winRate = float(fields[5].string)
    change = float(fields[6].string)
    heroClass = fields[7].string
    heroSubclass = fields[8].string

#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
# from dbs import storage
# from herotemplate import HeroTemplate

r = requests.get('http://hotslogs.com')
pagehtml = r.text


# # write the file just in case
# with open('hotsdump.html', 'w', encoding='utf-8') as f:
#     f.write(pagehtml)

soup = BeautifulSoup(pagehtml, 'html.parser')

def rc(target):
    """format hotslogs input for castings to primatives"""
    i = target.find(',')
    if i > -1:
        target = target[0:i] + target[i+1::]

    i = target.find(' %')
    if i > -1:
        target = target[0:i] + target[i+2::]
    return target

for row in soup.find('tbody').find_all('tr'):
    attrs = {}
    attrs['heroName'] = row.find('a')['title']
    fields = row.find_all('td')
    attrs['gamesPlayed'] = int(rc(fields[2].string)) 
    attrs['gamesBanned'] = int(rc(fields[3].string)) 
    attrs['winRate'] = float(rc(fields[5].contents[0]))
    attrs['change'] = float(rc(fields[6].string))
    attrs['heroClass'] = fields[7].string
    attrs['heroSubclass'] = fields[8].string
    attrs['participation'] = float(rc(fields[4].contents[0]))
    print(attrs)
    hero = HeroTemplate(**attrs)
    hero.save()
    
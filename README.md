# Hotslogs rankings scraper

Objective is to scrape winrates from hotslogs to convert it into a workable API

TODO:
-- figure out whether scrape.py should overwrite old data?
-- maybe I should make a new table every time i scrape...? 
--hots log doesn't do history charts that well. Maybe have a way to combine them  

Stretch
-- host the api on my web1 server
-- connect it with a webapp or a mobile app so I can play with the data
-- maybe connect with trello to ping my phone with today's top 2/3 of each hero class
-- output a suggested pick/bans list based on the current winrates that the API scrapes
-- create spreadsheets based off data from the heroes.json, such as damage/sec from autos
    --most burst possible
    --healing/sec
    --effective hp after armor/average

-- i could scrape the matchups and in the recommended ban, look at heroes that you have drafted and then suggest bans where matchup winrate is < 45 ... 
cronjob?
in game overlay
heroespatchnotes.com is a good model
https://getbootstrap.com/docs/4.1/utilities/borders/ bootstrap docs
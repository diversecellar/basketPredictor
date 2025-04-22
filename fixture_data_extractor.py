# to make and cbange directories
import dt_prompter
import os
import glob
import sys
import platform
import re

# Library for opening url and creating
# requests
import urllib.request

# pretty-print python data structures
from pprint import pprint

# for parsing all the tables present
# on the website
from html_table_parser.parser import HTMLTableParser

# for converting the parsed data in a
# pandas dataframe
import pandas as pd

# governing bs objects
from bs4 import BeautifulSoup

# date
import datetime as dt

#plotter
import matplotlib.pyplot as plt
#import seaborn as sns
import numpy as np

OSListWin = ["Windows", "windows", "WINDOWS"]
OSListLin = ["Linux", "linux", "LINUX"]

promptOS = platform.system()

if promptOS not in OSListLin+OSListWin:
    print("No valid OS used")
    sys.exit()

else:
    print("Operating system: "+promptOS)
    print("Starting to process game data...")

# Month abbreviation, day and year
today = dt.date.today()
date_today = today.strftime("%b-%d-%Y")
date_prompt = dt_prompter.date_prompt2
default = os.getcwd()

date_now = dt.datetime.now() - dt.timedelta(days = date_prompt)
print("Date of Interest: ",date_now)

date_year_now = date_now.strftime('%Y')
date_day_now = date_now.strftime('%d')
date_month_now = date_now.strftime('%B')[0:3]
date_month_now_1 = date_now.strftime('%B').lower()
date_month_now_2 = date_now.strftime('%m')

date_minus = date_now - dt.timedelta(days = 1)
date_year_minus = date_minus.strftime('%Y')
date_day_minus = date_minus.strftime('%d')
date_month_minus = date_minus.strftime('%B')[0:3]
date_month_minus_1 = date_minus.strftime('%B').lower()
date_month_minus_2 = date_minus.strftime('%m')

date_last = date_now - dt.timedelta(days = 30)
date_year_last = date_last.strftime('%Y')
date_day_last = date_last.strftime('%d')
date_month_last = date_last.strftime('%B')[0:3]
date_month_last_1 = date_last.strftime('%B').lower()
date_month_last_2 = date_last.strftime('%m')


lookup_date_format = "{month} {day}, {year}".format(month = date_month_minus, day = str(int(date_day_minus)), year = date_year_minus)

if date_month_last != date_month_now:
    premier_league_list = ['https://www.basketball-reference.com/leagues/NBA_2025_games-{month}.html'.format(month = date_month_last_1),
                           'https://www.basketball-reference.com/leagues/NBA_2025_games-{month}.html'.format(month = date_month_now_1)]

else:
    premier_league_list = ['https://www.basketball-reference.com/leagues/NBA_2025_games-{month}.html'.format(month = date_month_now_1)]

# loop over all leagues
for league in premier_league_list:
    #print(league)

    #extract league name
    if promptOS in OSListLin:
        my_folder = league.rsplit('/', 1)[-1]

    elif promptOS in OSListWin:
        my_folder = league.rsplit('/', 1)[-1]
        my_folder = my_folder[:-5]

    month = league.rsplit('/', 1)[-1]
    month = month.rsplit(".", 1)[0]
    month = month.rsplit("-", 1)[-1]

    print("---> Month: {}".format(month))

    print("---| Creating today's folder")


    # creating and changing to a directory for each league
    if not os.path.exists("{year}{month}{day}/FIXTURES".format(month = date_month_now_2, day = date_day_now, year = date_year_now[2:])):
        os.makedirs("{year}{month}{day}/FIXTURES".format(month = date_month_now_2, day = date_day_now, year = date_year_now[2:]))
    os.chdir("{year}{month}{day}/FIXTURES".format(month = date_month_now_2, day = date_day_now, year = date_year_now[2:]))
    statsFolder = os.getcwd()
    print(statsFolder)

    def get_links(url, reg_ex):

        # Add wiki url to html target
        html = urllib.request.urlopen(url=url)
        bs = BeautifulSoup(html, 'html.parser')
        link_result = bs.find('div',{'id':'div_schedule'}).find_all(
        'a', href=re.compile(reg_ex))
        return link_result

    # Opens a website and read its
    # binary contents (HTTP Response Body)
    def url_get_contents(url):

        # making request to the website
        req = urllib.request.Request(url=url)
        f = urllib.request.urlopen(req)

        # reading contents of the website
        return f.read()

    reg_ex_array = ['(/boxscores/)(?=index.)', '(/teams/)(?=.)']

    print("---| Getting page links")

    # extracts the date links for each fixture
    teams_links_2 = get_links("{}".format(league), reg_ex_array[0])
    fixtures_list = []
    for team_index_2 in range(len(teams_links_2)):
        teams_2 = teams_links_2[team_index_2].contents[0]
        fixtures_list.append(teams_2)

    # extracts the team pairs in each fixture
    teams_links = get_links("{}".format(league), reg_ex_array[1])
    teams_games = []
    for team_index in range(len(teams_links)):
        teams = teams_links[team_index].contents[0]
        teams_games.append(teams)
    team_pairs = []
    for teams_index in range(len(teams_games)):
        team_pair = teams_games[2*teams_index:2*(teams_index+1)]
        team_pairs.append(team_pair)

    # indexes each fixture in the game list
    fixtures_idx = [idx for idx, s in enumerate(fixtures_list) if "{}".format(lookup_date_format) in s]

    # compiles a list of home and away teams for dataframe construction (could be reworked)
    print("---| Compiling fixture data")
    today_teams_0 = []
    today_teams_1 = []
    for fixture_idx in fixtures_idx:
        today_teams = team_pairs[fixture_idx]
        print(today_teams)
        home_teams_str = today_teams[1].split(" ")[-1]
        away_teams_str = today_teams[0].split(" ")[-1]
        today_teams_0.append(home_teams_str.upper())
        today_teams_1.append(away_teams_str.upper())

    print("---| Saving data to excel")
    if len(fixtures_idx) > 0:
        data_fixtures = pd.DataFrame(list(zip(today_teams_0, today_teams_1)), columns = ['Away', 'Home'])
        data_fixtures.to_excel("FIXTURES.xlsx", index = False, header=True)
    print("Done processing game data.")
    os.chdir(default)
os.chdir(default)
os.chdir("{year}{month}{day}/FIXTURES".format(month = date_month_now_2, day = date_day_now, year = date_year_now[2:]))
os.system("start EXCEL.EXE FIXTURES.xlsx")
#os.chdir(default)
#exec(open('time-series_data-analysis.py').read())
os.chdir(default)
os.chdir("{year}{month}{day}".format(month = date_month_now_2, day = date_day_now, year = date_year_now[2:]))
exec(open('excel-file-opener.py').read())
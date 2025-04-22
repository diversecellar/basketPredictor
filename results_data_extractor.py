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
    premier_league_dict = {'https://www.basketball-reference.com/leagues/NBA_2025_games-{month}.html'.format(month = date_month_last_1):"last",
                           'https://www.basketball-reference.com/leagues/NBA_2025_games-{month}.html'.format(month = date_month_now_1):"now"}


else:
    premier_league_list = ['https://www.basketball-reference.com/leagues/NBA_2025_games-{month}.html'.format(month = date_month_now_1)]
    premier_league_dict = {'https://www.basketball-reference.com/leagues/NBA_2025_games-{month}.html'.format(month = date_month_now_1):"now"}

continental_teams = {}
cont_teams_pds = []
cont_teams_list = []
loc_teams_pds = []
loc_teams_list = []
local_teams = {}

def replace_unicode(item):
    item = str(item)
    if chr(237) in item or "Ã\xad" in item:
        item = item.replace(chr(237), 'i')
        item = item.replace("Ã\xad", "i")
    elif chr(233) in item or "Ã©" in item:
        item = item.replace(chr(233), 'e')
        item = item.replace("Ã©", 'e')
    elif chr(225) in item or "Ã¡" in item:
        item = item.replace(chr(225), 'a')
        item = item.replace("Ã¡", 'a')
    elif chr(243) in item or "Ã¶" in item:
        item = item.replace(chr(243), 'o')
        item = item.replace("Ã¶", 'o')
    elif chr(246) in item:
        item = item.replace(chr(246), 'o')
    elif chr(39) in item:
        item = item.replace(chr(39), "")
    else:
        item = item
    return item

file_names = ["NBA"]
teams_list = []
for file in file_names:
    team_file_name = file
    if os.path.exists("{year}{month}{day}/TEAMS-LIST".format(month = date_month_now_2, day = date_day_now, year = date_year_now[2:])):
        os.chdir("{year}{month}{day}/TEAMS-LIST".format(month = date_month_now_2, day = date_day_now, year = date_year_now[2:]))
    # Open the file in append & read mode ('a+')
    with open("{file}.txt".format(file = team_file_name), "r+") as teams_list_file:
    # Move read cursor to the start of file.
        items = teams_list_file.readlines()
        for item in items:
            teams_list.append(item.strip())
        teams_list_file.close()
    os.chdir(default)

# loop over all leagues
for league in premier_league_list:
    print(league)

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

    # defining the html contents of a URL.
    xhtml = url_get_contents("{}".format(league)).decode('utf-8')

    # Defining the HTMLTableParser object
    p = HTMLTableParser()

    # feeding the html contents in the
    # HTMLTableParser object
    p.feed(xhtml)
    all_month_games = p.tables[0]
    table_titles = all_month_games[0]
    table_data = all_month_games[1:]
    all_results_df = pd.DataFrame(table_data, columns=table_titles)
    scores_home_list = []
    dates_list = []
    ot_data_list = []
    scores_away_list = []
    teams_home_list = []
    teams_away_list = []
    for each_entry in table_data:
        dates_list.append(each_entry[0])
        ot_data_list.append(each_entry[7])
        teams_home_list.append(each_entry[4])
        scores_home_list.append(each_entry[5])
        scores_away_list.append(each_entry[3])
        teams_away_list.append(each_entry[2])

    # creating and changing to a directory for each league
    if not os.path.exists("LAST-SEVEN"):
        os.makedirs("LAST-SEVEN")
    os.chdir("LAST-SEVEN")
    resFolder = os.getcwd()
    print(resFolder)

    reg_ex_array = ['(/boxscores/)(?=index.)', '(/teams/)(?=.)']

    print("---| Getting page links")

    # extracts the date links for each fixture
    teams_links_2 = get_links("{}".format(league), reg_ex_array[0])
    fixtures_list = []
    for team_index_2 in range(len(teams_links_2)):
        teams_2 = teams_links_2[team_index_2].contents[0]
        fixtures_list.append(teams_2)

    scores_list = [s for s in fixtures_list if len(s) == 3]

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
    fixtures_idx = [idx for idx, s in enumerate(scores_home_list) if len(s) > 0]

    dates_list = dates_list[:]
    ot_data_list = ot_data_list[:]
    scores_home_list = scores_home_list[:]
    scores_away_list = scores_away_list[:]
    teams_home_list = teams_home_list[:]
    teams_away_list = teams_away_list[:]

    # indexes each fixture in the game list
    # fixtures_idx = []
    # fixtures_idx_build = [idx for idx, s in enumerate(scores_list)]
    # fixtures_idx += fixtures_idx_build

    # first_idx_date = fixtures_idx[-1]
    # print(first_idx_date)
    # all_scored_matches_idx = [] # this one is the list of all match indexes on fb-ref
    # for idx_matches in range(int(first_idx_date)):
    #     all_scored_matches_idx.append(idx_matches)
    # results_idx = all_scored_matches_idx
    # print(results_idx)

    def convert(date_time):
        format = '%b %d %Y'
        datetime_str = dt.datetime.strptime(date_time, format)
        return datetime_str

    for team in teams_list:
        print(team)
        # compiles a list of home and away teams for dataframe construction (could be reworked)
        print("---| Compiling fixture data")
        team_name = []
        today_teams_0 = []
        today_teams_1 = []
        today_score_0 = []
        today_dates = []
        today_score_1 = []
        game_diff_codes = []
        date_diff_codes = [None]*len(dates_list)
        for fixture_idx in fixtures_idx[:]:
            today_teams = team_pairs[fixture_idx]
            today_teams_0_const = teams_home_list[fixture_idx]
            today_teams_1_const = teams_away_list[fixture_idx]
            if str(today_teams_0_const) == str(team) or str(today_teams_1_const) == str(team):
                home_teams_str = today_teams_0_const.split(" ")[-1]
                away_teams_str = today_teams_1_const.split(" ")[-1]
                today_teams_0.append(home_teams_str.upper())
                today_teams_1.append(away_teams_str.upper())
                today_score_0.append(int(scores_home_list[fixture_idx]))
                today_score_1.append(int(scores_away_list[fixture_idx]))
                date_const = str(dates_list[fixture_idx])
                date_const = str(date_const.split(", ")[1])+" "+str(date_const.split(", ")[2])
                datetime_const = convert(date_const)
                today_dates.append(datetime_const)
                if ot_data_list[fixture_idx] == "OT":
                    game_diff_codes.append(int(1))
                else:
                    game_diff_codes.append(int(0))

        print("---| Saving data to excel")
        data_fixtures = pd.DataFrame(list(zip(today_teams_0, today_teams_1)), columns = ['Home', 'Away'])
        #data_fixtures.to_excel("FIXTURES.xlsx", index = False, header=True)
        #print(fixtures_idx)
        print("---| Saving data to excel")
        data_fixtures2 = pd.DataFrame(list(zip(today_dates, today_teams_0, today_score_0,
                                               today_score_1, today_teams_1, date_diff_codes,
                                               game_diff_codes)), columns = ['Date', 'Home',
                                                                               'HS', 'AS', 'Away',
                                                                               'B2BCODE', 'OTCODE'])

        if not data_fixtures2.empty:
            cont_teams_list.append(team)
            cont_teams_pds.append(data_fixtures2)
            local_teams[str(team+" "+premier_league_dict[league])] = data_fixtures2
        print("Done processing game data.")
    os.chdir(default)
# creating and changing to a directory for each league
if not os.path.exists("{year}{month}{day}".format(month = date_month_now_2, day = date_day_now, year = date_year_now[2:])):
    os.makedirs("{year}{month}{day}".format(month = date_month_now_2, day = date_day_now, year = date_year_now[2:]))
os.chdir("{year}{month}{day}".format(month = date_month_now_2, day = date_day_now, year = date_year_now[2:]))
statsFolder2 = os.getcwd()

lookback_games = 10.0
# first sheet entry
for team in teams_list[0:1]:
    team = replace_unicode(team)
    team = team.split(" ")[-1]
    os.chdir(statsFolder2)
    teams_fixtures = []
    teams_fixtures2 = []
    pd_results = pd.DataFrame(columns = ['Date', 'Home',
                                    'HS', 'AS', 'Away',
                                    'B2BCODE', 'OTCODE'])
    teams_fixtures2 += [val for key, val in local_teams.items() if team in key]
    joinery = pd.DataFrame(teams_fixtures2[0])
    if len(teams_fixtures2) > 1:
        joinery2 = pd.DataFrame(teams_fixtures2[1])
        df_merged = pd.concat([joinery,joinery2], ignore_index=True, sort=False)
    else:
        df_merged = pd.concat([joinery], ignore_index=True, sort=False)
        # pd_results.append(teams_fixtures2)
    final_pds = df_merged.sort_values(by=['Date'], ascending=True)
    pd_to_excel = final_pds.iloc[0-int(lookback_games):]
    # creating and changing to a directory for each league
    if not os.path.exists("LAST-SEVEN"):
        os.makedirs("LAST-SEVEN")
    os.chdir("LAST-SEVEN")
    resFolder = os.getcwd()
    # print(team)
    # print(resFolder)-
    team = team.upper()
    #pd_previous =  pd.read_excel("LAST-SEVEN.xlsx",sheet_name="{}".format(team), header=0)
    #df_merged1 = pd.concat([pd_to_excel, pd_previous.iloc[:7-int(lookback_games)]], ignore_index=True, sort=False)
    df_merged1 = pd.concat([pd_to_excel], ignore_index=True, sort=False)
    final_pds1 = df_merged1.sort_values(by=['Date'], ascending=True)
    for i in range(int(lookback_games)-1):
        delta_time = final_pds1['Date'].iloc[i+1] - final_pds1['Date'].iloc[i]
        if int(delta_time.days) > 1:
            final_pds1.at[i+1,"B2BCODE"] = int(0)
        else:
            final_pds1.at[i+1,"B2BCODE"] = int(1)
    #print(final_pds1)
    with pd.ExcelWriter("LAST-SEVEN.xlsx",engine='openpyxl',
                        mode='a',if_sheet_exists='overlay') as writer:
        try:
            final_pds1.to_excel(writer,sheet_name="{}".format(team), index=False, header=True)
        except ValueError:
            continue

# rest of hseet entries
for team in teams_list[1:]:
    team = replace_unicode(team)
    team = team.split(" ")[-1]
    os.chdir(statsFolder2)
    teams_fixtures = []
    teams_fixtures2 = []
    pd_results = pd.DataFrame(columns = ['Date', 'Home',
                                    'HS', 'AS', 'Away',
                                    'B2BCODE', 'OTCODE'])
    teams_fixtures2 += [val for key, val in local_teams.items() if team in key]
    joinery = pd.DataFrame(teams_fixtures2[0])
    if len(teams_fixtures2) > 1:
        joinery2 = pd.DataFrame(teams_fixtures2[1])
        df_merged = pd.concat([joinery,joinery2], ignore_index=True, sort=False)
    else:
        df_merged = pd.concat([joinery], ignore_index=True, sort=False)
        # pd_results.append(teams_fixtures2)
    final_pds = df_merged.sort_values(by=['Date'], ascending=True)
    pd_to_excel = final_pds.iloc[0-int(lookback_games):]
    # creating and changing to a directory for each league
    if not os.path.exists("LAST-SEVEN"):
        os.makedirs("LAST-SEVEN")
    os.chdir("LAST-SEVEN")
    resFolder = os.getcwd()
    # print(team)
    # print(resFolder)-
    team = team.upper()
    #pd_previous =  pd.read_excel("LAST-SEVEN.xlsx",sheet_name="{}".format(team), header=0)
    #df_merged1 = pd.concat([pd_to_excel, pd_previous.iloc[:7-int(lookback_games)]], ignore_index=True, sort=False)
    #construct fitst
    df_merged1 = pd.concat([pd_to_excel], ignore_index=True, sort=False)
    final_pds1 = df_merged1.sort_values(by=['Date'], ascending=True)
    for i in range(int(lookback_games)-1):
        delta_time = final_pds1['Date'].iloc[i+1] - final_pds1['Date'].iloc[i]
        if int(delta_time.days) > 1:
            final_pds1.at[i+1,"B2BCODE"] = int(0)
        else:
            final_pds1.at[i+1,"B2BCODE"] = int(1)
    #print(final_pds1)
    with pd.ExcelWriter("LAST-SEVEN.xlsx",engine='openpyxl',
                        mode='a',if_sheet_exists='overlay') as writer:
        try:
            final_pds1.to_excel(writer,sheet_name="{}".format(team), index=False, header=True)
        except ValueError:
            continue
os.chdir(default)
#os.chdir("{year}{month}{day}/FIXTURES".format(month = date_month_now_2, day = date_day_now, year = date_year_now[2:]))
#os.system("start EXCEL.EXE FIXTURES.xlsx")
#os.chdir(default)
#os.chdir("{year}{month}{day}".format(month = date_month_now_2, day = date_day_now, year = date_year_now[2:]))
#exec(open('excel-file-opener.py').read())
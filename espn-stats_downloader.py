" ------------------------------------------------------------ "
" start of code block to import all important libraries for use "

# to make, modify and change directories
import dt_prompter
import os
import glob
import shutil
import sys
from pathlib import Path

# important for making system commands
import sys
import platform

# library for opening url and creating requests
import urllib.request

# pretty-print python data structures
from pprint import pprint

# for parsing all the tables present on a website
from html_table_parser.parser import HTMLTableParser

# for converting the parsed data in a
# pandas dataframe
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

# date
import datetime as dt

# governing bs and html objects
from bs4 import BeautifulSoup

# graph plotter
import matplotlib.pyplot as plt

# array manipulation such as with matrices etc
import numpy as np

" end of code block to import all important libraries for use "
"-------------------------------------------------------------"

" line 42-53 code allows us to characterise which OS we are "
" runnning and other OS-related logic for this executable program "
OSListWin = ["Windows", "windows", "WINDOWS"] # list of acceptable windows OS names
OSListLin = ["Linux", "linux", "LINUX"] # list of acceptable linux OS names

promptOS = platform.system() # the system tells the program what OS it is

if promptOS not in OSListLin+OSListWin:
    print("No valid OS used")
    sys.exit()  # cut the execution if the OS we are using is not windows or linux

else:
    print("Operating system: "+promptOS)
    print("---Starting to process stats data---") # continue executing if correct OS

" set up of date and time "
date_prompt = dt_prompter.date_prompt2
date_now = dt.datetime.now() - dt.timedelta(days = date_prompt)
date_last = dt.datetime.now() - dt.timedelta(days = date_prompt)
date_year_now = date_now.strftime('%Y')
date_year_last = date_last.strftime('%Y')
date_day_now = date_now.strftime('%d')
date_day_last = date_last.strftime('%d')
date_month_now = date_now.strftime('%m')
date_month_last = date_last.strftime('%m')
print("--->Date of Interest: ",date_now)
format_date_now = "{yr}{mnth}{day}".format(yr=date_year_now[2:],mnth=date_month_now,day=date_day_now)
format_date_last = "{yr}{mnth}{day}".format(yr=date_year_last[2:],mnth=date_month_last,day=date_day_last)
root_bet_folder = Path(os.getcwd())
root_path = Path(root_bet_folder)
lastBetFolder = Path(str(root_path)+"\{}".format(str(format_date_last)))

if not os.path.exists("{betrootnow}".format(betrootnow = format_date_now)):
    os.makedirs("{betrootnow}".format(betrootnow = format_date_now))
os.chdir("{betrootnow}".format(betrootnow = format_date_now))
nowBetFolder = os.getcwd()
#print(nowBetFolder)

# print("---->Checking bet folder pre-requisites")
# if len(os.listdir(nowBetFolder)) == 0:
#     print("---->bet folder empty")
#     os.chdir(lastBetFolder)
#     src_files = os.listdir(lastBetFolder)
#     for file_name in src_files:
#         print(file_name)
#         full_file_name = os.path.join(lastBetFolder, file_name)
#         print(full_file_name)
#         if os.path.isfile(full_file_name):
#             shutil.copy(full_file_name, nowBetFolder)
#     os.chdir(nowBetFolder)
#     if len(os.listdir(nowBetFolder)) == 0:
#         print("---->bet folder still empty")
#     else:
#         print("---->copied base data successfully")
# else:
#     print("----<bet folder already populated")

" line 63 - 92 deal with sorting the league site data from basketballref or fbref etc "
" and then we also deal with each team in that league appropriately by collating all "
" important gross stats "
league_site_hook = ['https://www.espn.com/nba/standings'] # list of leagues

dataFilter = {"general-offense-factors": 3,
              "general-defense-factors": 3} # list of required datasets for the league

dataFiles = {"general-offense-factors": "RAWRECORDS",
              "general-defense-factors": "ROAD"} # list of required datasets for the league

# with open("teams-list.txt") as f:
#     empty = [] # empty so as to construct a list of teams in the program
#     for everyLine in f:
#         lineExtract = everyLine.strip() # extract each line in the teams list txt file
#         empty.append(lineExtract) # append each each line to the empty array
#         # if any("Line2" in iterate for iterate in empty):
#     selection = [everyLine for everyLine in empty] # finalise selection
# teams_list = selection # list of teams in the league

dataType = ["processed-data",
            "RAW",
            "league-raw-data",
            "player-raw-data"] # list of required datasets for each team

conferenceStats = ["eastern-conference", "western-conference"] # conference stats only
generalStats = ["general-offense-factors"] # raw gross stats
advancedStats = ["advanced-factors"] # advanced gross stats

default = os.getcwd() # the default directory is the league folder!

#driver_list = ['Brooklyn Nets']

# loop over all leagues
for league in league_site_hook:

    # extract league name
    if promptOS in OSListLin:
        my_folder = league.rsplit('/', 1)[-1]

    elif promptOS in OSListWin:
        my_folder = league.rsplit('/', 1)[-1]
        my_folder = my_folder[:-5]

    # creating and changing to a directory for each league

    if not os.path.exists("{statsroot}".format(statsroot = dataType[1])):
        os.makedirs("{statsroot}".format(statsroot = dataType[1]))
    os.chdir("{statsroot}".format(statsroot = dataType[1]))
    statsFolder = os.getcwd()
    print(statsFolder)

    # Opens a website and read its
    # binary contents (HTTP Response Body)
    def url_get_contents(url):

        # Opens a website and read its
        # binary contents (HTTP Response Body)

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

    # Now finally obtaining the data of
    # the table required
    #pprint(p.tables[1])itken

    table_captions = []

    # function to extract table captions
    def get_table_caption(url):

        # Opens a website and prints out table captions

        # making request to the website
        html = urllib.request.urlopen(url=url)
        bs = BeautifulSoup(html.read(), 'html.parser')

        # printing out the table captions
        captions = bs.find_all('caption')
        for caption in captions:
            table_captions.append(caption.get_text())
        return table_captions

    # get the captions
    get_caption = get_table_caption("{}".format(league))

    # Stats processing
    minutespg = []
    pacepg = []

    for eachType in generalStats:
        # Stats folder
        tableIndex = dataFilter[eachType]
        teamNames = pd.DataFrame(p.tables[0])
        dataOutput = pd.DataFrame(p.tables[1])
        teamNames1 = pd.DataFrame(p.tables[2])
        dataOutput1 = pd.DataFrame(p.tables[3])
        contentMarkers = dataOutput.iloc[:1, :]
        contentMarkers2 = dataOutput.iloc[-1:, :]
        contentDetail = dataOutput.iloc[1:-1,:]
        columnKeys = []
        dataOutputDriver = contentDetail.sort_values(1)
        dataOutputDriver = pd.concat([contentMarkers,dataOutputDriver,contentMarkers2])
        targetFileName = dataFiles[eachType]
        dataOutputDriver2 = pd.concat([teamNames, dataOutput], axis=1)
        dataOutputDriver3 = pd.concat([teamNames1, dataOutput1], axis=1)
        dataOutputDriver4 = dataOutputDriver3.iloc[1:,:]
        dataOutputDriver5 = pd.concat([dataOutputDriver2,dataOutputDriver4])
        #print(dataOutputDriver5)
        dataOutputDriver5.to_excel ("{file}.xlsx".format(file = targetFileName), index = False, header=False)

    # print(os.getcwd())
    os.chdir(statsFolder)

os.chdir(default)

print("---<Done processing stats data---")
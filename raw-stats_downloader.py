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

if sys.version_info[1] < 10:
    pass
else:
    import collections
    collections.Callable = collections.abc.Callable #python3.10+

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

here = os.getcwd()
all_dirs_here = os.walk(here)
here_dirs = [x[0] for x in all_dirs_here]

def retrieve_last_gameday(corrective_index, pattern='*', recursive=False):
    files = glob.glob(pattern, recursive=recursive)
    list_of_folder_names = []
    for file in files:
        strip_file = str(file)
        file_path = os.path.join(os.getcwd(),strip_file)
        if os.path.isdir(file_path):
            list_of_folder_names.append(file)
    list_of_folder_names = [x for x in list_of_folder_names if x != "__pycache__"]
    list_of_folder_names = [int(x) for x in list_of_folder_names if "DATA-VIS" not in x]
    list_of_folder_names = list(set(list_of_folder_names))
    list_of_folder_names.sort()
    last_game_day = str(list_of_folder_names[-1-corrective_index])
    return last_game_day

admissible_yes = ["y", "Y", "yes", "YEs", "YES", "yES", "yeS", "Yes", "YeS", "yEs"]
admissible_no = ["n", "N", "no", "No", "nO", "NO"]

empty_date_string = []
" set up of date and time "
" here we setup some codes for date and time"
nba_start_months = "10"
nba_end_months = "06"

#copy_type = str(input("Would you like to us the last bet gameday as a data-point reference: "))
copy_type = "y"
if copy_type in admissible_yes:
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
    format_date_last = "{last_gameday}".format(last_gameday=retrieve_last_gameday(corrective_index=0))
    empty_date_string.append(str(format_date_last))
    empty_date_string.append(str(format_date_now))
    root_path = os.getcwd()
    lastBetFolder = os.path.join(root_path,str(format_date_last))
    if not os.path.exists("{betrootnow}".format(betrootnow = format_date_now)):
        os.makedirs("{betrootnow}".format(betrootnow = format_date_now))
    os.chdir("{betrootnow}".format(betrootnow = format_date_now))
    nowBetFolder = os.getcwd()
    os.chdir(here)
    if str(nowBetFolder) == str(lastBetFolder):
        format_date_last = "{last_gameday}".format(last_gameday=retrieve_last_gameday(corrective_index=1))
        root_path = os.getcwd()
        lastBetFolder = os.path.join(root_path,str(format_date_last))
    print("now folder = ",nowBetFolder)
    print("last folder = ",lastBetFolder)
    os.chdir(nowBetFolder)

elif copy_type in admissible_no:
    date_prompt = int(input("How many days to yopur last bet-day: "))
    date_now = dt.datetime.now()
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
    empty_date_string.append(str(format_date_last))
    empty_date_string.append(str(format_date_now))
    root_path = os.getcwd()
    lastBetFolder = os.path.join(root_path,str(format_date_last))
    if not os.path.exists("{betrootnow}".format(betrootnow = format_date_now)):
        os.makedirs("{betrootnow}".format(betrootnow = format_date_now))
    os.chdir("{betrootnow}".format(betrootnow = format_date_now))
    nowBetFolder = os.getcwd()
    print("now folder = ",nowBetFolder)
    print("last folder = ",lastBetFolder)

else:
    print("Code crashed as you did not provide initial inputs: ")
    sys.exit()

print("---->Checking bet folder pre-requisites")

print(empty_date_string)

if len(os.listdir(nowBetFolder)) <= 9 or (len(os.listdir(nowBetFolder)) == 1 and "RAW" in os.listdir(nowBetFolder)):
    print("---->bet folder empty")
    os.chdir(lastBetFolder)
    #print(lastBetFolder)
    src_files = os.listdir(lastBetFolder)
    for file_name in src_files:
        print("----->copying file: "+file_name)
        full_file_name = os.path.join(lastBetFolder, file_name)
        dest_fold_name = os.path.join(nowBetFolder, file_name)
        while os.path.isfile(full_file_name):
            try:
                shutil.copy(full_file_name, nowBetFolder)
            except Exception as e:
                os.chdir(nowBetFolder)
                print("-----|{} trying to copy files from old bet folder".format(e))
                print("-----|restarting")
                continue
            break
        if "LAST-SEVEN" in full_file_name or "TEAMS-LIST" in full_file_name:
            shutil.copytree(full_file_name, dest_fold_name)
        while "-bball" in file_name:
            os.chdir(nowBetFolder)
            file_name_string = str(file_name)
            file_name_string = file_name_string.replace(str(empty_date_string[0]), str(empty_date_string[1]))
            new_file_name = os.path.join(nowBetFolder, file_name_string)
            os.rename(dest_fold_name, new_file_name)
            break
    os.chdir(nowBetFolder)
    if len(os.listdir(nowBetFolder)) == 0:
        print("---->bet folder still empty")
    else:
        print("----<copied base data successfully")

else:
    print("----<bet folder already populated")

" line 63 - 92 deal with sorting the league site data from basketballref or fbref etc "
" and then we also deal with each team in that league appropriately by collating all "
" important gross stats "
league_site_hook = ['https://www.basketball-reference.com/leagues/NBA_2025.html'] # list of leagues

dataFilter = {"general-offense-factors": 4,
              "general-defense-factors": 5,
              "advanced-factors": -3} # list of required datasets for the league

dataFiles = {"general-offense-factors": "RAWOFFENSE",
              "general-defense-factors": "RAWDEFENSE",
              "advanced-factors": "ADVANCED"} # list of required datasets for the league

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
generalStats = ["general-offense-factors", "general-defense-factors"] # raw gross stats
advancedStats = ["advanced-factors"] # advanced gross stats

default = os.getcwd() # the default directory is the league folder!

#driver_list = ['Brooklyn Nets']

# loop over all leagues
for league in league_site_hook:
    #print(league)

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
        dataOutput = pd.DataFrame(p.tables[tableIndex])
        contentMarkers = dataOutput.iloc[:1, :]
        contentMarkers2 = dataOutput.iloc[-1:, :]
        contentDetail = dataOutput.iloc[1:-1,:]
        columnKeys = []
        dataOutputDriver = contentDetail.sort_values(1)
        dataOutputDriver = pd.concat([contentMarkers,dataOutputDriver,contentMarkers2])
        targetFileName = dataFiles[eachType]
        dataOutputDriver.to_excel ("{file}.xlsx".format(file = targetFileName), index = False, header=False)

    # Advanced stats
    for eachType in advancedStats:
        tableIndex = dataFilter[eachType]
        dataOutput = pd.DataFrame(p.tables[tableIndex])
        contentMarkers = dataOutput.iloc[:2, :]
        contentMarkers2 = dataOutput.iloc[-1:, :]
        contentDetail = dataOutput.iloc[2:-1, :]
        columnKeys = []
        dataOutputDriver = contentDetail.sort_values(1)
        dataOutputDriver = pd.concat([contentMarkers,dataOutputDriver,contentMarkers2])
        targetFileName = dataFiles[eachType]
        dataOutputDriver.to_excel("{file}.xlsx".format(file = targetFileName), index = False, header=False)

    # print(os.getcwd())
    os.chdir(statsFolder)

os.chdir(here)

print("---<Done processing stats data---")
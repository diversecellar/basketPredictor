# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 21:27:15 2025

@author: Paul Namalomba
"""

import pandas as pd
import glob as gb
import seaborn as sns
import os
import numpy as np
import sys
import matplotlib.pyplot as plt
import shutil
import re

# data analysis suite for off rating, 3pt percentage and the other stats
#start_date = str(input("From which date do you want to visualise (YYMMDD format)?: "))
start_date = "241114"
files_to_analyse = ['NBADEFENSE.xlsx', 'NBAOFFENSE.xlsx', 'HOMEAWAY.xlsx']
parent_dir = os.getcwd()
# with open("column_headers.txt", "r") as file:
#     for line in file:
#         column_headers_ref = line
#teams_list_prompter = str(input("Do you want a custom teams list?: "))
teams_list_prompter = "N"
admissible_yes = ["y", "Y", "yes", "YEs", "YES", "yES", "yeS", "Yes", "YeS", "yEs"]
admissible_no = ["n", "N", "no", "No", "nO", "NO"]
if teams_list_prompter in admissible_yes:
    teams_list_ref = str(input("Input your teams list (each team separated by commas, only the team name and no city prefix): "))
    teams_list_ref = teams_list_ref.upper()
if teams_list_prompter in admissible_no:
    with open("teams_list_vis.txt", "r") as file2:
        for line in file2:
            teams_list_ref = line

# function defs for the explicit programming
def remove_brackets(str_name: str) -> str:
    # removing brackets
    while "[" in str_name:
        str_name = str_name.replace("[","")
    while "]" in str_name:
        str_name = str_name.replace("]","")
    return str_name
def remove_qoutes(str_name: str) -> str:
    # removing brackets
    while "'" in str_name:
        str_name = str_name.replace("'","")
    while "' " in str_name:
        str_name = str_name.replace("' ","")
    while " '" in str_name:
        str_name = str_name.replace(" '","")
    while " " in str_name:
        str_name = str_name.replace(" ","")
    while "\n" in str_name:
        str_name = str_name.replace("\n","")
    return str_name
def convert_str_to_list(str_name: str) -> list:
    # removing brackets
    str_name = remove_brackets(str_name)
    # splitting by commas
    list_of_strings = str_name.split(",")
    final_list = []
    for each_string in list_of_strings:
        constructor = remove_qoutes(each_string)
        final_list.append(constructor)
    return final_list
def is_float(element: any) -> bool:
    #If you expect None to be passed:
    if element is None:
        return False
    try:
        float(element)
        return True
    except ValueError:
        return False
def extract_dirs_in_dir(dir_name):
    print(os.getcwd())
    sub_folders_raw = os.listdir(dir_name)
    sub_folders = []
    for sub_folder in sub_folders_raw:
        if os.path.isdir(os.path.join(dir_name, sub_folder)):
            sub_folders.append(sub_folder)
    return sub_folders
def check_if_data_in_dir(dir_name, data_string_list) -> bool:
    sub_folders_raw = os.listdir(dir_name)
    for sub_folder in sub_folders_raw:
        for data_string in data_string_list:
            while str(data_string) in sub_folder:
                if os.path.isfile(os.path.join(dir_name, sub_folder)):
                    return True
                else:
                    return False
                break
def extract_data_relevant_dirs(dir_name):
    betday_folders_raw = extract_dirs_in_dir(dir_name)
    betday_folders = []
    for each_betday in betday_folders_raw:
        if is_float(each_betday):
            if float(str(each_betday)) >= float(start_date):
                betday_folders.append(each_betday)
    return betday_folders
def parse_list_of_lists(list_name):
    list_name_2 = []
    for each_entry in list_name:
        if isinstance(each_entry, list):
            list_name_2.append(each_entry[0])
        else:
            list_name_2.append(each_entry)
    cleaned_list = [x for x in list_name_2 if str(x) != 'nan']
    cleaned_list = [x.replace("'","") for x in cleaned_list]
    return cleaned_list
def extract_team_data_from_df(df_name, team_name):
    df2 = df_name[df_name['TEAM'] == team_name]
    return df2
def calc_essentials(dir_name, data_string_list):
    os.chdir(dir_name)
    data_dict = {}
    for data_string in data_string_list:
        key = data_string_list.index(data_string)
        df_data = pd.read_excel(data_string, index_col=None)
        df_data = df_data.iloc[:30,:27]
        df_data['PTS'] = pd.to_numeric(df_data['PTS'])
        df_data['FTA/FGA'] = df_data['FTA']/df_data['FGA']
        df_data['3PA/FGA'] = df_data['3PA']/df_data['FGA']
        df_data['2PA/FGA'] = df_data['2PA']/df_data['FGA']
        df_data['FGMsd'] = df_data['FGA'] - df_data['FG']
        df_data['SH.EFF'] = (df_data['3P%']*df_data['3PA/FGA']*3.0 \
                            + df_data['2P%']*df_data['2PA/FGA']*2.0) \
                            + (df_data['FT%']*df_data['FTA/FGA'] \
                            + ((df_data['AST'] - df_data['TOV'])/df_data['FGA'])
                            + 0.125*(1.0 - (df_data['BLK']/(df_data['FGMsd'])))
                            + (df_data['ORB']/df_data['FGMsd']))
        df_data['POS.NORM'] = df_data['Pace']/100.0
        df_data = df_data.sort_values(by=['TEAM'])
        df_data.reset_index(drop=True, inplace=True)
        df_hw = pd.read_excel('HOMEAWAY.xlsx', index_col=None)
        df_hw = df_hw.iloc[:30,:]
        df_hw = df_hw.sort_values(by=['TEAM'])
        df_hw.reset_index(drop=True, inplace=True)
        df_data['W'] = df_hw['W']
        df_data['W%'] = df_data['W']/df_data['G']
        df_data['DIFF'] = df_hw['DIFF']
        df_correl_w_pace = df_data['W%'].corr(df_data['POS.NORM'], method='pearson')
        df_data["REL.EFF"] = (1 + (df_data['POS.NORM'] - 1)*df_correl_w_pace)/df_data['SH.EFF']
        df_correl_w_releff = df_data['W%'].corr(df_data['REL.EFF'], method='pearson')
        df_data["CORR.REL.EFF"] = abs(df_correl_w_releff)
        data_dict[key] = df_data
    os.chdir(parent_dir)
    return data_dict

teams_list = convert_str_to_list(teams_list_ref)
regex_string = '^[0-9]{1,6}$'
regex_compile = re.compile(regex_string)
list_of_folders_in_dir = extract_dirs_in_dir(os.getcwd())
list_of_betdays = []
for folder in list_of_folders_in_dir:
    if regex_compile.match(folder):
        if int(folder) >= int(start_date):
            if check_if_data_in_dir(folder, files_to_analyse):
                list_of_betdays.append(regex_compile.match(folder).group())
list_of_betdays = list(set(list_of_betdays))
list_of_betdays.sort()
team_dict = {}
for team in teams_list:
    list_of_analysed_team_dfs = []
    for betday in list_of_betdays:
        final_data = calc_essentials(betday, files_to_analyse[:2])
        df_offdeff = pd.DataFrame()
        df_offdeff['TEAM'] = final_data[0]['TEAM']
        df_offdeff['G'] = final_data[0]['G']
        df_offdeff['REL.EFF-DEF'] = final_data[0]['REL.EFF']
        df_offdeff['CORREL1'] = abs(final_data[1]['CORR.REL.EFF'])/2 + abs(final_data[0]['CORR.REL.EFF'])/2
        df_offdeff['REL.EFF-OFF'] = final_data[1]['REL.EFF']
        df_offdeff['CORREL2'] = df_offdeff['REL.EFF-OFF'].corr(df_offdeff['REL.EFF-DEF'], method='pearson')
        df_offdeff['CORREL3'] = 1 - (df_offdeff['CORREL1'] - df_offdeff['CORREL2'])
        df_offdeff['REL.EFF-DIFF'] = (df_offdeff['REL.EFF-OFF']/df_offdeff['REL.EFF-DEF']) - 1
        df_offdeff['W%'] = final_data[0]['W%']
        columns_analysed_team_dfs = df_offdeff.columns.tolist()
        df_team_analysed = df_offdeff[df_offdeff['TEAM'] == team].values[0].tolist()
        list_of_analysed_team_dfs.append(df_team_analysed)
    df_analysed_team_data = pd.DataFrame(list_of_analysed_team_dfs, columns=columns_analysed_team_dfs)
    df_analysed_team_data = df_analysed_team_data.drop_duplicates(subset=['G'],keep='first')
    red_list = df_analysed_team_data['REL.EFF-DIFF'].values.tolist()
    game_list = df_analysed_team_data['G'].values.tolist()
    red_delta_list = [0]
    for idx in range(len(red_list)-1):
        game_delta = game_list[idx+1] - game_list[idx]
        red_delta = red_list[idx+1] - red_list[idx]
        red_per_game = red_delta/game_delta
        red_per_game_delta = red_per_game*100.0
        red_delta_list.append(red_per_game_delta)
    #df_analysed_team_data['R.E-DIFF.DELTA'] = red_delta_list
    df_analysed_team_data['R.E-DIFF.DELTA'] = 100.0 * df_analysed_team_data['REL.EFF-DIFF']
    fig, ax = plt.subplots(figsize=(10, 7), dpi=100)
    sns.set_theme(style="white", font_scale=1)
    sns.lineplot(x='G',y='R.E-DIFF.DELTA',data=df_analysed_team_data,\
                 marker='*', markerfacecolor='limegreen', markersize=10, ax=ax).set(title='{} [delta] relative effeciency difference - a time-series'.format(team),\
                                                                          xlabel='games played (G)', ylabel='values in %')
    ax.set_xlim(left=10.0, right=65.0)
    ax.set_ylim(bottom=-15.0, top=15.0)
    ax.yaxis.grid(True)
    ax.xaxis.grid(True)
    line = ax.get_lines()[0]
    x, y = line.get_data()
    mask = y != 0
    x, y = x[mask], y[mask]
    ax.fill_between(x, y1=y, alpha=0.5, facecolor='green')
    if not os.path.exists("DATA-VIS-V2"):
        os.makedirs("DATA-VIS-V2")
    os.chdir("DATA-VIS-V2")
    print("saving timeseries datanalysis for", team)
    plt.savefig("{}_REL.EFF-DIFF.png".format(team))
    plt.close()
    #plt.show()
    os.chdir(parent_dir)
    #team_dict[team] = df_team



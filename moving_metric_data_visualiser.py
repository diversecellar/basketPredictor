# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 08:37:36 2025

@author: Paul Namalomba
"""
import pandas as pd
import glob as gb
import os
import numpy as np
import sys
import matplotlib.pyplot as plt
import shutil

# data analysis suite for off rating, 3pt percentage and the other stats
#start_date = str(input("From which date do you want to visualise (YYMMDD format)?: "))
start_date = "241114"
files_to_analyse = ['NBADEFENSE.xlsx', 'NBAOFFENSE.xlsx']
parent_dir = os.getcwd()
with open("column_headers.txt", "r") as file:
    for line in file:
        column_headers_ref = line
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
    sub_folders_raw = os.listdir(dir_name)
    sub_folders = []
    for sub_folder in sub_folders_raw:
        if os.path.isdir(os.path.join(dir_name, sub_folder)):
            sub_folders.append(sub_folder)
    return sub_folders

def check_if_data_in_dir(dir_name, data_string) -> bool:
    sub_folders_raw = os.listdir(dir_name)
    for sub_folder in sub_folders_raw:
        while str(data_string) in sub_folder:
            if os.path.isfile(os.path.join(dir_name, sub_folder)):
                return True
            else:
                return False
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
    df2 = df[df['TEAM'] == each_team]
    return df2

# start of implicit programming
teams_list = convert_str_to_list(teams_list_ref)
column_headers = convert_str_to_list(column_headers_ref)
betday_folders = extract_data_relevant_dirs(parent_dir)
data_superheaders = betday_folders
list_of_offense_dfs = {}
list_of_defense_dfs = {}
true_betdays = []
for each_team in teams_list:
    print("--------------------------------")
    print("PROCESSING DFS FOR TEAM: ", each_team)
    team_offense_data_df_list = []
    team_defense_data_df_list = []
    for each_folder in betday_folders:
        each_folder_path = os.path.join(parent_dir, each_folder)
        offense_check_bool = check_if_data_in_dir(each_folder_path, "NBAOFFENSE")
        defense_check_bool = check_if_data_in_dir(each_folder_path, "NBADEFENSE")
        os.chdir(each_folder_path)
        while offense_check_bool and defense_check_bool:
            print("---|processing folder:", each_folder)
            while each_team == teams_list[0]:
                true_betdays.append(each_folder)
                break
            for each_file in files_to_analyse:
                each_file_path = os.path.join(each_folder_path, each_file)
                df = pd.read_excel(each_file)
                column_headers = column_headers_ref
                drop_candidates = ['RGRFAC']
                data_df = df.drop([x for x in drop_candidates if x in df.columns], axis=1)
                df_teams = data_df.iloc[:, 2:3].values.tolist()
                df_teams = parse_list_of_lists(df_teams)
                gandalf = data_df
                if 'OFFENSE' in each_file:
                    print("---|parsing dataframe data for:", each_team, "from", each_file)
                    team_offense_data_df_list.append(extract_team_data_from_df(gandalf, each_team))
                if 'DEFENSE' in each_file:
                    print("---|parsing dataframe data for:", each_team, "from", each_file)
                    team_defense_data_df_list.append(extract_team_data_from_df(gandalf, each_team))
            break
    print("DONE PROCESSING DFS FOR TEAM:", each_team)
    print("--------------------------------")
    #true_betdays.sort()
    list_of_offense_dfs['{}'.format(each_team)] = team_offense_data_df_list
    list_of_defense_dfs['{}'.format(each_team)] = team_defense_data_df_list

metric_names = {"0":"SHEFF","2":"PTS","3":"PACE","4":"RTNG",
                "5":"SHEFF%CHNG","6":"PTS%CHNG","7":"GP",
                "8":"RELEFF","9":"RELEFF%CHNG"}
metric_names2 = {"0","2","5","6","8","9"}
metric_names3 = {"5","6","9"}

#DATa_VISUALIZER
def data_visualiser_app(team_dfs, team_name):
    df_lists = team_dfs[team_name]
    df_raw_data_list = []
    for each_df in df_lists:
        each_df_to_list = each_df.iloc[0:1,:].values.tolist()
        df_raw_data_list.append(each_df_to_list[0])
    progressor_list = []
    progressor_int = 0
    ptsscl_list = []
    rtng_list = []
    pace_list = []
    pts_list = []
    sheff_pct_list = []
    releff_pct_list = []
    gp_list = []
    plt_data_dict = {}
    for each_df in df_raw_data_list:
        progressor_int += 1
        progressor_list.append(progressor_int)
        #print(each_df)
        ptsscl = float(each_df[32])
        sheff_pct = float(each_df[27])
        rtng = 100.0*float(each_df[25])/float(each_df[26])
        pts = float(each_df[25])
        pace = float(each_df[26])
        gp = int(each_df[3])
        # 32/(27*26/100)
        releff_pct = float(each_df[32]/(float(each_df[27])*float(each_df[26])/100.0))
        ptsscl_list.append(np.round(ptsscl,4))
        rtng_list.append(np.round(rtng,2))
        pts_list.append(np.round(pts,2))
        pace_list.append(np.round(pace,2))
        sheff_pct_list.append(np.round(sheff_pct,4))
        releff_pct_list.append(np.round(releff_pct,4))
        gp_list.append(gp)
    plt_data_dict["0"] = sheff_pct_list
    # plt_data_dict["1"] = ptsscl_list
    plt_data_dict["2"] = pts_list
    plt_data_dict["3"] = pace_list
    plt_data_dict["4"] = rtng_list
    releff_pct_change_list = [0.0]
    sheff_pct_change_list = [0.0]
    pts_pct_change_list = [0.0]
    for idx in range(len(sheff_pct_list)-1):
        sheff_pct_change = ((sheff_pct_list[idx+1]/sheff_pct_list[idx]) - 1.0)*100
        releff_pct_change = ((releff_pct_list[idx+1]/releff_pct_list[idx]) - 1.0)*100
        pts_pct_change = ((pts_list[idx+1]/pts_list[idx]) - 1.0)*100
        sheff_pct_change_list.append(sheff_pct_change)
        releff_pct_change_list.append(releff_pct_change)
        pts_pct_change_list.append(pts_pct_change)
    plt_data_dict["5"] = sheff_pct_change_list
    plt_data_dict["6"] = pts_pct_change_list
    plt_data_dict["7"] = gp_list
    plt_data_dict["8"] = releff_pct_list
    plt_data_dict["9"] = releff_pct_change_list
    return plt_data_dict

def plotter(plt_data: dict, plt_names: dict, ball_side: str, team_name):
    # Define X and Y variable data
    for key in plt_data.keys():
        plt_data_list = plt_data[key]
        plt.plot(true_betdays, plt_data_list, linestyle='--', marker='o', color='b')
        print("---|plotting {}:".format(ball_side), plt_names[key])
        plt.xlabel("Dates (YYMMDD)")  # add X-axis label
        plt.ylabel("{} Metric".format(plt_names[key]))  # add Y-axis label
        plt.title("{c} {a}: {b} - A Time-Series".format(a=ball_side,
                                                        b=plt_names[key],
                                                        c=team_name))  # add title
        plt.xticks(rotation=90)
        plt.subplots_adjust(bottom=0.20)
        plt_y_min = np.min(plt_data_list)
        plt_y_max = np.max(plt_data_list)
        ax = plt.gca()
        if plt_y_min > 0.0:
            ax.set(ylim=(0.99*plt_y_min,1.01*plt_y_max))
        if plt_y_min < 0.0:
            ax.set(ylim=(1.51*plt_y_min,1.49*plt_y_max))
        ax.figure.set_dpi(150)
        plt.grid()
        plt.savefig("{c}_{a}_{b}.png".format(a=ball_side,
                                             b=plt_names[key],
                                             c=team_name))
        plt.show()

def plotter2(plt_data: dict, plt_names: dict, plt_data2: dict, team_name):
    # Define X and Y variable
    for key in plt_data.keys():
        while key in metric_names2:
            plt_data_list = plt_data[key]
            plt_data2_list = plt_data2[key]
            plt_actual_list = []
            magic_list = []
            gp_list = plt_data2["7"]
            print(gp_list)
            while len(plt_data_list) == len(plt_data2_list):
                for each_idx in range(len(plt_data_list)):
                    if int(key) not in [int(5), int(6), int(9)]:
                        differential = 100.0*(plt_data_list[each_idx] - plt_data2_list[each_idx])/plt_data2_list[each_idx]
                    else:
                        differential = (plt_data_list[each_idx] - plt_data2_list[each_idx])
                    magic_list.append(gp_list[each_idx])
                    plt_actual_list.append(differential)
                break
            magic_length = magic_list[-1]
            theory = 82
            scaler = magic_length * 14 / theory
            plt.figure(figsize=(scaler, 5))
            intervals = [1.0/len(true_betdays),]
            for i in range(len(true_betdays)):
                while i < len(true_betdays)-1:
                    bet_changes = (int(true_betdays[i+1])-int(true_betdays[i]))/len(true_betdays)
                    intervals.append(bet_changes)
                    break
            print(intervals)
            # if key in metric_names3:
            #     plt_agg_list = [float(p)/float(i) for p,i in zip(plt_actual_list, int)]
            plt.plot(true_betdays, plt_actual_list, linestyle='--', marker='o', color='b')
            print("---|plotting OFF-DEF Deltas:", plt_names[key])
            plt.xlabel("Dates (YYMMDD)")  # add X-axis label
            plt.ylabel("Delta% {} Metric".format(plt_names[key]))  # add Y-axis label
            plt.title("OFF-DEF Delta% {c}: {b} - A Time-Series".format(b=plt_names[key],
                                                            c=team_name))  # add title
            plt.xticks(rotation=90)
            plt.subplots_adjust(bottom=0.20)
            plt_y_min = np.min(plt_actual_list)
            plt_y_max = np.max(plt_actual_list)
            ax = plt.gca()
            if plt_y_min >= 0.0 and plt_y_max >= 0.0:
                ax.set(ylim=(0.85*plt_y_min,1.15*plt_y_max))
            elif plt_y_min <= 0.0 and plt_y_max >= 0.0:
                ax.set(ylim=(1.51*plt_y_min,1.49*plt_y_max))
            elif plt_y_min < 0.0 and plt_y_max <= 0.0:
                ax.set(ylim=(1.51*plt_y_min,0.0*plt_y_max))
            ax.figure.set_dpi(150)
            plt.grid()
            plt.savefig("{a}_OFF-DEF_Delta_{b}.png".format(a=team_name,
                                                           b=plt_names[key]))
            plt.show()
            break

for each_team in teams_list:
    print("--------------------------------")
    print("PLOTTING DATA FOR TEAM:", each_team)
    os.chdir(parent_dir)
    today_betday = os.path.join(parent_dir, true_betdays[-1])
    os.chdir(today_betday)
    if not os.path.exists("DATA-VIS/{a}".format(a = each_team)):
        os.makedirs("DATA-VIS/{a}".format(a = each_team))
    else:
        os.chdir(os.path.join(today_betday,"DATA-VIS/{a}".format(a = each_team)))
        for files in gb.glob("**/*.png", recursive=True):
            os.remove(files)
            print("removing existing PNGs")
        os.chdir(today_betday)
    print("writing new PNGs")
    os.chdir("DATA-VIS/{a}".format(a = each_team))
    team_data_dict = data_visualiser_app(list_of_defense_dfs, each_team)
    # plotter(team_data_dict, metric_names, "DEFENSE", each_team)
    team_data_dict2 = data_visualiser_app(list_of_offense_dfs, each_team)
    # plotter(team_data_dict2, metric_names, "OFFENSE", each_team)
    plotter2(team_data_dict2, metric_names, team_data_dict, each_team)
    print("DONE PLOTTING TEAM:", each_team)
    print("--------------------------------")
    os.chdir(parent_dir)


            # if 'OFFENSE' in each_file:
            #     dothat=0




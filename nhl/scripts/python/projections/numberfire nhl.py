import time
import os

import pandas as pd
import requests
import numpy as np

from bs4 import BeautifulSoup

from datetime import date, timedelta

from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# working directory
wd = 'c:/dev/Python/Repos/dfs-model/nhl/data/'

# load env vars
load_dotenv()

# login credentials
nf_username = os.getenv('NF_USERNAME')
nf_password = os.getenv('NF_PASSWORD')

# path to webdriver exe
chromedriver = (
    'C:/dev/Web Drivers/chromedriver_win32/chromedriver.exe')

# configure options
options = webdriver.ChromeOptions()

prefs = {'download.default_directory': 'c:\dev\Python\Repos\dfs-model\\nhl\data\\',
         'download.prompt_for_download': False,
         'download.directory_upgrade': True, }

options.add_experimental_option('prefs', prefs)

# load browser
driver = webdriver.Chrome(chromedriver, options=options)

# navigate to login page
driver.get('https://www.numberfire.com/account/login-google-plus')

time.sleep(5)

# log in
username = driver.find_element_by_xpath(
    '//*[@id="identifierId"]')
username.send_keys(nf_username)

next_button = driver.find_element_by_xpath(
    '//*[@id="identifierNext"]/span/span')
next_button.click()

time.sleep(2)

password = driver.find_element_by_xpath(
    '//*[@id="password"]/div[1]/div/div[1]/input')
password.send_keys(nf_password)

next_button = driver.find_element_by_xpath(
    '//*[@id="passwordNext"]/span/span')
next_button.click()

time.sleep(5)

# navigate to fanduel skater projections page
driver.get('https://www.numberfire.com/nhl/daily-fantasy/set-dfs-site?site=3')

time.sleep(2)

driver.get(
    'https://www.numberfire.com/nhl/daily-fantasy/daily-hockey-projections/skaters')

# scrape slate IDs
slate_list_dropdown = driver.find_element_by_xpath(
    '/html/body/main/div[2]/div[2]/div/div[2]/div[3]/div/span')
slate_list_dropdown.click()

slate_list_ul = driver.find_element_by_xpath(
    '/html/body/main/div[2]/div[2]/div/div[2]/div[3]/div/ul')
slate_list_li = slate_list_ul.find_elements_by_tag_name('li')

slate_list = []
for li in slate_list_li:
    if '@' in li.text:
        print('single game slate, skipping')
    elif '3-Man Challenge' in li.text:
        print('3 man challenge slate, skipping')
    else:
        slate_list.append(li.get_attribute('data-value'))

time.sleep(2)

num_slates = len(slate_list)

nf_df_dict = {}
for slate in slate_list:
    nf_df_dict[slate] = pd.DataFrame()

time.sleep(2)


# function to scrape data
def scrapeData(dictionary, soup, index):
    return soup.find_all(
        dictionary[list(dictionary.keys())[index]][0][list(
            list(dictionary[list(dictionary.keys())[index]])[0])[0]], class_=dictionary[list(dictionary.keys())[index]][1][list(
                list(dictionary[list(dictionary.keys())[index]])[1])[0]])


# function to get contents of elements
def getContents(dictionary, index):
    soup = dictionary[list(dictionary.keys())[index]][0][list(
        list(dictionary[list(dictionary.keys())[index]])[0])[0]]
    final = dictionary[list(dictionary.keys())[index]][1][list(
        list(dictionary[list(dictionary.keys())[index]])[1])[0]]
    for x in soup:
        final.append(x.contents)
    return final


# function to populate dataframe columns with data
def populateColumn(columnName, data):
    temp_df = pd.DataFrame()
    temp_df[columnName] = data
    temp_df[columnName] = temp_df[columnName].astype(str)
    temp_df[columnName] = temp_df[columnName].apply(lambda x: x.replace('\\t', '').replace(
        '\\n', '').replace('\'', '').replace('[', '').replace(']', '').strip())
    return temp_df[columnName]


# function to create data frame
def createDataFrame(slate_id):
    # navigate to slate page by ID
    driver.get(
        'https://www.numberfire.com/nhl/daily-fantasy/set-slate?slate_id=' + slate_id)

    time.sleep(2)

    # navigate to skater projection page
    driver.get(
        'https://www.numberfire.com/nhl/daily-fantasy/daily-hockey-projections/skaters')
    skaters_url = driver.page_source

    time.sleep(2)

    # initial stat lists
    skater_names = []
    skater_positions = []
    skater_teams = []
    skater_opponents = []
    skater_projections = []
    skater_salaries = []
    skater_values = []
    skater_shots = []
    skater_goals = []
    skater_assists = []
    skater_points = []
    skater_ppg = []
    skater_ppa = []
    skater_plusminus = []
    skater_blocks = []
    skater_mins = []
    skater_pim = []

    # parse page
    skater_soup = BeautifulSoup(skaters_url, 'lxml')
    skater_table = skater_soup.find(
        'tbody', class_='stat-table__body')

    # web element dictionary
    skater_html_dict = {
        'skater_names': [
            {'tag': 'a'},
            {'class': 'full'},
        ],
        'skater_positions': [
            {'tag': 'span'},
            {'class': 'player-info--position'},
        ],
        'skater_teams': [
            {'tag': 'span'},
            {'class': 'team-player__team active'},
        ],
        'skater_opponents': [
            {'tag': 'span'},
            {'class': 'team-player__team'},
        ],
        'skater_projections': [
            {'tag': 'td'},
            {'class': 'fp active'},
        ],
        'skater_salaries': [
            {'tag': 'td'},
            {'class': 'cost'},
        ],
        'skater_values': [
            {'tag': 'td'},
            {'class': 'value'},
        ],
        'skater_shots': [
            {'tag': 'td'},
            {'class': 's'},
        ],
        'skater_goals': [
            {'tag': 'td'},
            {'class': 'g'},
        ],
        'skater_assists': [
            {'tag': 'td'},
            {'class': 'ast'},
        ],
        'skater_points': [
            {'tag': 'td'},
            {'class': 'points'},
        ],
        'skater_ppg': [
            {'tag': 'td'},
            {'class': 'ppg'},
        ],
        'skater_ppa': [
            {'tag': 'td'},
            {'class': 'ppa'},
        ],
        'skater_plusminus': [
            {'tag': 'td'},
            {'class': 'plus_minus'},
        ],
        'skater_blocks': [
            {'tag': 'td'},
            {'class': 'blk'},
        ],
        'skater_mins': [
            {'tag': 'td'},
            {'class': 'min'},
        ],
        'skater_pim': [
            {'tag': 'td'},
            {'class': 'pim'},
        ],
    }

    # populate lists
    for i in range(0, len(skater_html_dict)):
        if i == 0:
            skater_names = scrapeData(skater_html_dict, skater_table, i)
        if i == 1:
            skater_positions = scrapeData(skater_html_dict, skater_table, i)
        if i == 2:
            skater_teams = scrapeData(skater_html_dict, skater_table, i)
        if i == 3:
            skater_opponents = scrapeData(skater_html_dict, skater_table, i)
        if i == 4:
            skater_projections = scrapeData(skater_html_dict, skater_table, i)
        if i == 5:
            skater_salaries = scrapeData(skater_html_dict, skater_table, i)
        if i == 6:
            skater_values = scrapeData(skater_html_dict, skater_table, i)
        if i == 7:
            skater_shots = scrapeData(skater_html_dict, skater_table, i)
        if i == 8:
            skater_goals = scrapeData(skater_html_dict, skater_table, i)
        if i == 9:
            skater_assists = scrapeData(skater_html_dict, skater_table, i)
        if i == 10:
            skater_points = scrapeData(skater_html_dict, skater_table, i)
        if i == 11:
            skater_ppg = scrapeData(skater_html_dict, skater_table, i)
        if i == 12:
            skater_ppa = scrapeData(skater_html_dict, skater_table, i)
        if i == 13:
            skater_plusminus = scrapeData(skater_html_dict, skater_table, i)
        if i == 14:
            skater_blocks = scrapeData(skater_html_dict, skater_table, i)
        if i == 15:
            skater_mins = scrapeData(skater_html_dict, skater_table, i)
        if i == 16:
            skater_pim = scrapeData(skater_html_dict, skater_table, i)

    # final stat lists
    skater_names_final = []
    skater_positions_final = []
    skater_teams_final = []
    skater_opponents_final = []
    skater_projections_final = []
    skater_salaries_final = []
    skater_values_final = []
    skater_shots_final = []
    skater_goals_final = []
    skater_assists_final = []
    skater_points_final = []
    skater_ppg_final = []
    skater_ppa_final = []
    skater_plusminus_final = []
    skater_blocks_final = []
    skater_mins_final = []
    skater_pim_final = []

    # map initial lists to final lists
    skater_contents_dict = {
        'skater_names': [
            {'soup': skater_names},
            {'final': skater_names_final},
        ],
        'skater_positions': [
            {'soup': skater_positions},
            {'final': skater_positions_final},
        ],
        'skater_teams': [
            {'soup': skater_teams},
            {'final': skater_teams_final},
        ],
        'skater_opponents': [
            {'soup': skater_opponents},
            {'final': skater_opponents_final},
        ],
        'skater_projections': [
            {'soup': skater_projections},
            {'final': skater_projections_final},
        ],
        'skater_salaries': [
            {'soup': skater_salaries},
            {'final': skater_salaries_final},
        ],
        'skater_values': [
            {'soup': skater_values},
            {'final': skater_values_final},
        ],
        'skater_shots': [
            {'soup': skater_shots},
            {'final': skater_shots_final},
        ],
        'skater_goals': [
            {'soup': skater_goals},
            {'final': skater_goals_final},
        ],
        'skater_assists': [
            {'soup': skater_assists},
            {'final': skater_assists_final},
        ],
        'skater_points': [
            {'soup': skater_points},
            {'final': skater_points_final},
        ],
        'skater_ppg': [
            {'soup': skater_ppg},
            {'final': skater_ppg_final},
        ],
        'skater_ppa': [
            {'soup': skater_ppa},
            {'final': skater_ppa_final},
        ],
        'skater_plusminus': [
            {'soup': skater_plusminus},
            {'final': skater_plusminus_final},
        ],
        'skater_blocks': [
            {'soup': skater_blocks},
            {'final': skater_blocks_final},
        ],
        'skater_mins': [
            {'soup': skater_mins},
            {'final': skater_mins_final},
        ],
        'skater_pim': [
            {'soup': skater_pim},
            {'final': skater_pim_final},
        ],
    }

    # get contents
    for i in range(0, len(skater_contents_dict)):
        if i == 0:
            skater_names_final = getContents(skater_contents_dict, i)
        if i == 1:
            skater_positions_final = getContents(skater_contents_dict, i)
        if i == 2:
            skater_teams_final = getContents(skater_contents_dict, i)
        if i == 3:
            skater_opponents_final = getContents(skater_contents_dict, i)
        if i == 4:
            skater_projections_final = getContents(skater_contents_dict, i)
        if i == 5:
            skater_salaries_final = getContents(skater_contents_dict, i)
        if i == 6:
            skater_values_final = getContents(skater_contents_dict, i)
        if i == 7:
            skater_shots_final = getContents(skater_contents_dict, i)
        if i == 8:
            skater_goals_final = getContents(skater_contents_dict, i)
        if i == 9:
            skater_assists_final = getContents(skater_contents_dict, i)
        if i == 10:
            skater_points_final = getContents(skater_contents_dict, i)
        if i == 11:
            skater_ppg_final = getContents(skater_contents_dict, i)
        if i == 12:
            skater_ppa_final = getContents(skater_contents_dict, i)
        if i == 13:
            skater_plusminus_final = getContents(skater_contents_dict, i)
        if i == 14:
            skater_blocks_final = getContents(skater_contents_dict, i)
        if i == 15:
            skater_mins_final = getContents(skater_contents_dict, i)
        if i == 16:
            skater_pim_final = getContents(skater_contents_dict, i)

    # clean up data
    skater_teams_final_temp = pd.DataFrame(skater_teams_final)
    try:
        skater_teams_final_temp[0] = skater_teams_final_temp[0].astype(str)
        skater_teams_final_temp[0] = skater_teams_final_temp[0].apply(lambda x: x.replace('\\t', '').replace(
            '\\n', '').replace('\'', '').replace('[', '').replace(']', '').strip())
        # print(skater_teams_final_temp)
    except:
        print('skater team names list is empty, skipping')

    skater_opponents_final_temp = pd.DataFrame(skater_opponents_final)
    try:
        skater_opponents_final_temp[0] = skater_opponents_final_temp[0].astype(
            str)
        skater_opponents_final_temp[0] = skater_opponents_final_temp[0].apply(lambda x: x.replace('\\t', '').replace(
            '\\n', '').replace('\'', '').replace('[', '').replace(']', '').strip())
        # print(skater_opponents_final_temp)
    except:
        print('skater opponent names list is empty, skipping')

    skater_opponents_final_temp2 = pd.DataFrame(
        [np.nan] * len(skater_teams_final_temp)).fillna('')

    for i in range(0, len(skater_teams_final_temp)):
        index = (i + 1) * 2
        index1 = index - 2
        index2 = index - 1
        if skater_teams_final_temp[0][i] == skater_opponents_final_temp[0][index1]:
            skater_opponents_final_temp2[0][i] = skater_opponents_final_temp[0][index2]
        else:
            skater_opponents_final_temp2[0][i] = skater_opponents_final_temp[0][index1]

    skater_opponents_final = skater_opponents_final_temp2.values.tolist()

    # make final data frame
    skater_df = pd.DataFrame()

    skater_df['Name'] = populateColumn('Name', skater_names_final)
    skater_df['Position'] = populateColumn('Position', skater_positions_final)
    skater_df['Team'] = populateColumn('Team', skater_teams_final)
    skater_df['Opponent'] = populateColumn('Opponent', skater_opponents_final)
    skater_df['Projection'] = populateColumn(
        'Projection', skater_projections_final)
    skater_df['Salary'] = populateColumn('Salary', skater_salaries_final)
    skater_df['Value'] = populateColumn('Value', skater_values_final)
    skater_df['Shots'] = populateColumn('Shots', skater_shots_final)
    skater_df['Goals'] = populateColumn('Goals', skater_goals_final)
    skater_df['Assists'] = populateColumn('Assists', skater_assists_final)
    skater_df['Points'] = populateColumn('Points', skater_points_final)
    skater_df['PPG'] = populateColumn('PPG', skater_ppg_final)
    skater_df['PPA'] = populateColumn('PPA', skater_ppa_final)
    skater_df['+/-'] = populateColumn('+/-', skater_plusminus_final)
    skater_df['Blocks'] = populateColumn('Blocks', skater_blocks_final)
    skater_df['Minutes'] = populateColumn('Minutes', skater_mins_final)
    skater_df['PIM'] = populateColumn('PIM', skater_pim_final)

    time.sleep(2)

    # navigate to goalie projection page
    driver.get(
        'https://www.numberfire.com/nhl/daily-fantasy/daily-hockey-projections/goalies')
    goalie_url = driver.page_source

    time.sleep(2)

    # initial stat lists
    goalie_names = []
    goalie_teams = []
    goalie_opponents = []
    goalie_projections = []
    goalie_salaries = []
    goalie_values = []
    goalie_goals_against = []
    goalie_save_attempts = []
    goalie_saves = []
    goalie_shutouts = []
    goalie_wins = []
    goalie_mins = []

    # parse page
    goalie_soup = BeautifulSoup(goalie_url, 'lxml')
    goalie_table = goalie_soup.find(
        'tbody', class_='stat-table__body')

    # web element dictionary
    goalie_html_dict = {
        'goalie_names': [
            {'tag': 'a'},
            {'class': 'full'},
        ],
        'goalie_teams': [
            {'tag': 'span'},
            {'class': 'team-player__team active'},
        ],
        'goalie_opponents': [
            {'tag': 'span'},
            {'class': 'team-player__team'},
        ],
        'goalie_projections': [
            {'tag': 'td'},
            {'class': 'fp active'},
        ],
        'goalie_salaries': [
            {'tag': 'td'},
            {'class': 'cost'},
        ],
        'goalie_values': [
            {'tag': 'td'},
            {'class': 'value'},
        ],
        'goalie_goals_against': [
            {'tag': 'td'},
            {'class': 'ga'},
        ],
        'goalie_save_attempts': [
            {'tag': 'td'},
            {'class': 'sa'},
        ],
        'goalie_saves': [
            {'tag': 'td'},
            {'class': 'sv'},
        ],
        'goalie_shutouts': [
            {'tag': 'td'},
            {'class': 'so'},
        ],
        'goalie_wins': [
            {'tag': 'td'},
            {'class': 'w'},
        ],
        'goalie_mins': [
            {'tag': 'td'},
            {'class': 'min'},
        ],
    }

    # populate lists
    for i in range(0, len(goalie_html_dict)):
        if i == 0:
            goalie_names = scrapeData(goalie_html_dict, goalie_table, i)
        if i == 1:
            goalie_teams = scrapeData(goalie_html_dict, goalie_table, i)
        if i == 2:
            goalie_opponents = scrapeData(goalie_html_dict, goalie_table, i)
        if i == 3:
            goalie_projections = scrapeData(goalie_html_dict, goalie_table, i)
        if i == 4:
            goalie_salaries = scrapeData(goalie_html_dict, goalie_table, i)
        if i == 5:
            goalie_values = scrapeData(goalie_html_dict, goalie_table, i)
        if i == 6:
            goalie_goals_against = scrapeData(
                goalie_html_dict, goalie_table, i)
        if i == 7:
            goalie_save_attempts = scrapeData(
                goalie_html_dict, goalie_table, i)
        if i == 8:
            goalie_saves = scrapeData(goalie_html_dict, goalie_table, i)
        if i == 9:
            goalie_shutouts = scrapeData(goalie_html_dict, goalie_table, i)
        if i == 10:
            goalie_wins = scrapeData(goalie_html_dict, goalie_table, i)
        if i == 11:
            goalie_mins = scrapeData(goalie_html_dict, goalie_table, i)

    # final stat lists
    goalie_names_final = []
    goalie_teams_final = []
    goalie_opponents_final = []
    goalie_projections_final = []
    goalie_salaries_final = []
    goalie_values_final = []
    goalie_goals_against_final = []
    goalie_save_attempts_final = []
    goalie_saves_final = []
    goalie_shutouts_final = []
    goalie_wins_final = []
    goalie_mins_final = []

    # map initial lists to final lists
    goalie_contents_dict = {
        'goalie_names': [
            {'soup': goalie_names},
            {'final': goalie_names_final},
        ],
        'goalie_teams': [
            {'soup': goalie_teams},
            {'final': goalie_teams_final},
        ],
        'goalie_opponents': [
            {'soup': goalie_opponents},
            {'final': goalie_opponents_final},
        ],
        'goalie_projections': [
            {'soup': goalie_projections},
            {'final': goalie_projections_final},
        ],
        'goalie_salaries': [
            {'soup': goalie_salaries},
            {'final': goalie_salaries_final},
        ],
        'goalie_values': [
            {'soup': goalie_values},
            {'final': goalie_values_final},
        ],
        'goalie_goals_against': [
            {'soup': goalie_goals_against},
            {'final': goalie_goals_against_final},
        ],
        'goalie_save_attempts': [
            {'soup': goalie_save_attempts},
            {'final': goalie_save_attempts_final},
        ],
        'goalie_saves': [
            {'soup': goalie_saves},
            {'final': goalie_saves_final},
        ],
        'goalie_shutouts': [
            {'soup': goalie_shutouts},
            {'final': goalie_shutouts_final},
        ],
        'goalie_wins': [
            {'soup': goalie_wins},
            {'final': goalie_wins_final},
        ],
        'goalie_mins': [
            {'soup': goalie_mins},
            {'final': goalie_mins_final},
        ],
    }

    # get contents
    for i in range(0, len(goalie_contents_dict)):
        if i == 0:
            goalie_names_final = getContents(goalie_contents_dict, i)
        if i == 1:
            goalie_teams_final = getContents(goalie_contents_dict, i)
        if i == 2:
            goalie_opponents_final = getContents(goalie_contents_dict, i)
        if i == 3:
            goalie_projections_final = getContents(goalie_contents_dict, i)
        if i == 4:
            goalie_salaries_final = getContents(goalie_contents_dict, i)
        if i == 5:
            goalie_values_final = getContents(goalie_contents_dict, i)
        if i == 6:
            goalie_goals_against_final = getContents(goalie_contents_dict, i)
        if i == 7:
            goalie_save_attempts_final = getContents(goalie_contents_dict, i)
        if i == 8:
            goalie_saves_final = getContents(goalie_contents_dict, i)
        if i == 9:
            goalie_shutouts_final = getContents(goalie_contents_dict, i)
        if i == 10:
            goalie_wins_final = getContents(goalie_contents_dict, i)
        if i == 11:
            goalie_mins_final = getContents(goalie_contents_dict, i)

    # clean up data
    goalie_teams_final_temp = pd.DataFrame(goalie_teams_final)
    try:
        goalie_teams_final_temp[0] = goalie_teams_final_temp[0].astype(str)
        goalie_teams_final_temp[0] = goalie_teams_final_temp[0].apply(lambda x: x.replace('\\t', '').replace(
            '\\n', '').replace('\'', '').replace('[', '').replace(']', '').strip())
        # print(goalie_teams_final_temp)
    except:
        print('goalie team names list is empty, skipping')

    goalie_opponents_final_temp = pd.DataFrame(goalie_opponents_final)
    try:
        goalie_opponents_final_temp[0] = goalie_opponents_final_temp[0].astype(
            str)
        goalie_opponents_final_temp[0] = goalie_opponents_final_temp[0].apply(lambda x: x.replace('\\t', '').replace(
            '\\n', '').replace('\'', '').replace('[', '').replace(']', '').strip())
        # print(goalie_opponents_final_temp)
    except:
        print('goalie opponent names list is empty, skipping')

    goalie_opponents_final_temp2 = pd.DataFrame(
        [np.nan] * len(goalie_teams_final_temp)).fillna('')

    for i in range(0, len(goalie_teams_final_temp)):
        index = (i + 1) * 2
        index1 = index - 2
        index2 = index - 1
        if goalie_teams_final_temp[0][i] == goalie_opponents_final_temp[0][index1]:
            goalie_opponents_final_temp2[0][i] = goalie_opponents_final_temp[0][index2]
        else:
            goalie_opponents_final_temp2[0][i] = goalie_opponents_final_temp[0][index1]

    goalie_opponents_final = goalie_opponents_final_temp2.values.tolist()

    # make final data frame
    goalie_df = pd.DataFrame()

    goalie_df['Name'] = populateColumn('Name', goalie_names_final)
    goalie_df['Position'] = 'G'
    goalie_df['Team'] = populateColumn('Team', goalie_teams_final)
    goalie_df['Opponent'] = populateColumn('Opponent', goalie_opponents_final)
    goalie_df['Projection'] = populateColumn(
        'Projection', goalie_projections_final)
    goalie_df['Salary'] = populateColumn('Salary', goalie_salaries_final)
    goalie_df['Value'] = populateColumn('Value', goalie_values_final)
    goalie_df['Goals Against'] = populateColumn(
        'Goals Against', goalie_goals_against_final)
    goalie_df['Shots Against'] = populateColumn(
        'Shots Against', goalie_save_attempts_final)
    goalie_df['Saves'] = populateColumn('Saves', goalie_saves_final)
    goalie_df['Shutouts'] = populateColumn('Shutouts', goalie_shutouts_final)
    goalie_df['Wins'] = populateColumn('Wins', goalie_wins_final)
    goalie_df['Minutes'] = populateColumn('Minutes', goalie_mins_final)

    time.sleep(2)

    # combine skater and goalie data frames and clean up
    merge_df = skater_df.append(goalie_df)

    merge_df = merge_df[['Name', 'Position', 'Team', 'Opponent', 'Projection', 'Salary', 'Value',
                         'Shots', 'Goals', 'Assists', 'Points', 'PPG', 'PPA', '+/-', 'Blocks', 'Minutes',
                         'PIM', 'Goals Against', 'Shots Against', 'Saves', 'Shutouts', 'Wins']]

    merge_df['Salary'] = merge_df['Salary'].replace(
        '[\$,]', '', regex=True).astype(float)

    merge_df = merge_df.sort_values(
        by=['Salary', 'Name'], ascending=[False, True])

    merge_df = merge_df.reset_index(drop=True)

    return merge_df


# create data frames
for slate in slate_list:
    nf_df_dict[slate] = createDataFrame(slate)

time.sleep(2)

# combine data frames
final_df = pd.DataFrame()
for slate in slate_list:
    final_df = final_df.append(nf_df_dict[slate])

time.sleep(2)

final_df.drop_duplicates(subset='Name', keep='first', inplace=True)

final_df = final_df.sort_values(by=['Salary', 'Name'], ascending=[False, True])

final_df = final_df.reset_index(drop=True)

time.sleep(2)

# close browser
driver.close()

# export
final_df.to_csv(wd + 'numberfire_fanduel_all.csv', index=False)

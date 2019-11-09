import time
import os
import re

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
wd = 'c:/dev/Python/Repos/dfs-model/nba/data/'

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

prefs = {'download.default_directory': 'c:\dev\Python\Repos\dfs-model\\nba\data\\',
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

# navigate to fanduel projections page
driver.get('https://www.numberfire.com/nba/daily-fantasy/set-dfs-site?site=3')

time.sleep(2)

driver.get(
    'https://www.numberfire.com/nba/daily-fantasy/daily-basketball-projections')

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
        '\\n', '').replace('\"', '').replace('[', '').replace(']', '').strip())
    temp_df[columnName] = temp_df[columnName].apply(
        lambda x: re.sub(r"^'|'$", '', x).strip())
    return temp_df[columnName]


# function to create data frame
def createDataFrame(slate_id):
    # navigate to slate page by ID
    driver.get(
        'https://www.numberfire.com/nba/daily-fantasy/set-slate?slate_id=' + slate_list[0])

    time.sleep(2)

    # navigate to projection page
    driver.get(
        'https://www.numberfire.com/nba/daily-fantasy/daily-basketball-projections')
    players_url = driver.page_source

    time.sleep(2)

    # initial stat lists
    player_names = []
    player_positions = []
    player_teams = []
    player_opponents = []
    player_projections = []
    player_salaries = []
    player_values = []
    player_mins = []
    player_points = []
    player_rebounds = []
    player_assists = []
    player_steals = []
    player_blocks = []
    player_turnovers = []

    # parse page
    player_soup = BeautifulSoup(players_url, 'lxml')
    player_table = player_soup.find(
        'tbody', class_='stat-table__body')

    # web element dictionary
    player_html_dict = {
        'player_names': [
            {'tag': 'a'},
            {'class': 'full'},
        ],
        'player_positions': [
            {'tag': 'span'},
            {'class': 'player-info--position'},
        ],
        'player_teams': [
            {'tag': 'span'},
            {'class': 'team-player__team active'},
        ],
        'player_opponents': [
            {'tag': 'span'},
            {'class': 'team-player__team'},
        ],
        'player_projections': [
            {'tag': 'td'},
            {'class': 'fp active'},
        ],
        'player_salaries': [
            {'tag': 'td'},
            {'class': 'cost'},
        ],
        'player_values': [
            {'tag': 'td'},
            {'class': 'value'},
        ],
        'player_mins': [
            {'tag': 'td'},
            {'class': 'min'},
        ],
        'player_points': [
            {'tag': 'td'},
            {'class': 'pts'},
        ],
        'player_rebounds': [
            {'tag': 'td'},
            {'class': 'reb'},
        ],
        'player_assists': [
            {'tag': 'td'},
            {'class': 'ast'},
        ],
        'player_steals': [
            {'tag': 'td'},
            {'class': 'stl'},
        ],
        'player_blocks': [
            {'tag': 'td'},
            {'class': 'blk'},
        ],
        'player_turnovers': [
            {'tag': 'td'},
            {'class': 'to'},
        ],
    }

    # populate lists
    for i in range(0, len(player_html_dict)):
        if i == 0:
            player_names = scrapeData(player_html_dict, player_table, i)
        if i == 1:
            player_positions = scrapeData(player_html_dict, player_table, i)
        if i == 2:
            player_teams = scrapeData(player_html_dict, player_table, i)
        if i == 3:
            player_opponents = scrapeData(player_html_dict, player_table, i)
        if i == 4:
            player_projections = scrapeData(player_html_dict, player_table, i)
        if i == 5:
            player_salaries = scrapeData(player_html_dict, player_table, i)
        if i == 6:
            player_values = scrapeData(player_html_dict, player_table, i)
        if i == 7:
            player_mins = scrapeData(player_html_dict, player_table, i)
        if i == 8:
            player_points = scrapeData(player_html_dict, player_table, i)
        if i == 9:
            player_rebounds = scrapeData(player_html_dict, player_table, i)
        if i == 10:
            player_assists = scrapeData(player_html_dict, player_table, i)
        if i == 11:
            player_steals = scrapeData(player_html_dict, player_table, i)
        if i == 12:
            player_blocks = scrapeData(player_html_dict, player_table, i)
        if i == 13:
            player_turnovers = scrapeData(player_html_dict, player_table, i)

    # final stat lists
    player_names_final = []
    player_positions_final = []
    player_teams_final = []
    player_opponents_final = []
    player_projections_final = []
    player_salaries_final = []
    player_values_final = []
    player_mins_final = []
    player_points_final = []
    player_rebounds_final = []
    player_assists_final = []
    player_steals_final = []
    player_blocks_final = []
    player_turnovers_final = []

    # map initial lists to final lists
    player_contents_dict = {
        'player_names': [
            {'soup': player_names},
            {'final': player_names_final},
        ],
        'player_positions': [
            {'soup': player_positions},
            {'final': player_positions_final},
        ],
        'player_teams': [
            {'soup': player_teams},
            {'final': player_teams_final},
        ],
        'player_opponents': [
            {'soup': player_opponents},
            {'final': player_opponents_final},
        ],
        'player_projections': [
            {'soup': player_projections},
            {'final': player_projections_final},
        ],
        'player_salaries': [
            {'soup': player_salaries},
            {'final': player_salaries_final},
        ],
        'player_values': [
            {'soup': player_values},
            {'final': player_values_final},
        ],
        'player_mins': [
            {'soup': player_mins},
            {'final': player_mins_final},
        ],
        'player_points': [
            {'soup': player_points},
            {'final': player_points_final},
        ],
        'player_rebounds': [
            {'soup': player_rebounds},
            {'final': player_rebounds_final},
        ],
        'player_assists': [
            {'soup': player_assists},
            {'final': player_assists_final},
        ],
        'player_steals': [
            {'soup': player_steals},
            {'final': player_steals_final},
        ],
        'player_blocks': [
            {'soup': player_blocks},
            {'final': player_blocks_final},
        ],
        'player_turnovers': [
            {'soup': player_turnovers},
            {'final': player_turnovers_final},
        ],
    }

    # get contents
    for i in range(0, len(player_contents_dict)):
        if i == 0:
            player_names_final = getContents(player_contents_dict, i)
        if i == 1:
            player_positions_final = getContents(player_contents_dict, i)
        if i == 2:
            player_teams_final = getContents(player_contents_dict, i)
        if i == 3:
            player_opponents_final = getContents(player_contents_dict, i)
        if i == 4:
            player_projections_final = getContents(player_contents_dict, i)
        if i == 5:
            player_salaries_final = getContents(player_contents_dict, i)
        if i == 6:
            player_values_final = getContents(player_contents_dict, i)
        if i == 7:
            player_mins_final = getContents(player_contents_dict, i)
        if i == 8:
            player_points_final = getContents(player_contents_dict, i)
        if i == 9:
            player_rebounds_final = getContents(player_contents_dict, i)
        if i == 10:
            player_assists_final = getContents(player_contents_dict, i)
        if i == 11:
            player_steals_final = getContents(player_contents_dict, i)
        if i == 12:
            player_blocks_final = getContents(player_contents_dict, i)
        if i == 13:
            player_turnovers_final = getContents(player_contents_dict, i)

    # clean up data
    player_teams_final_temp = pd.DataFrame(player_teams_final)
    try:
        player_teams_final_temp[0] = player_teams_final_temp[0].astype(str)
        player_teams_final_temp[0] = player_teams_final_temp[0].apply(lambda x: x.replace('\\t', '').replace(
            '\\n', '').replace('\'', '').replace('[', '').replace(']', '').strip())
        # print(player_teams_final_temp)
    except:
        print('player team names list is empty, skipping')

    player_opponents_final_temp = pd.DataFrame(player_opponents_final)
    try:
        player_opponents_final_temp[0] = player_opponents_final_temp[0].astype(
            str)
        player_opponents_final_temp[0] = player_opponents_final_temp[0].apply(lambda x: x.replace('\\t', '').replace(
            '\\n', '').replace('\'', '').replace('[', '').replace(']', '').strip())
        # print(player_opponents_final_temp)
    except:
        print('player opponent names list is empty, skipping')

    player_opponents_final_temp2 = pd.DataFrame(
        [np.nan] * len(player_teams_final_temp)).fillna('')

    for i in range(0, len(player_teams_final_temp)):
        index = (i + 1) * 2
        index1 = index - 2
        index2 = index - 1
        if player_teams_final_temp[0][i] == player_opponents_final_temp[0][index1]:
            player_opponents_final_temp2[0][i] = player_opponents_final_temp[0][index2]
        else:
            player_opponents_final_temp2[0][i] = player_opponents_final_temp[0][index1]

    player_opponents_final = player_opponents_final_temp2.values.tolist()

    # make final data frame
    player_df = pd.DataFrame()

    player_df['Name'] = populateColumn('Name', player_names_final)
    player_df['Position'] = populateColumn('Position', player_positions_final)
    player_df['Team'] = populateColumn('Team', player_teams_final)
    player_df['Opponent'] = populateColumn('Opponent', player_opponents_final)
    player_df['Projection'] = populateColumn(
        'Projection', player_projections_final)
    player_df['Salary'] = populateColumn('Salary', player_salaries_final)
    player_df['Value'] = populateColumn('Value', player_values_final)
    player_df['Minutes'] = populateColumn('Minutes', player_mins_final)
    player_df['Points'] = populateColumn('Points', player_points_final)
    player_df['Rebounds'] = populateColumn('Rebounds', player_rebounds_final)
    player_df['Assists'] = populateColumn('Assists', player_assists_final)
    player_df['Steals'] = populateColumn('Steals', player_steals_final)
    player_df['Blocks'] = populateColumn('Blocks', player_blocks_final)
    player_df['Turnovers'] = populateColumn(
        'Turnovers', player_turnovers_final)

    time.sleep(2)

    # clean up
    player_df['Salary'] = player_df['Salary'].replace(
        '[\$,]', '', regex=True).astype(float)

    player_df = player_df.sort_values(
        by=['Salary', 'Name'], ascending=[False, True])

    player_df = player_df.reset_index(drop=True)

    for name in player_df['Name']:
        print(re.sub(r"^'|'$", '', name).strip())

    return player_df


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

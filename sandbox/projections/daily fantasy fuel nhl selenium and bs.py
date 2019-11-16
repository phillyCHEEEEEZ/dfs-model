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
driver.get('https://www.dailyfantasyfuel.com/nhl?platform=fd')

time.sleep(5)

# show all players
show_all = driver.find_element_by_xpath(
    '//*[@id="listings"]/div/li/span')
show_all.click()

time.sleep(2)

# count number of players
player_list = driver.find_element_by_id("listings")
num_players = len(player_list.find_elements_by_tag_name("li")) - 2

time.sleep(2)

# scrape slate URLs
slate_list_dropdown = driver.find_element_by_xpath(
    '//*[@id="makePicks"]/div/div[2]/div/div[1]/div[1]/div')
slate_list_dropdown.click()

slate_list_div = driver.find_element_by_xpath(
    '//*[@id="makePicks"]/div/div[2]/div/div[2]/div')
slate_list_a = slate_list_div.find_elements_by_tag_name('a')

slate_list = []
for a in slate_list_a:
    slate_list.append(a.get_attribute('href'))

time.sleep(2)

num_slates = len(slate_list)

dff_df_dict = {}
for slate in slate_list:
    dff_df_dict[slate] = pd.DataFrame()

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


slate_id = slate_list[0]


# function to create data frame
def createDataFrame(slate_id):


    # navigate to projection page
driver.get(slate_id)
players_url = driver.page_source

# show all players
show_all = driver.find_element_by_xpath(
    '//*[@id="listings"]/div/li/span')
show_all.click()

time.sleep(2)

# initial stat lists
player_names = []
player_positions = []
player_teams = []
player_opponents = []
player_projections = []
player_salaries = []
player_values = []
player_pp = []
player_vegas = []
player_dvp = []

# parse page
player_soup = BeautifulSoup(players_url, 'lxml')
player_table = player_soup.find(
    'ul', class_='listings row-table')

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
    'player_pp': [
        {'tag': 'td'},
        {'class': 's'},
    ],
    'player_vegas': [
        {'tag': 'td'},
        {'class': 'g'},
    ],
    'player_dvp': [
        {'tag': 'td'},
        {'class': 'ast'},
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
        player_pp = scrapeData(player_html_dict, player_table, i)
    if i == 8:
        player_vegas = scrapeData(player_html_dict, player_table, i)
    if i == 9:
        player_dvp = scrapeData(player_html_dict, player_table, i)

# final stat lists
player_names_final = []
player_positions_final = []
player_teams_final = []
player_opponents_final = []
player_projections_final = []
player_salaries_final = []
player_values_final = []
player_pp_final = []
player_vegas_final = []
player_dvp_final = []

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
    'player_pp': [
        {'soup': player_pp},
        {'final': player_pp_final},
    ],
    'player_vegas': [
        {'soup': player_vegas},
        {'final': player_vegas_final},
    ],
    'player_dvp': [
        {'soup': player_dvp},
        {'final': player_dvp_final},
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
        player_pp_final = getContents(player_contents_dict, i)
    if i == 8:
        player_vegas_final = getContents(player_contents_dict, i)
    if i == 9:
        player_dvp_final = getContents(player_contents_dict, i)

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
player_df['PP Unit'] = populateColumn('PP Unit', player_pp_final)
player_df['Vegas'] = populateColumn('Vegas', player_vegas_final)
player_df['DvP'] = populateColumn('DvP', player_dvp_final)

time.sleep(2)

# clean up
player_df = player_df[['Name', 'Position', 'Team', 'Opponent', 'Projection',
                       'Salary', 'Value', 'PP Unit', 'Vegas', 'DvP']]

player_df['Salary'] = player_df['Salary'].replace(
    '[\$,]', '', regex=True).astype(float)

player_df = player_df.sort_values(
    by=['Salary', 'Name'], ascending=[False, True])

player_df = player_df.reset_index(drop=True)

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

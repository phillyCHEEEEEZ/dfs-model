import time
import os

from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from datetime import date, timedelta

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import pandas as pd
import requests
import numpy as np

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

# determine number of players
skaters_url = requests.get(
    'https://www.numberfire.com/nhl/daily-fantasy/daily-hockey-projections/skaters').text

goalie_url = requests.get(
    'https://www.numberfire.com/nhl/daily-fantasy/daily-hockey-projections/goalies').text

skater_names = []
goalie_names = []

skater_soup = BeautifulSoup(skaters_url, 'lxml')
goalie_soup = BeautifulSoup(goalie_url, 'lxml')

skater_table = skater_soup.find(
    'table', class_='stat-table fixed-head')
goalie_table = goalie_soup.find(
    'table', class_='stat-table fixed-head')

html_dict = {
    'names': [
        {'tag': 'a'},
        {'class': 'full'},
    ],
}


def scrapeData(dictionary, soup, index):
    return soup.find_all(
        dictionary[list(dictionary.keys())[index]][0][list(
            list(dictionary[list(dictionary.keys())[index]])[0])[0]], class_=dictionary[list(dictionary.keys())[index]][1][list(
                list(dictionary[list(dictionary.keys())[index]])[1])[0]])


skater_names = scrapeData(html_dict, skater_table, 0)
goalie_names = scrapeData(html_dict, goalie_table, 0)

num_skaters = len(skater_names)
num_goalies = len(goalie_names)
num_players = num_skaters + num_goalies

# xpath strings
# skaters
skater_name_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
skater_name_xpath_2 = ']/td[1]/span/a[2]'

skater_position_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
skater_position_xpath_2 = ']/td[1]/span/span'

skater_team_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
skater_team_xpath_2 = ']/td[1]/span/div/span[1]'
skater_team_xpath_3 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
skater_team_xpath_4 = ']/td[1]/span/div/span[2]'

skater_projection_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
skater_projection_xpath_2 = ']/td[2]'

skater_salary_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
skater_salary_xpath_2 = ']/td[3]'

skater_value_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
skater_value_xpath_2 = ']/td[4]'

skater_shots_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
skater_shots_xpath_2 = ']/td[5]'

skater_goals_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
skater_goals_xpath_2 = ']/td[6]'

skater_assists_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
skater_assists_xpath_2 = ']/td[7]'

skater_points_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
skater_points_xpath_2 = ']/td[8]'

skater_ppg_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
skater_ppg_xpath_2 = ']/td[9]'

skater_ppa_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
skater_ppa_xpath_2 = ']/td[10]'

skater_plusminus_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
skater_plusminus_xpath_2 = ']/td[11]'

skater_blocks_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
skater_blocks_xpath_2 = ']/td[12]'

skater_minutes_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
skater_minutes_xpath_2 = ']/td[13]'

skater_pim_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
skater_pim_xpath_2 = ']/td[14]'

# goalies
goalie_name_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
goalie_name_xpath_2 = ']/td[1]/span/a[2]'

goalie_position_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
goalie_position_xpath_2 = ']/td[1]/span/span'

goalie_team_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
goalie_team_xpath_2 = ']/td[1]/span/div/span[1]'
goalie_team_xpath_3 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
goalie_team_xpath_4 = ']/td[1]/span/div/span[2]'

goalie_projection_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
goalie_projection_xpath_2 = ']/td[2]'

goalie_salary_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
goalie_salary_xpath_2 = ']/td[3]'

goalie_value_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
goalie_value_xpath_2 = ']/td[4]'

goalie_goals_against_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
goalie_goals_against_xpath_2 = ']/td[5]'

goalie_shots_against_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
goalie_shots_against_xpath_2 = ']/td[6]'

goalie_saves_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
goalie_saves_xpath_2 = ']/td[7]'

goalie_shutouts_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
goalie_shutouts_xpath_2 = ']/td[8]'

goalie_wins_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
goalie_wins_xpath_2 = ']/td[9]'

goalie_minutes_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
goalie_minutes_xpath_2 = ']/td[10]'


# function to populate columns
def populateColumn(df, num_rows, xpath1, xpath2, xpath3='', xpath4='', opponent=False):
    df = pd.DataFrame(index=range(num_rows), columns=range(1))
    for i in range(0, num_rows):
        row = i + 1
        xpath_final1 = xpath1 + str(row) + xpath2
        xpath_final2 = xpath3 + str(row) + xpath4
        content = driver.find_element_by_xpath(xpath_final1)
        if (xpath3 != '' and xpath4 != '' and opponent == False):
            if (content.get_attribute('class') == 'team-player__team active'):
                df[0][i] = content.text
            else:
                content = driver.find_element_by_xpath(xpath_final2)
                df[0][i] = content.text
        elif (xpath3 != '' and xpath4 != '' and opponent == True):
            if (content.get_attribute('class') == 'team-player__team '):
                df[0][i] = content.text
            else:
                content = driver.find_element_by_xpath(xpath_final2)
                df[0][i] = content.text
        else:
            df[0][i] = content.text
    return df[0]


# create data frames
# navigate to skater projections page
driver.get(
    'https://www.numberfire.com/nhl/daily-fantasy/daily-hockey-projections/skaters')

# select fanduel from dropdown list
dropdown = driver.find_element_by_class_name('custom-drop__current')
dropdown.click()

dropdown_fanduel = driver.find_element_by_xpath('//li[@data-value="3"]')
dropdown_fanduel.click()

# initialize data frame
skater_df = pd.DataFrame(index=range(num_skaters), columns=range(17))
skater_df.columns = ['Name', 'Position', 'Team', 'Opponent', 'Projection', 'Salary', 'Value',
                     'Shots', 'Goals', 'Assists', 'Points', 'PPG', 'PPA', '+/-', 'Blocks', 'Minutes', 'PIM']

time.sleep(5)

# populate skater data
skater_df['Name'] = populateColumn(
    skater_df, num_skaters, skater_name_xpath_1, skater_name_xpath_2)
skater_df['Position'] = populateColumn(
    skater_df, num_skaters, skater_position_xpath_1, skater_position_xpath_2)
skater_df['Team'] = populateColumn(
    skater_df, num_skaters, skater_team_xpath_1, skater_team_xpath_2, skater_team_xpath_3, skater_team_xpath_4)
skater_df['Opponent'] = populateColumn(
    skater_df, num_skaters, skater_team_xpath_1, skater_team_xpath_2, skater_team_xpath_3, skater_team_xpath_4, opponent=True)
skater_df['Projection'] = populateColumn(
    skater_df, num_skaters, skater_projection_xpath_1, skater_projection_xpath_2)
skater_df['Salary'] = populateColumn(
    skater_df, num_skaters, skater_salary_xpath_1, skater_salary_xpath_2)
skater_df['Value'] = populateColumn(
    skater_df, num_skaters, skater_value_xpath_1, skater_value_xpath_2)
skater_df['Shots'] = populateColumn(
    skater_df, num_skaters, skater_shots_xpath_1, skater_shots_xpath_2)
skater_df['Goals'] = populateColumn(
    skater_df, num_skaters, skater_goals_xpath_1, skater_goals_xpath_2)
skater_df['Assists'] = populateColumn(
    skater_df, num_skaters, skater_assists_xpath_1, skater_assists_xpath_2)
skater_df['Points'] = populateColumn(
    skater_df, num_skaters, skater_points_xpath_1, skater_points_xpath_2)
skater_df['PPG'] = populateColumn(
    skater_df, num_skaters, skater_ppg_xpath_1, skater_ppg_xpath_2)
skater_df['PPA'] = populateColumn(
    skater_df, num_skaters, skater_ppa_xpath_1, skater_ppa_xpath_2)
skater_df['+/-'] = populateColumn(
    skater_df, num_skaters, skater_plusminus_xpath_1, skater_plusminus_xpath_2)
skater_df['Blocks'] = populateColumn(
    skater_df, num_skaters, skater_blocks_xpath_1, skater_blocks_xpath_2)
skater_df['Minutes'] = populateColumn(
    skater_df, num_skaters, skater_minutes_xpath_1, skater_minutes_xpath_2)
skater_df['PIM'] = populateColumn(
    skater_df, num_skaters, skater_pim_xpath_1, skater_pim_xpath_2)

time.sleep(5)

# navigate to goalie projections page
driver.get(
    'https://www.numberfire.com/nhl/daily-fantasy/daily-hockey-projections/goalies')

# select fanduel from dropdown list
dropdown = driver.find_element_by_class_name('custom-drop__current')
dropdown.click()

dropdown_fanduel = driver.find_element_by_xpath('//li[@data-value="3"]')
dropdown_fanduel.click()

# initialize data frame
goalie_df = pd.DataFrame(index=range(num_goalies), columns=range(13))
goalie_df.columns = ['Name', 'Position', 'Team', 'Opponent', 'Projection', 'Salary', 'Value',
                     'Goals Against', 'Shots Against', 'Saves', 'Shutouts', 'Wins', 'Minutes']

time.sleep(5)

# populate goalie data
goalie_df['Name'] = populateColumn(
    goalie_df, num_goalies, goalie_name_xpath_1, goalie_name_xpath_2)
goalie_df['Position'] = 'G'
goalie_df['Team'] = populateColumn(
    goalie_df, num_goalies, goalie_team_xpath_1, goalie_team_xpath_2, goalie_team_xpath_3, goalie_team_xpath_4)
goalie_df['Opponent'] = populateColumn(
    goalie_df, num_goalies, goalie_team_xpath_1, goalie_team_xpath_2, goalie_team_xpath_3, goalie_team_xpath_4, opponent=True)
goalie_df['Projection'] = populateColumn(
    goalie_df, num_goalies, goalie_projection_xpath_1, goalie_projection_xpath_2)
goalie_df['Salary'] = populateColumn(
    goalie_df, num_goalies, goalie_salary_xpath_1, goalie_salary_xpath_2)
goalie_df['Value'] = populateColumn(
    goalie_df, num_goalies, goalie_value_xpath_1, goalie_value_xpath_2)
goalie_df['Goals Against'] = populateColumn(
    goalie_df, num_goalies, goalie_goals_against_xpath_1, goalie_goals_against_xpath_2)
goalie_df['Shots Against'] = populateColumn(
    goalie_df, num_goalies, goalie_shots_against_xpath_1, goalie_shots_against_xpath_2)
goalie_df['Saves'] = populateColumn(
    goalie_df, num_goalies, goalie_saves_xpath_1, goalie_saves_xpath_2)
goalie_df['Shutouts'] = populateColumn(
    goalie_df, num_goalies, goalie_shutouts_xpath_1, goalie_shutouts_xpath_2)
goalie_df['Wins'] = populateColumn(
    goalie_df, num_goalies, goalie_wins_xpath_1, goalie_wins_xpath_2)
goalie_df['Minutes'] = populateColumn(
    goalie_df, num_goalies, goalie_minutes_xpath_1, goalie_minutes_xpath_2)

time.sleep(5)

# close browser
driver.close()

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

# export
merge_df.to_csv(
    'c:/dev/Python/Repos/dfs-model/nhl/data/numberfire_fanduel_all.csv',
    index=False)

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

# determine number of players
players_url = requests.get(
    'https://www.numberfire.com/nba/daily-fantasy/daily-basketball-projections').text

player_names = []

player_soup = BeautifulSoup(players_url, 'lxml')

player_table = player_soup.find(
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


player_names = scrapeData(html_dict, player_table, 0)

num_players = len(player_names)

# xpath strings
name_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
name_xpath_2 = ']/td[1]/span/a[2]'

position_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
position_xpath_2 = ']/td[1]/span/span'

team_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
team_xpath_2 = ']/td[1]/span/div/span[1]'
team_xpath_3 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
team_xpath_4 = ']/td[1]/span/div/span[2]'

projection_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
projection_xpath_2 = ']/td[2]'

salary_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
salary_xpath_2 = ']/td[3]'

value_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
value_xpath_2 = ']/td[4]'

minutes_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
minutes_xpath_2 = ']/td[5]'

points_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
points_xpath_2 = ']/td[6]'

rebounds_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
rebounds_xpath_2 = ']/td[7]'

assists_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
assists_xpath_2 = ']/td[8]'

steals_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
steals_xpath_2 = ']/td[9]'

blocks_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
blocks_xpath_2 = ']/td[10]'

turnovers_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
turnovers_xpath_2 = ']/td[11]'


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
# navigate to projections page
driver.get(
    'https://www.numberfire.com/nba/daily-fantasy/daily-basketball-projections')

# select fanduel from dropdown list
dropdown = driver.find_element_by_class_name('custom-drop__current')
dropdown.click()

dropdown_fanduel = driver.find_element_by_xpath('//li[@data-value="3"]')
dropdown_fanduel.click()

# initialize data frame
player_df = pd.DataFrame(index=range(num_players), columns=range(14))
player_df.columns = ['Name', 'Position', 'Team', 'Opponent', 'Projection', 'Salary', 'Value',
                     'Minutes', 'Points', 'Rebounds', 'Assists', 'Steals', 'Blocks', 'Turnovers']

time.sleep(5)

# populate data
player_df['Name'] = populateColumn(
    player_df, num_players, name_xpath_1, name_xpath_2)
player_df['Position'] = populateColumn(
    player_df, num_players, position_xpath_1, position_xpath_2)
player_df['Team'] = populateColumn(
    player_df, num_players, team_xpath_1, team_xpath_2, team_xpath_3, team_xpath_4)
player_df['Opponent'] = populateColumn(
    player_df, num_players, team_xpath_1, team_xpath_2, team_xpath_3, team_xpath_4, opponent=True)
player_df['Projection'] = populateColumn(
    player_df, num_players, projection_xpath_1, projection_xpath_2)
player_df['Salary'] = populateColumn(
    player_df, num_players, salary_xpath_1, salary_xpath_2)
player_df['Value'] = populateColumn(
    player_df, num_players, value_xpath_1, value_xpath_2)
player_df['Minutes'] = populateColumn(
    player_df, num_players, minutes_xpath_1, minutes_xpath_2)
player_df['Points'] = populateColumn(
    player_df, num_players, points_xpath_1, points_xpath_2)
player_df['Rebounds'] = populateColumn(
    player_df, num_players, rebounds_xpath_1, rebounds_xpath_2)
player_df['Assists'] = populateColumn(
    player_df, num_players, assists_xpath_1, assists_xpath_2)
player_df['Steals'] = populateColumn(
    player_df, num_players, steals_xpath_1, steals_xpath_2)
player_df['Blocks'] = populateColumn(
    player_df, num_players, blocks_xpath_1, blocks_xpath_2)
player_df['Turnovers'] = populateColumn(
    player_df, num_players, turnovers_xpath_1, turnovers_xpath_2)

time.sleep(5)

# close browser
driver.close()

# export
player_df.to_csv(
    'c:/dev/Python/Repos/dfs-model/nba/data/numberfire_fanduel.csv',
    index=False)

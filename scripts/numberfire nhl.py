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

prefs = {'download.default_directory': 'c:\dev\Python\Repos\dfs-model\\',
         'download.prompt_for_download': False,
         'download.directory_upgrade': True, }

options.add_experimental_option('prefs', prefs)

# load browser
driver = webdriver.Chrome(chromedriver, options=options)

# navigate to login page
driver.get('https://www.numberfire.com/account/login-google-plus')

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

shots_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
shots_xpath_2 = ']/td[5]'

goals_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
goals_xpath_2 = ']/td[6]'

assists_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
assists_xpath_2 = ']/td[7]'

points_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
points_xpath_2 = ']/td[8]'

ppg_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
ppg_xpath_2 = ']/td[9]'

ppa_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
ppa_xpath_2 = ']/td[10]'

plusminus_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
plusminus_xpath_2 = ']/td[11]'

blocks_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
blocks_xpath_2 = ']/td[12]'

minutes_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
minutes_xpath_2 = ']/td[13]'

pim_xpath_1 = '/html/body/main/div[2]/div[2]/section/div[4]/div[2]/table/tbody/tr['
pim_xpath_2 = ']/td[14]'

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


# populate skater data
skater_df['Name'] = populateColumn(
    skater_df, num_skaters, name_xpath_1, name_xpath_2)
skater_df['Position'] = populateColumn(
    skater_df, num_skaters, position_xpath_1, position_xpath_2)
skater_df['Team'] = populateColumn(
    skater_df, num_skaters, team_xpath_1, team_xpath_2, team_xpath_3, team_xpath_4)
skater_df['Opponent'] = populateColumn(
    skater_df, num_skaters, team_xpath_1, team_xpath_2, team_xpath_3, team_xpath_4, opponent=True)
skater_df['Projection'] = populateColumn(
    skater_df, num_skaters, projection_xpath_1, projection_xpath_2)
skater_df['Salary'] = populateColumn(
    skater_df, num_skaters, salary_xpath_1, salary_xpath_2)
skater_df['Value'] = populateColumn(
    skater_df, num_skaters, value_xpath_1, value_xpath_2)
skater_df['Shots'] = populateColumn(
    skater_df, num_skaters, shots_xpath_1, shots_xpath_2)
skater_df['Goals'] = populateColumn(
    skater_df, num_skaters, goals_xpath_1, goals_xpath_2)
skater_df['Assists'] = populateColumn(
    skater_df, num_skaters, assists_xpath_1, assists_xpath_2)
skater_df['Points'] = populateColumn(
    skater_df, num_skaters, points_xpath_1, points_xpath_2)
skater_df['PPG'] = populateColumn(
    skater_df, num_skaters, ppg_xpath_1, ppg_xpath_2)
skater_df['PPA'] = populateColumn(
    skater_df, num_skaters, ppa_xpath_1, ppa_xpath_2)
skater_df['+/-'] = populateColumn(
    skater_df, num_skaters, plusminus_xpath_1, plusminus_xpath_2)
skater_df['Blocks'] = populateColumn(
    skater_df, num_skaters, blocks_xpath_1, blocks_xpath_2)
skater_df['Minutes'] = populateColumn(
    skater_df, num_skaters, minutes_xpath_1, minutes_xpath_2)
skater_df['PIM'] = populateColumn(
    skater_df, num_skaters, pim_xpath_1, pim_xpath_2)

time.sleep(5)

# close
driver.close()

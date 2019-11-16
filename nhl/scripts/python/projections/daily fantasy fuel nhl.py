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

# navigate to projections page
driver.get('http://www.dailyfantasyfuel.com/nhl?platform=fd')

time.sleep(5)

# show all players
show_all = driver.find_element_by_xpath(
    '//*[@id="listings"]/div/li/span')
show_all.click()

time.sleep(2)

# count number of players
player_list = driver.find_element_by_id("listings")
num_players = len(player_list.find_elements_by_tag_name("li")) - 2

# //*[@id = "listings"]/li[3]/div/div[1]/div[7]/span[1]
# /html/body/div[5]/section[1]/div[2]/div[1]/section/div/ul/li[3]/div/div[1]/div[7]/span[1]

# xpath strings
name_xpath_1 = '//*[@id="listings"]/li['
name_xpath_2 = ']/div/div[1]/div[7]/span[1]'

position_xpath_1 = '//*[@id="listings"]/li['
position_xpath_2 = ']/div/div[1]/div[2]/div'

team_xpath_1 = '//*[@id="listings"]/li['
team_xpath_2 = ']/div/div[1]/div[3]/div'

opponent_xpath_1 = '//*[@id="listings"]/li['
opponent_xpath_2 = ']/div/div[1]/div[4]/div'

projection_xpath_1 = '//*[@id="listings"]/li['
projection_xpath_2 = ']/div/div[2]/div[2]/div[4]/input'

salary_xpath_1 = '//*[@id="listings"]/li['
salary_xpath_2 = ']/div/div[2]/div[2]/div[5]'

value_xpath_1 = '//*[@id="listings"]/li['
value_xpath_2 = ']/div/div[2]/div[2]/div[2]/span[1]'

ppunit_xpath_1 = '//*[@id="listings"]/li['
ppunit_xpath_2 = ']/div/div[1]/div[6]/div'

vegas_xpath_1 = '//*[@id="listings"]/li['
vegas_xpath_2 = ']/div/div[1]/div[5]/div'

dvp_xpath_1 = '//*[@id="listings"]/li['
dvp_xpath_2 = ']/div/div[2]/div[2]/div[1]'


# function to populate columns
def populateColumn(df, num_rows, xpath1, xpath2, projection=False):
    df = pd.DataFrame(index=range(num_rows), columns=range(1))
    for i in range(0, num_rows):
        row = i + 3
        xpath_final1 = xpath1 + str(row) + xpath2
        content = driver.find_element_by_xpath(xpath_final1)
        if (projection == True):
            df[0][i] = content.get_attribute("value")
        else:
            df[0][i] = content.text
    return df[0]


# initialize data frame
dff_df = pd.DataFrame(index=range(num_players), columns=range(10))
dff_df.columns = ['Name', 'Position', 'Team', 'Opponent', 'Projection',
                  'Salary', 'Value', 'PP Unit', 'Vegas', 'DvP']

time.sleep(2)

# populate data frame
dff_df['Name'] = populateColumn(
    dff_df, num_players, name_xpath_1, name_xpath_2)
dff_df['Position'] = populateColumn(
    dff_df, num_players, position_xpath_1, position_xpath_2)
dff_df['Team'] = populateColumn(
    dff_df, num_players, team_xpath_1, team_xpath_2)
dff_df['Opponent'] = populateColumn(
    dff_df, num_players, opponent_xpath_1, opponent_xpath_2)
dff_df['Projection'] = populateColumn(
    dff_df, num_players, projection_xpath_1, projection_xpath_2, projection=True)
dff_df['Salary'] = populateColumn(
    dff_df, num_players, salary_xpath_1, salary_xpath_2)
dff_df['Value'] = populateColumn(
    dff_df, num_players, value_xpath_1, value_xpath_2)
dff_df['PP Unit'] = populateColumn(
    dff_df, num_players, ppunit_xpath_1, ppunit_xpath_2)
dff_df['Vegas'] = populateColumn(
    dff_df, num_players, vegas_xpath_1, vegas_xpath_2)
dff_df['DvP'] = populateColumn(
    dff_df, num_players, dvp_xpath_1, dvp_xpath_2)

time.sleep(2)

# close browser
driver.close()

# export
dff_df.to_csv(wd + 'dff_fanduel_all.csv', index=False)

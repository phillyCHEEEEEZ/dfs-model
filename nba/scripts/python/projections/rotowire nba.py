import time
import os
import datetime
import csv
import pandas as pd

from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from datetime import date, timedelta

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# datetime vars
now = datetime.datetime.now()
today = str(now.strftime('%Y-%m-%d'))

# working directory
wd = 'c:/dev/Python/Repos/dfs-model/nba/data/'

# load env vars
load_dotenv()

# login credentials
rw_username = os.getenv('RW_USERNAME')
rw_password = os.getenv('RW_PASSWORD')

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
driver.get('https://www.rotowire.com/users/login.php')

# log in
username = driver.find_element_by_xpath(
    '/html/body/div[1]/div/main/div/div[1]/form/input[1]')
username.send_keys(rw_username)

password = driver.find_element_by_xpath(
    '/html/body/div[1]/div/main/div/div[1]/form/input[2]')
password.send_keys(rw_password)

login = driver.find_element_by_xpath(
    '/html/body/div[1]/div/main/div/div[1]/form/button')
login.click()

time.sleep(5)

# navigate to fp projections page
driver.get(
    'https://www.rotowire.com/daily/nba/value-report.php?site=FanDuel&slate=Main&type=main')

# wait for download button to render
WebDriverWait(driver, 5).until(EC.presence_of_element_located(
    (By.XPATH, '//*[@id="NBAPlayers"]/div[3]/div[2]/button[2]')))

# click download button
download_button = driver.find_element_by_xpath(
    '//*[@id="NBAPlayers"]/div[3]/div[2]/button[2]')
download_button.click()

time.sleep(2)

# rename file
os.rename(wd + 'rotowire-NBA-players.csv',
          wd + 'rotowire-fanduel-NBA-fp-projections.csv')

# navigate to stats projections page
driver.get(
    'https://www.rotowire.com/basketball/projections.php?type=daily')

# wait for download button to render
WebDriverWait(driver, 5).until(EC.presence_of_element_located(
    (By.XPATH, '//*[@id="nba-projections"]/div[3]/div[2]/button[2]')))

# click download button
download_button = driver.find_element_by_xpath(
    '//*[@id="nba-projections"]/div[3]/div[2]/button[2]')
download_button.click()

time.sleep(2)

# rename file
os.rename(wd + 'rotowire-nba-projections.csv',
          wd + 'rotowire-fanduel-NBA-stats-projections.csv')

# close browser
driver.close()

####### combine files ######
# import data
rw_proj_df = pd.read_csv(wd + 'rotowire-fanduel-NBA-fp-projections.csv')
rw_stats_df = pd.read_csv(wd + 'rotowire-fanduel-NBA-stats-projections.csv')

# fix headers
rw_stats_df = rw_stats_df.rename(columns=rw_stats_df.iloc[0])
rw_stats_df = rw_stats_df.iloc[1:, ]

# merge
rw_all_df = rw_proj_df.merge(rw_stats_df[['NAME', 'PTS', 'REB', 'AST',
                                          'STL', 'BLK', 'TO', 'FGM', 'FGA',
                                          'FG%', '3PM', '3PA', '3P%', 'FTM',
                                          'FTA', 'FT%', 'OREB', 'DREB']],
                             left_on='PLAYER', right_on='NAME', how='left')

del rw_all_df['NAME']

# export
rw_all_df.to_csv(wd + 'rotowire-fanduel-NBA-all.csv',
                 index=False)

# delete files
os.remove(wd + 'rotowire-fanduel-NBA-fp-projections.csv')
os.remove(wd + 'rotowire-fanduel-NBA-stats-projections.csv')

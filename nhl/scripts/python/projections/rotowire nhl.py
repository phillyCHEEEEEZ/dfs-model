import time
import os
import datetime

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
wd = 'c:/dev/Python/Repos/dfs-model/nhl/data/'

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

prefs = {'download.default_directory': 'c:\dev\Python\Repos\dfs-model\\nhl\data\\',
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
    'https://www.rotowire.com/daily/nhl/value-report.php?site=FanDuel&slate=Main&type=main')

# wait for download button to render
WebDriverWait(driver, 5).until(EC.presence_of_element_located(
    (By.XPATH, '//*[@id="NHLPlayers"]/div[3]/div[2]/button[2]')))

# click download button
download_button = driver.find_element_by_xpath(
    '//*[@id="NHLPlayers"]/div[3]/div[2]/button[2]')
download_button.click()

time.sleep(2)

# rename file
os.rename(wd + 'rotowire-NHL-players.csv',
          wd + 'rotowire-fanduel-NHL-players-projections.csv')

# navigate to skater stats projections pages
driver.get(
    'https://www.rotowire.com/hockey/projections-daily.php')

# wait for download button to render
WebDriverWait(driver, 5).until(EC.presence_of_element_located(
    (By.XPATH, '//*[@id="NHLDailyProjections"]/div[3]/div[2]/button[2]')))

# click download button
download_button = driver.find_element_by_xpath(
    '//*[@id="NHLDailyProjections"]/div[3]/div[2]/button[2]')
download_button.click()

time.sleep(2)

# rename file
os.rename(wd + 'rotowire-nhl-projections-' + today + '.csv',
          wd + 'rotowire-fanduel-NHL-skaters-stats.csv')

# navigate to goalie stats projections pages
driver.get(
    'https://www.rotowire.com/hockey/projections-daily.php?pos=goalie')

# wait for download button to render
WebDriverWait(driver, 5).until(EC.presence_of_element_located(
    (By.XPATH, '//*[@id="NHLDailyProjections"]/div[3]/div[2]/button[2]')))

# click download button
download_button = driver.find_element_by_xpath(
    '//*[@id="NHLDailyProjections"]/div[3]/div[2]/button[2]')
download_button.click()

time.sleep(2)

# rename file
os.rename(wd + 'rotowire-nhl-projections-' + today + '.csv',
          wd + 'rotowire-fanduel-NHL-goalies-stats.csv')

# close browser
driver.close()

import time
import os
import csv
import datetime
import pandas as pd
import datetime

from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from datetime import date, timedelta

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# load env vars
load_dotenv()

# login credentials
bm_username = os.getenv('BM_USERNAME')
bm_password = os.getenv('BM_PASSWORD')

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
driver.get('https://basketballmonster.com/login.aspx')

# log in
username = driver.find_element_by_xpath(
    '//*[@id="UsernameTB"]')
username.send_keys(bm_username)

password = driver.find_element_by_xpath(
    '//*[@id="PasswordTB"]')
password.send_keys(bm_password)

login = driver.find_element_by_xpath(
    '//*[@id="LoginButton"]')
login.click()

time.sleep(5)

# navigate to projections page
driver.get(
    'https://basketballmonster.com/Daily.aspx')

time.sleep(5)

# click fanduel button
try:
    fanduel_button = driver.find_element_by_xpath(
        '//*[@id="form1"]/div[3]/div[2]/table/tbody/tr/td[4]/table/tbody/tr[2]/td[1]/div/input')
    fanduel_button.click()
except:
    try:
        fanduel_button = driver.find_element_by_xpath(
            '//*[@id="form1"]/div[4]/div[2]/table/tbody/tr/td[4]/table/tbody/tr[2]/td[1]/div/input')
        fanduel_button.click()
    except:
        fanduel_button = driver.find_element_by_xpath(
            '//*[@id="form1"]/div[5]/div[2]/table/tbody/tr/td[4]/table/tbody/tr[2]/td[1]/div/input')
        fanduel_button.click()

# wait for download button to render
WebDriverWait(driver, 5).until(EC.presence_of_element_located(
    (By.XPATH, '//*[@id="ContentPlaceHolder1_ButtonCSV2Button"]')))

# click download button
download_button = driver.find_element_by_xpath(
    '//*[@id="ContentPlaceHolder1_ButtonCSV2Button"]')
download_button.click()

# click download button
download_button = driver.find_element_by_xpath(
    '//*[@id="ContentPlaceHolder1_ExportValueCSVButton"]')
download_button.click()

time.sleep(5)

# close browser
driver.close()

# merge files
# datetime vars
now = datetime.datetime.now()
today = str(now.strftime('%Y_%m_%d'))
timestamp = str(now.strftime('_%Y-%m-%d_%H-%M-%S'))

# filename vars
data_dir = 'c:/dev/Python/Repos/dfs-model/nba/data/'
names_filename = 'master/names.xlsx'
bm_stats_filename = 'Export_' + today + '.csv'
bm_projections_filename = 'ValuesExport_' + today + '.csv'

# read CSVs
names_df = pd.read_excel(data_dir + names_filename)
bm_stats_df = pd.read_csv(data_dir + bm_stats_filename)
bm_projections_df = pd.read_csv(data_dir + bm_projections_filename)

# combine files
bm_stats_df["full_name"] = bm_stats_df["first_name"] + \
    ' ' + bm_stats_df["last_name"]

try:
    bm_projections_df = bm_projections_df.merge(
        bm_stats_df, left_on='Player', right_on='full_name', how='left')
except:
    bm_projections_df = bm_projections_df.merge(
        bm_stats_df, left_on='Name', right_on='full_name', how='left')

del bm_projections_df["full_name"]

# export
bm_projections_df.to_csv(
    'c:/dev/Python/Repos/dfs-model/nba/data/basketball_monster_fanduel.csv',
    index=False)

# rename file
os.remove(data_dir + bm_stats_filename)
os.remove(data_dir + bm_projections_filename)

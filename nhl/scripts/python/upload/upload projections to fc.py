import os
import pandas as pd
import pyperclip

from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from datetime import date, timedelta

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# load env vars
load_dotenv()

# login credentials
fc_username = os.getenv('FC_USERNAME')
fc_password = os.getenv('FC_PASSWORD')

# read in projections csv
fc_upload_df = pd.read_csv(
    'c:/dev/Python/Repos/dfs-model/nhl/data/fc_upload.csv')

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
driver.get('https://www.fantasycruncher.com/login/')

# log in
username = driver.find_element_by_id('user_email')
username.send_keys(fc_username)

password = driver.find_element_by_id('user_password')
password.send_keys(fc_password)

login = driver.find_element_by_id('submit')
login.click()

# navigate to projections page
driver.get('https://www.fantasycruncher.com/lineup-cruncher/fanduel/NHL')

# wait for actions button to render
WebDriverWait(driver, 5).until(EC.presence_of_element_located(
    (By.XPATH, '//div[@data-action="downloadPlayerlist"]')))

# click upload data button
upload_data_button = driver.find_element_by_xpath(
    '/html/body/div[3]/nav/ul/div/li[2]/a/i')
upload_data_button.click()

time.sleep(5)

# select first cell in player column
player_col = driver.find_element_by_xpath(
    '//*[@id="upload-proj-table"]/div[1]/div[1]/div/div[1]/table/tbody/tr[1]/td[1]')
player_col.click()

# populate names and projections
for i in range(0, len(fc_upload_df) - 1):
    actions = ActionChains(driver)
    actions.send_keys(fc_upload_df['Player'][i])
    actions.send_keys(Keys.TAB)
    actions.send_keys(str(fc_upload_df['Avg'][i]))
    actions.send_keys(Keys.ENTER)
    actions.send_keys(Keys.LEFT)
    actions.perform()
    del actions

# click button to upload projections
upload_projections_button = driver.find_element_by_xpath(
    '//*[@id="import-proj"]')
upload_projections_button.click()

time.sleep(10)

# close browser
driver.close()

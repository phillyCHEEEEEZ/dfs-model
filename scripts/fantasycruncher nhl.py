import time
import os

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
fc_username = os.getenv('FC_USERNAME')
fc_password = os.getenv('FC_PASSWORD')

# path to webdrive exe
chromedriver = (
    'C:/dev/Web Drivers/chromedriver_win32/chromedriver.exe')

# set options
options = webdriver.ChromeOptions()

prefs = {'download.default_directory': 'c:\dev\Python\Repos\dfs-model\\',
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

# click actions dropdown
actions_dropdown = driver.find_element_by_id('table-actions')
actions_dropdown.click()

# click download button
download_button = driver.find_element_by_xpath(
    '//div[@data-action="downloadPlayerlist"]')
download_button.click()

time.sleep(5)

# close browser
driver.close()

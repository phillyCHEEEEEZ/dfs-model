import time
import os

from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from datetime import date, timedelta

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

sleepTime = 5

chromedriver = (
    'C:/dev/Web Drivers/chromedriver_win32/chromedriver.exe')

options = webdriver.ChromeOptions()

prefs = {'download.default_directory': 'C:\dev\Python\Scripts\Web Scraping\\',
         'download.prompt_for_download': False,
         'download.directory_upgrade': True, }

options.add_experimental_option('prefs', prefs)

driver = webdriver.Chrome(chromedriver, options=options)

fc_username = os.getenv('FC_USERNAME')
fc_password = os.getenv('FC_PASSWORD')

driver.get('https://www.fantasycruncher.com/login/')

username = driver.find_element_by_id('user_email')
username.send_keys(fc_username)

password = driver.find_element_by_id('user_password')
password.send_keys(fc_password)

login = driver.find_element_by_id('submit')
login.click()

driver.get('https://www.fantasycruncher.com/lineup-cruncher/fanduel/NHL')

WebDriverWait(driver, 5).until(EC.presence_of_element_located(
    (By.XPATH, '//div[@data-action="downloadPlayerlist"]')))

actions = driver.find_element_by_id('table-actions')
actions.click()

downloadPlayerlist = driver.find_element_by_xpath(
    '//div[@data-action="downloadPlayerlist"]')
downloadPlayerlist.click()

time.sleep(sleepTime)

driver.close()

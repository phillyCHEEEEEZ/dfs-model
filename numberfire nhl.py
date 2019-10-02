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

chromedriver = (
    'C:/dev/Web Drivers/chromedriver_win32/chromedriver.exe')

options = webdriver.ChromeOptions()

prefs = {'download.default_directory': 'c:\dev\Python\Repos\dfs-model\\',
         'download.prompt_for_download': False,
         'download.directory_upgrade': True, }

options.add_experimental_option('prefs', prefs)

driver = webdriver.Chrome(chromedriver, options=options)

nf_username = os.getenv('NF_USERNAME')
nf_password = os.getenv('NF_PASSWORD')

driver.get(
    'https://www.numberfire.com/account/login-google-plus')

WebDriverWait(driver, 5).until(EC.presence_of_element_located(
    (By.XPATH, '//*[@id="identifierId"]')))

username = driver.find_element_by_xpath(
    '//*[@id="identifierId"]')
username.send_keys(nf_username)

nextButton = driver.find_element_by_xpath(
    '//*[@id="identifierNext"]/span/span')
nextButton.click()

time.sleep(2)

WebDriverWait(driver, 5).until(EC.presence_of_element_located(
    (By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')))

password = driver.find_element_by_xpath(
    '//*[@id="password"]/div[1]/div/div[1]/input')
password.send_keys(nf_password)

nextButton = driver.find_element_by_xpath(
    '//*[@id="passwordNext"]/span/span')
nextButton.click()

time.sleep(2)

driver.get(
    'https://www.numberfire.com/nhl/daily-fantasy/daily-hockey-projections/skaters')

driver.close()

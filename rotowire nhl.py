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

prefs = {'download.default_directory': 'c:\dev\Python\Repos\dfs-model\\',
         'download.prompt_for_download': False,
         'download.directory_upgrade': True, }

options.add_experimental_option('prefs', prefs)

driver = webdriver.Chrome(chromedriver, options=options)

rw_username = os.getenv('RW_USERNAME')
rw_password = os.getenv('RW_PASSWORD')

driver.get('https://www.rotowire.com/users/login.php')

username = driver.find_element_by_xpath(
    '/html/body/div[1]/div/main/div/div[1]/form/input[1]')
username.send_keys(rw_username)

password = driver.find_element_by_xpath(
    '/html/body/div[1]/div/main/div/div[1]/form/input[2]')
password.send_keys(rw_password)

login = driver.find_element_by_xpath(
    '/html/body/div[1]/div/main/div/div[1]/form/button')
login.click()

time.sleep(sleepTime)

driver.get('https://www.rotowire.com/daily/nhl/value-report.php?site=FanDuel')

WebDriverWait(driver, 5).until(EC.presence_of_element_located(
    (By.XPATH, '//*[@id="NHLPlayers"]/div[3]/div[2]/button[2]')))

downloadPlayerlist = driver.find_element_by_xpath(
    '//*[@id="NHLPlayers"]/div[3]/div[2]/button[2]')
downloadPlayerlist.click()

time.sleep(sleepTime)

driver.close()

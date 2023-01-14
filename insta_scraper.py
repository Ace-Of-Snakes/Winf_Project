#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import time
import pandas as pd

# used for standard options


def getOptions()->webdriver.chrome.options:
    '''Returns the options for the webdriver'''
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--incognito')
    # options.add_argument('--headless')
    # user_ agent is used to simulate a non-headless browser, to avoid access denial
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    options.add_argument('user-agent={0}'.format(user_agent))
    # options.add_argument('--no-sandbox')
    options.add_argument('--log-level=1')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # options.add_argument("--disable-3d-apis")
    return options

# startSession() is used to keep the browser open through global


def startSession()->webdriver:
    '''Starts the session and returns the driver'''
    global driver
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=getOptions())
    # initializes the user agent
    driver.execute_script("return navigator.userAgent")
    return driver

# endSession() is used to close the browser
def acceptCookies():
    '''Accepts the cookies'''
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//button[contains(text(), "Nur erforderliche Cookies erlauben")]'))).click()
    except TimeoutException:
        print('No cookies to accept')

def main():
    '''Main function'''
    # start the session
    driver = startSession()
    # open the url
    client_username = 'jonasroeber'
    driver.get(f'https://www.instagram.com/{client_username}/')
    # wait for the page to load

    # accept the cookies
    acceptCookies()
    # wait for the page to load
    time.sleep(10)
    # find the username and password fields
    # username = driver.find_element_by_name('username')
    # password = driver.find_element_by_name('password')
    # # enter the username and password
    # username.send_keys('your_username')
    # password.send_keys('your_password')

if __name__ == '__main__':
    main()
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
import regex as re
import json
# used for standard options

json_profile = {
    "username ": "",
    "biographie ": "",
    "number_of_followers ": "",
    "number_of_following ": "",
    "number_of_posts ": "",
}
def getOptions()->webdriver.chrome.options:
    '''Returns the options for the webdriver'''
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--incognito')
    # options.add_argument('--headless')
    # user_ agent is used to simulate a non-headless browser, to avoid access denial
    # user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    # options.add_argument('user-agent={0}'.format(user_agent))
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
    # driver.execute_script("return navigator.userAgent")
    return driver

# endSession() is used to close the browser
def acceptCookies():
    '''Accepts the cookies'''
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//button[contains(text(), "Nur erforderliche Cookies erlauben")]'))).click()
    except TimeoutException:
        print('No cookies to accept')

def get_number_of_posts()->int:
    '''Returns the number of posts'''
    try:
        html = driver.page_source
        time.sleep(10)
        number_regex = re.search(r'''\d+ Follower, \d+ gefolgt, \d+ Beitr''', html)
        numbers = re.findall(r'\d+', number_regex.group(0))
        number_of_followers = driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/section/ul/li[2]/button/div/span/span').text
        number_of_following = driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/section/ul/li[3]/button/div/span/span').text
        biographie = driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/section/div[3]/h1').text
        # number_of_followers = int(numbers[0])
        # number_of_following = int(numbers[1])
        number_of_posts = int(numbers[2])
        print(f'Number of followers: {number_of_followers}')
        print(f'Number of following: {number_of_following}')
        print(f'Number of posts: {number_of_posts}')
        print(f'Biographie: {biographie}')
        
        json_profile["username "] = client_username
        json_profile["biographie "] = biographie
        json_profile["number_of_followers "] = number_of_followers
        json_profile["number_of_following "] = number_of_following
        json_profile["number_of_posts "] = number_of_posts
        with open('profile.json', 'w') as f:
            json.dump(json_profile, f)

        return number_of_posts
    except TimeoutException:
        print('Number of posts not found')

def main():
    global client_username
    '''Main function'''
    # start the session
    driver = startSession()
    # open the url
    client_username = 'jonasroeber'
    driver.get(f'https://www.instagram.com/{client_username}/')
    # wait for the page to load

    # accept the cookies
    acceptCookies()
    # get the number of posts
    number_of_posts = get_number_of_posts()
    # wait for the page to load
    time.sleep(100)
    # find the username and password fields
    # username = driver.find_element_by_name('username')
    # password = driver.find_element_by_name('password')
    # # enter the username and password
    # username.send_keys('your_username')
    # password.send_keys('your_password')

if __name__ == '__main__':
    main()
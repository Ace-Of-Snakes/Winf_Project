#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import regex as re
import json
import pickle
import numpy as np
# used for standard options
button_exists = False
json_profile = {
    "username": "",
    "biographie": "",
    "number_of_followers": "",
    "number_of_following": "",
    "number_of_posts": "",
    "posts": {}
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

def startSession()->webdriver:
    '''Starts the session and returns the driver'''
    global driver
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=getOptions())
    # initializes the user agent
    # driver.execute_script("return navigator.userAgent")
    driver.set_window_position(-1000, 0)
    driver.maximize_window()
    return driver

def acceptCookies():
    '''Accepts the cookies'''
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//button[contains(text(), "Nur erforderliche Cookies erlauben")]'))).click()
    except TimeoutException:
        print('No cookies to accept')

def login()->None:
    '''Logins to the account'''
    startSession()
    # load_cookies_pickle()

    driver.get('https://www.instagram.com/accounts/login/')
    acceptCookies()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.NAME, 'username'))).send_keys('wiinfprojekt')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.NAME, 'password'))).send_keys('=:j2i#e;8Zeh8hz')
    time.sleep(1)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, '//div[contains(text(), "Anmelden")]'))).click()
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    #     (By.XPATH, '//button[contains(text(), "Informationen speichern")]'))).click()
    
    # dump_cookies_pickle()
    time.sleep(8)

    return driver

def indexer(number_of_posts: int):
    anzahl_beitraege = int(number_of_posts)
    print(anzahl_beitraege)
    if anzahl_beitraege % 3 == 0:
        i = int(anzahl_beitraege / 3)
        restbetrag = 0
    elif anzahl_beitraege % 3 != 0:
        restbetrag = anzahl_beitraege % 3
        i = (anzahl_beitraege - restbetrag)/3 + 1 
    return i, restbetrag

def iteration(number_of_posts: int):
    index,restbetrag = indexer(number_of_posts)
    print(index,restbetrag)
    data =  {}
    index = int(index)
    if int(restbetrag) == 0:
        for i in range(index):
            if  i <= index:
                for j in range(3):
                    data[f"{i+1},{j+1}"]= scrape_post_for_data(i,j)


    if int(restbetrag) != 0:
        for i in range(index):
            if  i != index:
                for j in range(3):
                    data[f"{i+1},{j+1}"]= scrape_post_for_data(i,j)
            if  i == index:
                for j in range(restbetrag):
                    data[f"{i+1},{j+1}"]= scrape_post_for_data(i,j)
    return data

def scrape_post_for_data(i,j):
    """Scrapes the post for data and returns the data as a dictionary containing description, likes, comments, hashtags and mentions"""
    global client_username, button_exists
    i = int(i)
    j = int(j)
    print(i+1,j+1)
    if button_exists:
        try:
            next_button = "/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[1]/div/div/div[2]/button"
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, next_button)))
            driver.find_element(By.XPATH, next_button).click()
        except Exception:
            return

    if i == 0 and j == 0:
        post_xpath= f"/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[3]/article/div[1]/div/div[{int(i+1)}]/div[{int(j+1)}]/a/div"
        # click on first post
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, post_xpath)))
        driver.find_element(By.XPATH, post_xpath).click()
        print("first condition")

    if i == 0 and j == 1:
        try:
            next_button = "/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[1]/div/div/div/button"
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, next_button)))
            driver.find_element(By.XPATH, next_button).click()
        except Exception:
            print("No next button found")
        button_exists = True

    time.sleep(3)
    like_xpath= "/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[2]/div/div/div/a/div/span"
    description_xpath = "/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div/li/div/div/div[2]/div[1]/h1"
    def return_username(index):
        return f"/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/ul[{index}]/div/li/div/div/div[2]/h3/div/div/div/a"

    def return_comment(index):
        return f"/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/ul[{index}]/div/li/div/div/div[2]/div[1]/span"
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, description_xpath)))
        # get text of xpath
        # text_element = driver.find_element(By.XPATH, kommentar_xpath)
        text ={}
        text["description"] = driver.find_element(By.XPATH, description_xpath).text
        text["comments"] = {}
        comm_number = 1
        time.sleep(3)
        all_comms_checked = False
        while all_comms_checked == False:
            try:
                username = driver.find_element(By.XPATH,return_username(comm_number)).text
                # print(username)
                comment = driver.find_element(By.XPATH, return_comment(comm_number)).text
                # print(comment)
                text["comments"][username] = comment
                comm_number += 1
            except Exception as e:
                all_comms_checked = True
                # print(e)
                pass

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, like_xpath)))
        # get number of likes
        likes = int(driver.find_element(By.XPATH, like_xpath).text)

        time.sleep(2)
        return_dict= {"likes":likes, "text":text}
        print(return_dict)
        return return_dict
    except Exception as e:
        print(e)
        return f"Beitrag {i,j} hat nicht geladen"

def get_number_of_posts()->int:
    '''Returns the number of posts'''
    try:
        time.sleep(10)

        # get number of posts through xpath
        number_of_posts = int(driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/ul/li[1]/div/span/span').text.strip())
        print(f'Number of posts: {number_of_posts}')
        
        # get number of followers through xpath
        number_of_followers = int(driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/ul/li[2]/a/div/span').text.strip())
        print(f'Number of followers: {number_of_followers}')
        
        # get number of following through xpath
        number_of_following = int(driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/ul/li[3]/a/div/span').text.strip())
        print(f'Number of following: {number_of_following}')

        # get biographie through xpath
        try:
            biographie = driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/div[3]/h1').text
            print(f'Biographie: {biographie}')
        except Exception as e:
            # print(e)
            # if it doesnt work, set biographie to "Keine Biographie"
            biographie = "Keine Biographie"
        
        # put data into json format
        json_profile["username"] = client_username
        json_profile["biographie"] = biographie
        json_profile["number_of_followers"] = number_of_followers
        json_profile["number_of_following"] = number_of_following
        json_profile["number_of_posts"] = number_of_posts

        return number_of_posts
    
    except TimeoutException as e:
        print('Number of posts not found')

def main():
    global client_username, driver
    '''Main function'''
    login()
    time.sleep(1)
    
    # open the url
    client_username = 'jonasroeber'
    driver.get(f'https://www.instagram.com/{client_username}/')

    # get the number of posts
    number_of_posts = get_number_of_posts()

    data = iteration(number_of_posts)
    # print(data)

    # put data into json
    json_profile["posts"] = data
    with open(f'{client_username}.json', 'w') as f:
        json.dump(json_profile, f)
    # close the browser
    # wait for the page to load
    time.sleep(10)
# test
if __name__ == '__main__':
    main()

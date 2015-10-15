# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 12:23:01 2015

@author: wly
"""


import logging
import os
from pathlib import Path
from requests import get
from requests_oauthlib import OAuth2
from selenium import webdriver
import re
import time

logger = logging.getLogger(__name__)


def get_tokenDict(client_id, username,password):
    
    for i in range(5):
        try:
            browser = webdriver.Firefox() 
        except:
            pass
        else:
            break
        
    for i in range(5):
        try:
            browser.get("https://api.imgur.com/oauth2/authorize?client_id="
            +client_id
            +"&response_type=token&state=APPLICATION_STATE")
        except:
            pass
        else:
            break
    time.sleep(1)    
    inputUsername = browser.find_element_by_id('username')
    inputUsername.send_keys(username)
    inputPassword = browser.find_element_by_id('password')
    inputPassword.send_keys(password)
    allow = browser.find_element_by_id('allow')
    allow.click()
    current_url = browser.current_url
    browser.close()

    tokenItemsSpans = []
    tokenItemsSpans.append(re.search(r"access_token=[a-z0-9]+",current_url).span())
    tokenItemsSpans.append(re.search(r"refresh_token=[a-z0-9]+",current_url).span())
    tokenItemsSpans.append(re.search(r"token_type=[a-z]+",current_url).span())
    tokenItemsSpans.append(re.search(r"expires_in=[0-9]+",current_url).span())
    tokenItems = [current_url[slice(*spans)].split("=") for spans in tokenItemsSpans]
    tokenDict = dict(tokenItems)
    return tokenDict
    

def get_links(client_id,tokenDict):
   auth=OAuth2(client_id=client_id,token=tokenDict)
   data = get('https://api.imgur.com/3/gallery/', auth=auth)
   jsdata=data.json()
   return map(lambda item: item['link'], jsdata['data'])

def download_link(directory, link):
   logger.info('Downloading %s', link)
   download_path = directory / os.path.basename(link)
   image=get(link).content
   with download_path.open('wb') as f:
       f.write(image)

def setup_download_dir():
   download_dir = Path('PythreadImages')
   if not download_dir.exists():
       download_dir.mkdir()
   return download_dir


 
from requests_oauthlib import OAuth1Session
import requests
from bs4 import BeautifulSoup
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time 
from datetime import date
today = date.today()
print("Today's date:", today)


def toStr(elements):
    elements = [element.text for element in elements]
    return elements

browser = webdriver.Chrome()
contest_url = 'https://kenkoooo.com/atcoder/#/contest/recent'
browser.get(contest_url)
elements = browser.find_elements(By.TAG_NAME, "h2")
elements = toStr(elements)
print(elements)

# res = requests.get("https://kenkoooo.com/atcoder/#/contest/recent") #サイトマップにアクセスしている
# res.raise_for_status()
# soup = BeautifulSoup(res.text, "html.parser") #アクセスして、そのHTMLを文字情報として取得
# print(soup.text)
# links = [] #サイトマップに記載されているURLを格納するための空のリスト
# elems = soup.select("h2") #サイトマップの中で、URLを取得したい要素を指定
# for elem in elems: #取得した要素for文で一つずつ検証していく
#     print(elem)

# for url in soup.find_all('h2'): #取得した要素for文で一つずつ検証していく
#     # url.get = url.get('href')
#     print(url)
browser.quit()
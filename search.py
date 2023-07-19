from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time 
from bs4 import BeautifulSoup
from datetime import date
import re
from test import tweet

today = date.today()
print("Today's date:", today)

options = Options()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--headless")
browser = webdriver.Chrome(options=options)
virtual_contests_url = 'https://kenkoooo.com/atcoder/#/contest/recent/'
browser.get(virtual_contests_url)
elements = browser.find_elements(By.TAG_NAME, "*")

# pattern = r"[Tt][Uu][Aa][Tt]"
pattern = r"[A][B][C]"
notable_contest = set()

st = set()
for element in elements:  
    if element is None: continue
    try:
        innerHTML = element.get_attribute("outerHTML")
    except:
        print("error")

    if st.__contains__(innerHTML) : continue
    if innerHTML is None: continue
    st.add(innerHTML)
    soup = BeautifulSoup(innerHTML, "html.parser")
    tr = soup.find_all("tr")

    for t in tr:
        a = t.find("a")
        if a:
            url = a.get("href")
            title = a.getText().replace("Public ", "")
        if(len(t.find_all("div")) < 3) : continue    
        [mode, start, end, *remains] = t.find_all("div")

        text = t.getText()

        if re.search(pattern, text):
            contest_url = 'https://kenkoooo.com/atcoder/'+url
            notable_contest.add((title, start.text, end.text, contest_url))

try :
    print(notable_contest)
    [title, start, end, contest_url] = notable_contest.pop()

    # tweet(f"test: コンテストのお知らせ -> {title} {contest_url}\
    # ※これはAPIを使った自動ツイートです\
    # #AtCoderProblems")
except :
    print("error")

browser.quit()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time 
from bs4 import BeautifulSoup
from datetime import date
today = date.today()
print("Today's date:", today)


def toStr(elements):
    elements = [element.text for element in elements]
    return elements

options = Options()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--headless")
browser = webdriver.Chrome(options=options)
# contest_url = 'https://www.yahoo.co.jp/'
contest_url = 'https://kenkoooo.com/atcoder/#/contest/recent/'
browser.get(contest_url)
elements = browser.find_elements(By.TAG_NAME, "h2")
elements = toStr(elements)
print(elements)
elements = browser.find_elements(By.CSS_SELECTOR, "*")
# 要素の数を表示
print(len(elements))
for element in elements:
    if element is None: continue
    innerHTML = element.get_attribute("innerHTML")
    # BeautifulSoupでinnerHTMLからaタグの要素をすべて取得
    if innerHTML is None: continue
    soup = BeautifulSoup(innerHTML, "html.parser")
    links = soup.find_all("a")
    tds = soup.find_all("td")
    if len(tds) is not 0:
        print(tds)
        # print("\n")
        url = ""
        contest_date = ""
        result = False
        for i in range(len(tds)):
            if tds[i] is not None:
                if i==0 :
                    a = tds[i].find("a")
                    if a:
                        result |= True
                        url = a.get("href")
                        # print(a)
                        print("☆ URL: ", url, "☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆")
                        # print("☆ tds[0]: ", tds[i], "☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆")
                if i==3 :
                    result |= True
                    contest_date = tds[i].getText()
        if result :
            print("TTTTTTTTTTTT: ", "https://kenkoooo.com/atcoder/"+url, contest_date)
    
        print("#######################################################\n")


browser.quit()
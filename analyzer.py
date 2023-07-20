from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time 
from bs4 import BeautifulSoup
from datetime import datetime
import re
from test import tweet
from enum import Enum

class State(Enum):
    RECENT = 1
    UPCOMING_TODAY = 2
    UPCOMING_FUTURE = 3
    RUNNING = 4

today = datetime.today()
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



def getContestState(start, end):
    s = datetime.strptime(start, '%Y-%m-%d %H:%M:%S (%a)')
    e = datetime.strptime(end, '%Y-%m-%d %H:%M:%S (%a)')
    now = datetime.now()
    print(now, ": [", s, ", ", e, "]")

    # 比較して結果を返す
    if s > now and s.day == now.day:
        return State.UPCOMING_TODAY
    elif s > now :
        return State.UPCOMING_FUTURE
    elif e < now :
        return State.RECENT
    else :
        return State.RUNNING    
    
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

runningContests = set()
upcomingContests = set()  
recentContests = set()

try :
    for contest in notable_contest:
        [title, start, end, contest_url] = contest
        # print(start, end, type(start), type(end))
        print(getContestState(start, end), contest)
        if getContestState(start, end) == State.UPCOMING_TODAY:
            upcomingContests.add(contest)

    while len(notable_contest) > 1:
        [title, start, end, contest_url] = notable_contest.pop()
        notable_contest.pop()
except :
    print("search error")


text = ""
for i in upcomingContests:
    [title, start, end, contest_url] = i
    tmp = title + " " + start + " " + contest_url + "\n"
    if i == 0:
        text = tmp
    if len(tmp) > 110 :
        tweet(f"[本日開催のバーチャルコンテスト]\n{text}#AtCoderProblems")
        text = ""
    text += tmp 
# tweet(f"test: コンテストのお知らせ ->\n {title} {start} {contest_url}\
#     ※これはAPIを使った自動ツイートです\
#     #AtCoderProblems")


browser.quit()
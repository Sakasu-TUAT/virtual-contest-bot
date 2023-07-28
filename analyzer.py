from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
from enum import Enum
from contests import State, Contests
from driver import Scraper

today = datetime.today()
print("Today's date:", today)
scraper = Scraper()
elements = scraper.scraping()

print(elements[0].text)
# pattern = r"(TUAT|ABC|ARC|AGC)"
# pattern = re.compile(r"(TUAT|ABC)", re.IGNORECASE)
notable_contest = set()

def getContestState(start, end):
    s = datetime.strptime(start, '%Y-%m-%d %H:%M:%S (%a)')
    e = datetime.strptime(end, '%Y-%m-%d %H:%M:%S (%a)')
    now = datetime.now()
    # print(now, ": [", s, ", ", e, "]")
    if timedelta(minutes=0) <= s - now <= timedelta(minutes=10):
        return State.START_ALARM
    elif timedelta(minutes=0) <= now - e <= timedelta(minutes=10):
        return State.END_ALARM
    elif s > now and s.day == now.day:
        return State.UPCOMING_TODAY
    elif s > now :
        return State.UPCOMING_FUTURE
    elif e < now :
        return State.RECENT
    else :
        return State.RUNNING    
    
st = set()
for element in elements:  
    innerHTML = ""
    if element is None: continue
    try:
        innerHTML = element.get_attribute("outerHTML")
    except Exception as e:
        print("tweet error:", e)   

    if st.__contains__(innerHTML) : continue
    if innerHTML is None: continue
    st.add(innerHTML)
    soup = BeautifulSoup(innerHTML, "html.parser")
    tr = soup.find_all("tr")

    url = ""
    title = ""
    for t in tr:
        a = t.find("a")
        if a:
            url = a.get("href")
            title = a.getText().replace("Public ", "")
        else:
            continue
        if(len(t.find_all("div")) < 3) : continue    
        [mode, start, end, *remains] = t.find_all("div")

        text = t.getText()

        # if re.search(pattern, text):
        contest_url = 'https://kenkoooo.com/atcoder/'+url
        notable_contest.add((title, start.text, end.text, contest_url))
        
try :
    for contest in notable_contest:
        [title, start, end, contest_url] = contest
        res = getContestState(start, end)
        targetContest = Contests[res]
        targetContest.add_contest(contest)

    while len(notable_contest) > 1:
        [title, start, end, contest_url] = notable_contest.pop()
        notable_contest.pop()

except :
    print("search error")

cnt = 0
for [state, con] in Contests.items():
    # if state in (State.RECENT, State.RUNNING, State.UPCOMING_FUTURE) : continue
    # if state is not State.UPCOMING_TODAY : continue
    
    if state not in (State.START_ALARM, State.END_ALARM, State.UPCOMING_TODAY) : continue
    try: con.executeTweet() 
    except Exception as e: 
        print("tweet error:", e)

scraper.quit()
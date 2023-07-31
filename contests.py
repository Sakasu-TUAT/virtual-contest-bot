from enum import Enum
from abc import ABC, abstractmethod
from test import tweet

import time 

class State(Enum):
    RECENT = 1
    UPCOMING_TODAY = 2
    START_ALARM_TEN_MINUTES = 3
    START_ALARM_THIRTY_MINUTES = 4
    START_ALARM_AN_HOUR = 5
    END_ALARM = 6
    UPCOMING_FUTURE = 7
    RUNNING = 8

class BaseContest(ABC):
    def __init__(self):
        self.__contests = set()

    def add_contest(self, contest):
        self.__contests.add(contest)

    def get_contests(self):
        return self.__contests
    
    def printContest(self):
        for contest in self.__contests:
            print(contest)

    def tweetContest(self, header): 
        text=""
        for i in self.__contests:
            # if len(text)*2 > 280:
            [title, start_row, end_row, contest_url] = i
            start = start_row.replace("2023-", "")
            end = end_row.replace("2023-", "")
            text =  header+"\n"\
                    +"■━━━━━━━━━━━━━━━━□\n "\
                    +title+"\n"+         \
                    "□━━━━━━━━━━━━━━━━■\n"\
                    + "・" + start + "~" + end + "\n・"+contest_url + "\n"
            print(text)
            time.sleep(20)
            tweet(f"{text}\n#AtCoderProblems")
            
            # text =header+\
            # "\n◎ "+title+"\n・" + start + "~" + end + "\n・"+contest_url + "\n"\
            # + "\n◎ "+title+"\n・" + start + "~" + end + "\n・"+contest_url + "\n"
            # print(text)
            # print("len: ",  len(text) - len(contest_url) + 44)
            
    @abstractmethod
    def executeTweet(self):
        pass

class RecentContest(BaseContest):
    def executeTweet(self):
        self.tweetContest("【 過去 の バチャ 】")

class UpcomingTodayContest(BaseContest):
    def executeTweet(self):
        self.tweetContest("【 本日開催 の バチャ 】")

class StartingContestTenMinutes(BaseContest):
    def executeTweet(self):
        self.tweetContest("【 10分以内 に 開催予定! 】")

class StartingContestThirtyMinutes(BaseContest):
    def executeTweet(self):
        self.tweetContest("【 30分以内 に 開催予定! 】")

class StartingContestAnHour(BaseContest):
    def executeTweet(self):
        self.tweetContest("【 1時間以内 に 開催予定! 】")

class FinishedContest(BaseContest):
    def executeTweet(self):
        self.tweetContest("【 バチャ 結果 】")

class UpcomingFutureContest(BaseContest):
    def executeTweet(self):
        self.tweetContest("【 明日以降 の バチャ 】")

class RunningContest(BaseContest):
    def executeTweet(self):
        self.tweetContest("【 現在進行中 の バチャ 】")

Contests = {
    State.RECENT: RecentContest(),
    State.UPCOMING_TODAY: UpcomingTodayContest(),
    State.START_ALARM_TEN_MINUTES: StartingContestTenMinutes(),
    State.START_ALARM_THIRTY_MINUTES: StartingContestThirtyMinutes(),
    State.START_ALARM_AN_HOUR: StartingContestAnHour(),
    State.END_ALARM: FinishedContest(),
    State.UPCOMING_FUTURE: UpcomingFutureContest(),
    State.RUNNING: RunningContest(),
}
           
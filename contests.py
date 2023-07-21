from enum import Enum
from abc import ABC, abstractmethod
from test import tweet
import time 

class State(Enum):
    RECENT = 1
    UPCOMING_TODAY = 2
    START_ALARM = 3
    END_ALARM = 4
    UPCOMING_FUTURE = 5
    RUNNING = 6

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
        for i in self.__contests:
            [title, start, end, contest_url] = i
            text = title + " " + start + "~" + end + contest_url + "\n"
            tweet(f"{header}\n{text}#AtCoderProblems")
            time.sleep(10)
            
    @abstractmethod
    def executeTweet(self):
        pass

class RecentContest(BaseContest):
    def executeTweet(self):
        self.tweetContest("【 過去のバチャ 】")

class UpcomingTodayContest(BaseContest):
    def executeTweet(self):
        self.tweetContest("【 本日開催のバチャ 】")

class StartingContest(BaseContest):
    def executeTweet(self):
        self.tweetContest("【 10分以内に開催予定! 】")

class FinishedContest(BaseContest):
    def executeTweet(self):
        self.tweetContest("【 バチャ結果 】")

class UpcomingFutureContest(BaseContest):
    def executeTweet(self):
        self.tweetContest("【 来るべきバチャ 】")

class RunningContest(BaseContest):
    def executeTweet(self):
        self.tweetContest("【 現在進行中のバチャ 】")

Contests = {
    State.RECENT: RecentContest(),
    State.UPCOMING_TODAY: UpcomingTodayContest(),
    State.START_ALARM: StartingContest(),
    State.END_ALARM: FinishedContest(),
    State.UPCOMING_FUTURE: UpcomingFutureContest(),
    State.RUNNING: RunningContest(),
}
           
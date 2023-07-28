from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import tweepy
from selenium.webdriver.chrome.service import Service

# .envファイルのパスを指定して読み込み
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# 環境変数の値を取得
def tweet(message):
    client = tweepy.Client(
        consumer_key = os.getenv('TWITTER_API_KEY'),
        consumer_secret = os.getenv('TWITTER_API_SECRET'),
        access_token = os.getenv('ACCESS_TOKEN'),
        access_token_secret = os.getenv('ACCESS_TOKEN_SECRET'),
    )
    client.create_tweet(text = message)


# driver_path = '/app/.chromedriver/bin/chromedriver' #heroku用
driver_path = '/usr/local/bin/chromedriver' #ローカル用
service = Service(driver_path)

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--remote-debugging-port=9222')
browser = webdriver.Chrome(options=options, service=service)
# browser = webdriver.Chrome(options=options) #ローカル用
contest_url = 'https://kenkoooo.com/atcoder/#/contest/recent'


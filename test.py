from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time 
import os
import tweepy

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


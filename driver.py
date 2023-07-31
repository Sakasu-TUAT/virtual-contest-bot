import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class Scraper:

    def __init__(self):
        # ドライバーセッティング
        self.driver = webdriver.Chrome(
            options=self.settingChromeOptions(),
            # service=Service('/usr/local/bin/chromedriver')
            service=Service('/app/.chromedriver/bin/chromedriver')
        )    

    def scraping(self):
        virtual_contests_url = 'https://kenkoooo.com/atcoder/#/contest/recent/'
        self.driver.get(virtual_contests_url)
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "*")))
        elements = self.driver.find_elements(By.TAG_NAME, "*")
        return elements
    
    def quit(self):
        self.driver.quit()

    @classmethod
    def settingChromeOptions(cls):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--hide-scrollbars")
        chrome_options.add_argument("--enable-logging")
        chrome_options.add_argument("--log-level=0")
        chrome_options.add_argument("--v=99")
        chrome_options.add_argument("--single-process")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--disable-dev-shm-usage")

        print("get driver")
        return chrome_options

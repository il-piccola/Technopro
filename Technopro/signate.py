import os
import datetime
import shutil
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from settings import *

def getSignateScore() :
    score = 0
    driver = getDriver()
    soup = getSoup(driver)
    score = getScore(soup)
    writeProgress(9)
    return score

def getDriver() :
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome('chromedriver', options=options)

# SIGNATEにログインして投稿結果一覧を取得
def getSoup(driver) :
    driver.get("https://signate.jp/login")
    driver.find_element(By.NAME, "encrypted_email_bidx").send_keys(EMAIL)
    writeProgress(1)
    sleep(1)
    writeProgress(2)
    sleep(1)
    writeProgress(3)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    sleep(1)
    writeProgress(4)
    sleep(1)
    writeProgress(5)
    driver.find_element(By.ID, "login_submit").send_keys(Keys.ENTER)
    sleep(1)
    writeProgress(6)
    driver.get(URL)
    writeProgress(7)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    writeProgress(8)
    return soup

# SIGNATEの最新スコアを取得
def getScore(soup) :
    table = soup.find(id="submissionTable")
    tr = table.find_all("tr")[1]
    return float(tr.find_all("td")[2].text.replace(' ', ''))

# ベストスコアファイル更新
def writeBestScore(score) :
    bestscore_path = os.path.join(WORKDIR, BESTSCORE_FILE)
    with open(bestscore_path, mode='w') as f :
        f.write(str(score))

# 進捗ファイル更新
def writeProgress(n) :
    progress_path = os.path.join(WORKDIR, PROGRESS_FILE)
    with open(progress_path, mode='w') as f :
        f.write(str(n))
    return

timestr = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S')
basename = os.path.splitext(os.path.basename(SUBMISSION_FILE))[0]

score = getSignateScore()
writeBestScore(score)

os.remove(os.path.join(WORKDIR, PROGRESS_FILE))

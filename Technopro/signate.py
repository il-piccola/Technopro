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
    progress = 0
    for i in range(10) :
        sleep(1)
        progress = progress + 1
        writeProgress(progress)
    score = 100.00
    os.remove(os.path.join(WORKDIR, PROGRESS_FILE))
    return score

def writeProgress(n) :
    progress_path = os.path.join(WORKDIR, PROGRESS_FILE)
    with open(progress_path, mode='w') as f :
        f.write(str(n))
    return

timestr = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S')
basename = os.path.splitext(os.path.basename(SUBMISSION_FILE))[0]

# options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')

# driver = webdriver.Chrome('chromedriver', options=options)

# # SIGNATEにログインして投稿結果一覧を取得
# driver.get("https://signate.jp/login")
# driver.find_element(By.NAME, "encrypted_email_bidx").send_keys(EMAIL)
# sleep(3)
# driver.find_element(By.NAME, "password").send_keys(PASSWORD)
# sleep(3)
# driver.find_element(By.ID, "login_submit").send_keys(Keys.ENTER)
# driver.get(URL)
# soup = BeautifulSoup(driver.page_source, 'lxml')

# # SIGNATEの最新スコアを取得
# table = soup.find(id="submissionTable")
# tr = table.find_all("tr")[1]
# score = float(tr.find_all("td")[2].text.replace(' ', ''))

score = getSignateScore()

bestscore_path = os.path.join(WORKDIR, BESTSCORE_FILE)
with open(bestscore_path, mode='w') as f :
    f.write(str(score))

import os
import datetime
import pandas as pd
from subprocess import Popen, PIPE
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from settings import *
from progress_s import *

# SIGNATEの投稿結果を取得
def getSignateResult(timestr) :
    newtimestr = ''
    score = 0
    i = 10
    driver = getDriver()
    soup = getSoup(driver)
    row = getRow(soup)
    newtimestr = getTime(row)
    score = 0
    writeProgress(i)
    print('time:', timestr, newtimestr, i)
    while timestr == newtimestr :
        i = i + 0.3
        row = getRow(soup)
        newtimestr = getTime(row)
        writeProgress(i)
        print('time:', timestr, newtimestr, i)
        sleep(10)
        soup = getSoup(driver)
        score = getScore(row)
    writeProgress(80, score=score)
    return score, newtimestr

# SIGNATEにログインして投稿結果一覧を取得
def getDriver() :
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome('chromedriver', options=options)
    driver.get("https://signate.jp/login")
    driver.find_element(By.NAME, "encrypted_email_bidx").send_keys(EMAIL)
    sleep(2)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    sleep(2)
    driver.find_element(By.ID, "login_submit").send_keys(Keys.ENTER)
    sleep(1)
    return driver

# SIGNATEの投稿結果ページを取得
def getSoup(driver) :
    driver.get(URL)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return soup

# SIGNATEの最新投稿結果を取得
def getRow(soup) :
    table = soup.find(id="submissionTable")
    return table.find_all("tr")[1]

# SIGNATEの最新投稿時刻を取得
def getTime(row) :
    s = row.find_all("td")[4].text
    return s

# SIGNATEの最新スコアを取得
def getScore(row) :
    s = row.find_all("td")[2].text.replace(' ', '')
    f = convertFloat(s)
    return f

# アップロードファイルをSIGNATEに投稿
def submitSignate(timestr_now) :
    submission_path = os.path.join(WORKDIR, SUBMISSION_FILE)
    df_in = pd.read_csv(submission_path, names=('index', 'n', 'e'))
    df_out = makeSubmissionDF(df_in)
    submission_out = makeSubmissionFile(df_out, timestr_now)
    submission_out = 'submission_titanic01.tsv'    # タイタニック投稿ファイル
    submitFile(submission_out)
    return

# 投稿ファイルの編集
def makeSubmissionDF(df_in) :
    df_out = df_in.copy()
    writeProgress(90)
    return df_out

# SIGNATE投稿ファイルを作成
def makeSubmissionFile(df_out, timestr_now) :
    basename = os.path.splitext(os.path.basename(SUBMISSION_FILE))[0]
    submission_out = timestr_now + '_' + basename + '.csv'
    outfile_path = os.path.join(WORKDIR, submission_out)
    df_out.to_csv(outfile_path, header=False, index=False)
    writeProgress(95, submission_file=submission_out)
    return submission_out

# SIGNATEに投稿
def submitFile(submission_out) :
    writeProgress(98)
    outfile_path = os.path.join(WORKDIR, submission_out)
    submit_com = 'signate submit --competition-id=' + str(COMPETITION_ID) + ' ' + outfile_path
    proc = Popen(submit_com, shell=True, stdout=PIPE, stderr=PIPE, text=True)
    writeProgressInfo(str(proc))
    writeProgress(99)
    return

# ベストスコアファイル更新
def writeBestScore(score) :
    bestscore = 0
    bestscore_path = os.path.join(WORKDIR, BESTSCORE_FILE)
    if os.path.exists(bestscore_path) :
        with open(bestscore_path) as f :
            s = f.read()
            bestscore = convertFloat(s)
    if score > bestscore :
        with open(bestscore_path, mode='w') as f :
            f.write(str(score))
    return

# 検索完了リストファイル更新
def writeWplistfin() :
    wplist = [getProgressName() + ',' + str(score) + ',' + '34.56' + ',' + '123.45']
    wplistfin_path = os.path.join(WORKDIR, WPLISTFIN_FILE)
    if os.path.exists(wplistfin_path) :
        with open(wplistfin_path) as f :
            for line in f :
                wplist.append(line)
    with open(wplistfin_path, mode='w') as f :
        f.write('\n'.join(wplist))
    return

score = 0
timestr = ''

score, timestr = getSignateResult(timestr)
for i in range(5) :
    timestr_now = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S')
    writeProgress(89)
    submitSignate(timestr_now)
    writeProgress(1, post=i+1)
    score, timestr = getSignateResult(timestr)

writeBestScore(score)
writeWplistfin()


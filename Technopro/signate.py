import os
import shutil
import datetime
import pandas as pd
from subprocess import run, PIPE
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from settings import *
from progress_s import *
from angle import *

# SIGNATEの投稿結果を取得
def getSignateResult(timestr) :
    newtimestr = ''
    score = 0
    i = 10
    driver = getDriver()
    soup = getSoup(driver)
    row = getRow(soup)
    newtimestr = getTime(row)
    writeProgress(i)
    print('time:', timestr, newtimestr, i)
    while timestr == newtimestr :
        # sleep(10)
        sleep(1)
        i = i + 10
        soup = getSoup(driver)
        row = getRow(soup)
        newtimestr = getTime(row)
        writeProgress(i)
        print('time:', timestr, newtimestr, i)
        # ↓テストコード↓
        if i >= 80 :
            break
        # ↑テストコード↑
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
def submitSignate() :
    submission_file = getSubmissionFile()
    submission_path = os.path.join(WORKDIR, submission_file)
    df_in = pd.read_csv(submission_path, names=('index', 'n', 'e'))
    df_out = makeSubmissionDF(df_in)
    submission_out = makeSubmissionFile(df_out)
    submission_out = 'submission_titanic01.tsv'    # タイタニック投稿ファイル
    submitFile(submission_out)
    return

# 投稿ファイルの編集
def makeSubmissionDF(df_in) :
    waypoint_path = os.path.join(WORKDIR, WAYPOINT_FILE)
    df_wp = pd.read_csv(waypoint_path, names=('index', 'name'))
    index = df_wp[df_wp['name'] == getProgressName()].iat[0, 0]
    df_out = df_in.copy()
    post_num = getPostNum()
    score_list = getScoreList()
    # 各進捗フェーズの作業
    if post_num == 1 :
        # 求めたいWPの値を基準A(N37.5, E125.0)に設定
        df_out[df_out['index'] == index].iat[0, 1] = NE_A[0]
        df_out[df_out['index'] == index].iat[0, 2] = NE_A[1]
    elif post_num == 2 :
        # 基準Aの緯度を0.1ずらす(N37.6)
        df_out[df_out['index'] == index].iat[0, 1] = NE_A[0] + 0.1
        df_out[df_out['index'] == index].iat[0, 2] = NE_A[1]
    elif post_num == 3 :
        # 2点目の基準を選定
        c, l = get_second_standard(score_list[1], score_list[2])
        # 求めたいWPの値を基準に設定
        df_out[df_out['index'] == index].iat[0, 1] = l[0]
        df_out[df_out['index'] == index].iat[0, 2] = l[1]
    elif post_num == 4 :
        # 2点目の基準を選定
        c, l = get_second_standard(score_list[1], score_list[2])
        # 緯度を0.1ずらす(N37.6)
        df_out[df_out['index'] == index].iat[0, 1] = l[0] + 0.1
        df_out[df_out['index'] == index].iat[0, 2] = l[1]
    elif post_num == 5 :
        # 基準1(基準A)の角度を求める
        angle_1 = get_angle('A', score_list[1], score_list[2])
        # 2点目の基準を選定
        c, l = get_second_standard(score_list[1], score_list[2])
        # 基準2の角度を求める
        angle_2 = get_angle(c, score_list[3], score_list[4])
        # 2点の基準の角度からWPの座標を求める
        X, Y = find_wp_from_stAngle("A", angle_1, c, angle_2)
        df_out[df_out['index'] == index].iat[0, 1] = Y
        df_out[df_out['index'] == index].iat[0, 2] = X
    writeProgress(90)
    return df_out

# 2点目の基準を選定
def get_second_standard(score1, score2) :
    # 基準Aからの角度を求める
    angle = get_angle('A', score1, score2)
    # 基準Aの角度から2点目の基準を選定
    c = 'C'
    l = NE_C
    if angle >= 0 and angle <= 20 :
        c = 'D'
        l = NE_D
    return c, l

# 角度を求める
def get_angle(c, score1, score2) :
    # 2回の投稿結果の差分Δdを求める
    delta_d = score2 - score1
    # Δdの値より角度を求める
    angle = None
    if c == 'A' :
        angle = find_wp_A_angle(delta_d)
    elif c == 'B' :
        angle = find_wp_B_angle(delta_d)
    elif c == 'C' :
        angle = find_wp_C_angle(delta_d)
    elif c == 'D' :
        angle = find_wp_D_angle(delta_d)
    return angle

# SIGNATE投稿ファイルを作成
def makeSubmissionFile(df_out) :
    timestr_now = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S')
    basename = os.path.splitext(os.path.basename(SUBMISSION_FILE))[0]
    submission_out = timestr_now + '_' + basename + '.csv'
    outfile_path = os.path.join(WORKDIR, submission_out)
    df_out.to_csv(outfile_path, header=False, index=False)
    writeProgress(95, submission_file=submission_out)
    return submission_out

# SIGNATEに投稿
def submitFile(submission_out) :
    outfile_path = os.path.join(WORKDIR, submission_out)
    submit_com = 'signate submit --competition-id=' + str(COMPETITION_ID) + ' ' + outfile_path
    writeProgressInfo(submit_com)
    # proc = run(submit_com, shell=True, stdout=PIPE, stderr=PIPE, text=True)
    # writeProgressInfo(str(proc.stdout))
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
    ret = bestscore
    if score > bestscore :
        with open(bestscore_path, mode='w') as f :
            f.write(str(score))
        ret = score
    return ret

# 基準投稿ファイル更新
def copySubmissionFile(basetimestr) :
    basename = os.path.splitext(os.path.basename(SUBMISSION_FILE))[0]
    backup_file = basename + '_bak_' + basetimestr + '.csv'
    print(backup_file)
    shutil.move(os.path.join(WORKDIR, SUBMISSION_FILE), os.path.join(BACKUPDIR, backup_file))
    shutil.copy2(os.path.join(WORKDIR, getSubmissionFile()), os.path.join(WORKDIR, SUBMISSION_FILE))

# 投稿ファイルバックアップ
def backupSubmissionFile(basetimestr) :
    backup_dir = os.path.join(BACKUPDIR, basetimestr)
    os.makedirs(backup_dir, exist_ok=True)
    submission_list = getSubmissionFiles()
    for file in submission_list :
        if file != SUBMISSION_FILE :
            filepath = os.path.join(WORKDIR, file)
            if os.path.exists(filepath) :
                shutil.move(filepath, backup_dir)
    return backup_dir

# 検索完了リストファイル更新
def writeWplistfin() :
    wplist = [getProgressName() + ',' + str(score) + ',' + '34.56' + ',' + '123.45']
    wplistfin_path = os.path.join(WORKDIR, WPLISTFIN_FILE)
    if os.path.exists(wplistfin_path) :
        with open(wplistfin_path) as f :
            for line in f :
                wplist.append(line.strip())
    with open(wplistfin_path, mode='w') as f :
        f.write('\n'.join(wplist))
    return

score = 0
timestr = ''
basetimestr = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S')

score, timestr = getSignateResult(timestr)
for i in range(5) :
    submitSignate()
    writeProgress(1, post=i+1)
    score, timestr = getSignateResult(timestr)

bestscore =  writeBestScore(score)
writeWplistfin()
if bestscore >= score :
    copySubmissionFile(basetimestr)
backup_dir = backupSubmissionFile(basetimestr)

writeProgress(100, backup_dir=backup_dir)

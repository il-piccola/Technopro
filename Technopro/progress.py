import os
import datetime
import shutil
from decimal import Decimal
from .settings import *

progress_path = os.path.join(WORKDIR, PROGRESS_FILE)
progressinfo_path = os.path.join(WORKDIR, PROGRESSINFO_FILE)

# ウェイポイント名取得
def getProgressName() :
    ret = ''
    l = readProgress()
    if len(l) >= 1 :
        ret = l[0]
    return ret

# 進捗状況取得
def getProgress() :
    ret = 0
    l = readProgress()
    if len(l) >= 2 :
        ret = float(l[1])
    return ret

# 投稿回数取得
def getPostNum() :
    ret = 0
    l = readProgress()
    if len(l) >= 3 :
        ret = int(l[2])
    return ret

# 投稿ファイルリスト取得
def getSubmissionFiles() :
    ret = SUBMISSION_FILE
    l = readProgress()
    if len(l) >= 4 :
        ret = l[3].split(',')
    return ret

# 最新投稿ファイル名取得
def getSubmissionFile() :
    return getSubmissionFiles()[-1]

# バックアップディレクトリパス取得
def getBackupDir() :
    ret = ''
    l = readProgress()
    if len(l) >= 6 :
        ret = l[5]
    return ret

# 進捗ファイル読込
def readProgress() :
    ret = []
    if os.path.exists(progress_path) :
        with open(progress_path) as f :
            ret = [s.strip() for s in f.readlines()]
    return ret

# 進捗ファイル更新
def writeProgress(n, name='', post=0, submission_file='', score=0, backup_dir='') :
    l = readProgress()
    if len(l) <= 0 :
        l = []
        l.append(name)
        l.append(str(n))
        l.append(str(post))
        l.append(submission_file)
    else :
        if name != '' :
            l[0] = name
        l[1] = str(Decimal(str(n)).quantize(Decimal('.01')))
        if post > 0 :
            l[2] = str(post)
        if submission_file != '' :
            if len(l) > 3 :
                if len(l[3]) <= 0 :
                    l[3] = submission_file
                else :
                    l[3] = l[3] + ',' + submission_file
            else :
                l.append(submission_file)
        if score > 0 :
            if len(l) >= 5 :
                if len(l[4]) <= 0 :
                    l[4] = str(score)
                else :
                    l[4] = l[4] + ',' + str(score)
            else :
                l.append(str(score))
        if backup_dir != '' :
            if len(l) >= 6 :
                l[5] = backup_dir
            else :
                l.append(backup_dir)
    with open(progress_path, mode='w') as f :
        f.write('\n'.join(l))
    return

# 進捗ファイルバックアップ
def backupProgress() :
    backup_dir = getBackupDir()
    if os.path.exists(backup_dir) :
        if os.path.exists(progress_path) :
            shutil.move(progress_path, backup_dir)
        if os.path.exists(progressinfo_path) :
            shutil.move(progressinfo_path, backup_dir)

def convertFloat(s):
    ret = -1
    try:
        ret = float(s)
    except ValueError :
        return ret
    else :
        return ret

# バッチ情報ファイル書き込み
def writeProgressInfo(s) :
    d = datetime.datetime.strftime(datetime.datetime.now(), '[%Y/%m/%d %H:%M:%S] ')
    with open(progressinfo_path, mode='a') as f :
        f.write(d + s + '\n')
import os
from .settings import *

progress_path = os.path.join(WORKDIR, PROGRESS_FILE)

# ウェイポイント名取得
def getProgressName() :
    return readProgress()[0]

# 進捗状況取得
def getProgress() :
    return readProgress()[1]

# 進捗ファイル更新
def writeProgress(n, name='') :
    if name == '' :
        name = getProgressName()
    s = name + ',' + str(n)
    with open(progress_path, mode='w') as f :
        f.write(s)
    return

# 進捗ファイル読込
def readProgress() :
    ret = ['', 0]
    if os.path.exists(progress_path) :
        with open(progress_path) as f :
            s = f.read()
            ret = s.split(',')
            ret[1] = convertFloat(ret[1])
    return ret

# 進捗ファイル削除
def deleteProgress() :
    if os.path.exists(progress_path) :
        os.remove(progress_path)

def convertFloat(s):
    ret = -1
    try:
        ret = float(s)
    except ValueError :
        return ret
    else :
        return ret

import os
import pandas as pd
from subprocess import Popen, PIPE
from django.shortcuts import render, redirect
from django.views.decorators.clickjacking import xframe_options_exempt
from .settings import *
from .forms import *

def getParams() :
    return {
        'msg' : 'ボタン押下で座標計算およびSIGNATEスコアを取得します',
        'reload' : False,
        'progress' : 0,
        'anime' : 'progress-bar-animated',
        'wplistfin' : getFinList()
    }

def upload(request) :
    params = getParams()
    params['msg'] = '最新のSIGNATE投稿ファイルをアップロードしてください'
    params['uploadform'] = uploadForm()
    if request.POST :
        uploadform = uploadForm(request.POST, request.FILES)
        if uploadform.is_valid() :
            submission_path = os.path.join(WORKDIR, SUBMISSION_FILE)
            with open(submission_path, 'wb') as f:
                f.write(request.FILES['file'].read())
        return redirect('index')
    return render(request, 'Technopro/index.html', params)

def index(request) :
    if not isExistsSubmission() :
        return redirect('upload')
    params = getParams()
    params['indexform'] = indexForm()
    if request.POST :
        indexform = indexForm(data=request.POST)
        if indexform.is_valid() :
            waypoint = indexform.cleaned_data['waypoint']
            params['msg'] = '座標計算中です、お待ちください'
            params['reload'] = True
            params['progress'] = getProgress(waypoint)
            score = execSignate()
            if score > 0 :
                params['msg'] = 'スコアは' + str(score) + 'です'
                params['reload'] = False
                params['progress'] = 100
                params['anime'] = 'progress-bar-striped'
        params['indexform'] = indexform
    return render(request, 'Technopro/index.html', params)

def execSignate(waypoint) :
    score = -1
    process_path = os.path.join(WORKDIR, PROCESS_FILE)
    if not os.path.exists(process_path) :
        proc = Popen(SIGNATE_COM, shell=True, stdout=PIPE, stderr=PIPE, text=True)
        with open(process_path, mode='w') as f :
            f.write(SIGNATE_COM)
        return score
    bestscore_path = os.path.join(WORKDIR, BESTSCORE_FILE)
    if os.path.exists(bestscore_path) :
        with open(bestscore_path) as f :
            s = f.read()
            score = convertFloat(s)
        os.remove(bestscore_path)
        os.remove(process_path)
    return score

def getProgress() :
    ret = 0
    progress_path = os.path.join(WORKDIR, PROGRESS_FILE)
    if os.path.exists(progress_path) :
        with open(progress_path) as f :
            s = f.read()
            ret = int(convertFloat(s)*10)
    return ret

def isExistsSubmission() :
    submission_path = os.path.join(WORKDIR, SUBMISSION_FILE)
    print(submission_path)
    ret = os.path.exists(submission_path)
    print(ret)
    return ret

def getFinList() :
    ret = pd.DataFrame()
    wplistfin_path = os.path.join(WORKDIR, WPLISTFIN_FILE)
    if os.path.exists(wplistfin_path) :
        ret = pd.read_csv(wplistfin_path, header=None)
    return ret

def convertFloat(s):
    ret = -1
    try:
        ret = float(s)
    except ValueError :
        return ret
    else :
        return ret

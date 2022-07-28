import os
import pandas as pd
from subprocess import Popen, PIPE
from django.shortcuts import render, redirect
from django.views.decorators.clickjacking import xframe_options_exempt
from .settings import *
from .forms import *
from .progress import *

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
    if request.POST :
        submission_path = os.path.join(WORKDIR, SUBMISSION_FILE)
        with open(submission_path, 'wb') as f:
            f.write(request.FILES['file'].read())
        return redirect('index')
    return render(request, 'Technopro/index.html', params)

def index(request) :
    submission_path = os.path.join(WORKDIR, SUBMISSION_FILE)
    if not os.path.exists(submission_path) :
        return redirect('upload')
    params = getParams()
    progress = getProgress()
    name = getProgressName()
    if progress >= 100 :
        params['msg'] = '【' + name + '】の座標計算処理が完了しました'
        params['anime'] = 'progress-bar-striped'
        params['result'] = getWaypointFin(name=name)
        deleteProgress()
        if request.POST :
            params['indexform'] = indexForm(data=request.POST)
        else :
            params['indexform'] = indexForm()
    elif progress > 0 :
        params['msg'] = '【' + name + '】の座標を計算中です、しばらくお待ちください'
        params['reload'] = True
        if request.POST :
            params['indexform'] = indexForm(data=request.POST)
        else :
            params['indexform'] = indexForm()
    else :
        if request.POST :
            indexform = indexForm(data=request.POST)
            if indexform.is_valid() :
                waypoint = int(indexform.cleaned_data['waypoint'])
                ret = execSignate(waypoint)
                name = getWaypointName(waypoint)
                if not ret :
                    params['msg'] = '【' + name + '】の座標計算処理は完了しています'
                    params['anime'] = 'progress-bar-striped'
                    params['result'] = getWaypointFin(name=name)
                    deleteProgress()
                else :
                    params['msg'] = '【' + name + '】の座標を計算中です、しばらくお待ちください'
                    params['reload'] = True
            params['indexform'] = indexform
        else :
            params['msg'] = 'ボタン押下で座標計算およびSIGNATEスコアを取得します'
            params['indexform'] = indexForm()
    params['progress'] = progress
    return render(request, 'Technopro/index.html', params)

def execSignate(waypoint) :
    if len(getWaypointFin(index=waypoint)) > 0 :
        return False
    if getProgress() <= 0 and getPostNum() <= 0 :
        name = getWaypointName(waypoint)
        writeProgress(1, name=name, post=1, submission_file=SUBMISSION_FILE)
        proc = Popen(SIGNATE_COM, shell=True, stdout=PIPE, stderr=PIPE, text=True)
    return True

def getFinList() :
    ret = pd.DataFrame()
    wplistfin_path = os.path.join(WORKDIR, WPLISTFIN_FILE)
    if os.path.exists(wplistfin_path) :
        ret = pd.read_csv(wplistfin_path, names=('name', 'score', 'n', 'e'))
    return ret

def getWaypointFin(index=-1, name='') :
    ret = []
    df = getFinList()
    if len(name) > 0 :
        ret = df[df['name']==name].values.tolist()
        if len(ret) > 0 :
            ret = ret[0]
    elif index >= 0 :
        ret = df[df['name']==getWaypointName(index)].values.tolist()
        if len(ret) > 0 :
            ret = ret[0]
    return ret

def getWaypointName(waypoint) :
    ret = ''
    waypoint_path = os.path.join(WORKDIR, WAYPOINT_FILE)
    if os.path.exists(waypoint_path) :
        df = pd.read_csv(waypoint_path, names=('index', 'name'))
        ret = df[df['index']==waypoint].iat[0, 1]
    return ret

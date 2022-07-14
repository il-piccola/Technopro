import os
from subprocess import Popen, PIPE
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from .settings import *
from .forms import *

def index(request) :
    params = {
        'msg' : 'ボタン押下でスコアを取得します',
        'reload' : False
    }
    if request.POST :
        params['msg'] = 'スコア取得中です、お待ちください'
        params['reload'] = True
        score = execSignate()
        if score > 0 :
            params['msg'] = 'スコアは' + str(score) + 'です'
            params['reload'] = False
    return render(request, 'Technopro/index.html', params)

def execSignate() :
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

def convertFloat(s):
    ret = -1
    try:
        ret = float(s)
    except ValueError :
        return ret
    else :
        return ret

import os
from pathlib import Path
import subprocess
from subprocess import PIPE
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
    signate_path = os.path.join(Path(__file__).resolve().parent, SIGNATE_PY)
    print('signate path :', signate_path)
    if not os.path.exists(process_path) :
        proc = subprocess.Popen('python ' + signate_path, shell=True, stdout=PIPE, stderr=PIPE, text=True)
        with open(process_path, mode='w') as f :
            f.write(str(proc.stdout))
        return score
    bestscore_path = os.path.join(WORKDIR, BESTSCORE_FILE)
    if os.path.exists(bestscore_path) :
        subprocess.Popen(['python', SIGNATE_PY], stdout=PIPE, stderr=PIPE, text=True)
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

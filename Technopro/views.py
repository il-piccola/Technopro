from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from .forms import *

def index(request) :
    params = {}
    return render(request, 'Technopro/index.html', params)


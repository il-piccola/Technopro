import csv
from django import forms
from .settings import *

class indexForm(forms.Form) :
    def getWaypointList() :
        ret = []
        waypoint_path = os.path.join(WORKDIR, WAYPOINT_FILE)
        f = open(waypoint_path, encoding='utf_8')
        list = csv.reader(f)
        for row in list :
            ret.append((row[0], row[1]))
        return ret

    waypoint = forms.ChoiceField(
        choices=getWaypointList(),
        widget=forms.Select()
    )
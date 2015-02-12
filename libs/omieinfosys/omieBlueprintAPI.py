# -*- coding: utf-8 -*

from flask import Blueprint
from flask import request

omieMercadoDiario = Blueprint('verver1', __name__,url_prefix='/omieinfosys')

import datetime
import json


def jsondefaultvalues(obj):
    """jsondefaultvalues
    Helper method to the json enconder to the web page
    for now only a datetime handler is set!
    """
    if isinstance(obj,datetime.datetime):
        return obj.isoformat()
    elif isinstance(obj,float):
        return round(obj,2)
        #return format(str(round(obj,2)), '.2f'))
    else:
        return obj

@omieMercadoDiario.route('/status',methods=['GET'])
def status():
    """status

    Some basic statistics/status on the omie collections:

    Note:
        test using curl->
        curl -X POST -H "Content-Type: application/json" -d '{"day":"2014-1-1","market":"ES"}' http://localhost:5000/omieinfosys/ReportDay

    """
    
    try:
        from . import status
    except:
        return json.dumps({"Error":"No data to sent"})
    else:
        return json.dumps(status(),default=jsondefaultvalues)

@omieMercadoDiario.route('/ReportDay',methods=['GET','POST'])
def ReportDay():
    """ReportDay

    Note:
        test using curl->
        curl -X POST -H "Content-Type: application/json" -d '{"day":"2014-1-1","market":"ES"}' http://localhost:5000/omieinfosys/ReportDay

    """
    if request.method == 'GET':
        day = 'lastavailable'
        market = 'MI'
    elif request.method == 'POST':
        day = request.json['day']
        try:
            day = datetime.datetime.strptime(request.json['day'],'%Y-%m-%d %H:%M:%S %Z')
        except:
            day = datetime.datetime.strptime(request.json['day'],'%Y-%m-%d')
        market = request.json['market']
    try:
        from omieMercadoDiarioReports import ReportDay
        if day == 'lastavailable':
            day = None
        verver = dict(ReportDay(market=market,day=day).items())
    except:
        return json.dumps({"Error":"No data to sent"})
    else:
        return json.dumps(verver,default=jsondefaultvalues)


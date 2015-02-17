# -*- coding: utf-8 -*

from flask import Blueprint
from flask import request, render_template

omieMercadoDiario = Blueprint('verver1', __name__,url_prefix='/omieinfosys', template_folder="plots_templates")

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

@omieMercadoDiario.route('/PreciosHorariosUltimoDia',methods=['GET','POST'])
def ReportLastAvailableDay():
    # """ReportDay

    # Note:
    #     test using curl->
    #     curl -X POST -H "Content-Type: application/json" -d '{"day":"2014-1-1","market":"ES"}' http://localhost:5000/omieinfosys/ReportDay


    
    # """
    # if request.method == 'GET':
    #     day = 'lastavailable'
    #     market = 'MI'
    # elif request.method == 'POST':
    #     day = request.json['day']
    #     try:
    #         day = datetime.datetime.strptime(request.json['day'],'%Y-%m-%d %H:%M:%S %Z')
    #     except:
    #         day = datetime.datetime.strptime(request.json['day'],'%Y-%m-%d')
    #     market = request.json['market']
    # try:
    #     from omieMercadoDiarioReports import ReportDay
    #     if day == 'lastavailable':
    #         day = None
    #     verver = dict(ReportDay(market=market,day=day).items())
    # except:
    #     return json.dumps({"Error":"No data to sent"})
    # else:
    #     return render_template('test.html',valores=json.dumps(verver,default=jsondefaultvalues))
    
    # from nvd3 import linePlusBarChart
    # chart = linePlusBarChart(name="linePlusBarChart",
    #                      width=500, height=400, x_axis_format="%d %b %Y",
    #                      x_is_date=True,
    #                      yaxis2_format="function(d) { return d3.format(',0.3f')(d) }")

    # xdata = [1338501600000, 1345501600000, 1353501600000]
    # ydata = [6, 5, 1]
    # y2data = [0.002, 0.003, 0.004]

    # extra_serie = {"tooltip": {"y_start": "There are ", "y_end": " calls"},
    #                "date_format": "%d %b %Y %H:%S" }
    # chart.add_serie(name="Serie 1", y=ydata, x=xdata, extra=extra_serie,
    #                 bar=True)

    # extra_serie = {"tooltip": {"y_start": "There are ", "y_end": " min"}}
    # chart.add_serie(name="Serie 2", y=y2data, x=xdata, extra=extra_serie)
    # # chart.buildcontent()
    # chart.buildjschart()
    # print type(chart)
    # print chart.__dict__.keys()
    # print chart.series
    # return render_template('test.html',valores=chart.jschart)

    # Now lets try oput HighCharts:
    ## Getting necessary Data:
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
        result = dict(ReportDay(market=market,day=day).items())
    except:
        result = {"Error":"No data to sent"}

    ## Setting data to template:

    ## Possibly some dump would be helpful

    if result.has_key("Error"):
        return "no data to plot"
    else:
        return render_template('highcharts.html',precio=result['Precios'],energia=result['VolumenesMWh'],sumario=result)
# -*- coding: utf-8 -*
# 

from flask import Blueprint, Response
from flask import request, render_template, url_for, redirect

omieMercadoDiario = Blueprint('omieinfosys', __name__,url_prefix='/omieinfosys', template_folder="plots_templates")

import datetime
import json

def _decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, str):
            key = key.encode('utf-8')
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv

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
        curl -H "Content-Type: application/json" http://localhost:5000/omieinfosys/status

        test using curl->

    """
    
    try:
        from . import status
    except:
        return json.dumps({"Error":"No data to sent"})
    else:
        return json.dumps(status(),default=jsondefaultvalues)

@omieMercadoDiario.route('/updatedb',methods=['GET'])
def updatedb():
    """status

    Some basic statistics/status on the omie collections:

    Note:
        test using curl->
        curl -H "Content-Type: application/json" http://localhost:5000/omieinfosys/updatedb

        test using curl->

    """
    
    try:
        from . import updatedb
        updatedb()
    except:
        return json.dumps({"Error":"Update not executed properly. Try Again"})
    else:
        return json.dumps({"Ok":"Collections are up to date"})

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
        if day != 'lastavailable':
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

@omieMercadoDiario.route('/ReportDayTech',methods=['GET','POST'])
def ReportDayTech():
    """ReportDayTech

    Note:
        test using curl->
        curl -X POST -H "Content-Type: application/json" -d '{"day":"2014-1-1","market":"ES"}' http://localhost:5000/omieinfosys/ReportDayTech

    """
    if request.method == 'GET':
        day = 'lastavailable'
        market = 'MI'
    elif request.method == 'POST':
        day = request.json['day']
        if day != 'lastavailable':
            try:
                day = datetime.datetime.strptime(request.json['day'],'%Y-%m-%d %H:%M:%S %Z')
            except:
                day = datetime.datetime.strptime(request.json['day'],'%Y-%m-%d')
        market = request.json['market']
    try:
        from omieMercadoDiarioReports import ReportDayTecnologies
        if day == 'lastavailable':
            day = None
        verver = dict(ReportDayTecnologies(market=market,day=day).items())
    except:
        result = {"Error":"No data to sent"}
    else:
        verver['Mercado'] = market
        result = verver

    series = list()
    for key,value in result.iteritems():
        if isinstance(value,list) and 'TOTAL' not in key and 'EUR' not in key and key!='VolumenesMWh' and key!='Precios':
            series.append({'name':str(key).replace("Volumenes",""),'data':value})
        else:
            pass
    # series = [if isinstance(value,list) {'name':key,'data':value} for key,value in result.iteritems()]
    print series

    return json.dumps(result,default=jsondefaultvalues)




@omieMercadoDiario.route('/DataFileGenerator',methods=['GET'])
def DataFileGeneratorPage():
    """
    """

    return redirect(url_for('static', filename="DataFileGenerator.html"))


@omieMercadoDiario.route('/DataFileGenerator',methods=['POST'])
def DataFileGenerator():
    """DataFileGenerator

    posted data should be a json file with the keys:
    fechaini -> string in format YYYY-MM-DD
    fechafin -> string in format YYYY-MM-DD
    market string in ['MI','ES','PT']
    headerstoprocess json with format key:bool

    Note:
        test using curl->
        curl -X POST -H "Content-Type: application/json" -d '{"fechaini":"2015-1-1","fechafin":"2015-1-2","market":"ES"}' http://localhost:5000/omieinfosys/DataFileGenerator

    """
    try:
        if request.method == 'POST':
            posteddata = json.loads(request.data,object_hook=_decode_dict)
            # posteddata = request.json
            # print posteddata
            fechaini = datetime.datetime.strptime(posteddata.pop('fechaini'),'%Y-%m-%d')
            fechafin = datetime.datetime.strptime(posteddata.pop('fechafin'),'%Y-%m-%d')
            market = posteddata.pop('market')
            headerstoprocess = posteddata

        from omieDataFilesGenerators import generateOMIEwebdata
        result = generateOMIEwebdata(fechaini,fechafin,market,headerstoprocess=headerstoprocess,rewritetemp=True)
        def generate(result):
            with open(result, 'rU') as f:
              for row in f:
                 yield row
    except:
        raise
        # return json.dumps({"Error":"No data to sent"})
    else:
        # return result
        return Response(generate(result), mimetype='text/csv')


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
        from omieMercadoDiarioReports import ReportDayTecnologies
        if day == 'lastavailable':
            day = None
        result = dict(ReportDayTecnologies(market=market,day=day).items())
    except:
        result = {"Error":"No data to sent"}

    ## Setting data to template:

    ## Possibly some dump would be helpful

    if result.has_key("Error"):
        return "no data to plot"
    else:
        return render_template('ReportDay.html',
            precio=result['Precios'],
            energia=result['VolumenesMWh'],
            preciomedio=result['PrecioMedio'],
            mediaaritmetica=result['MediaAritmetica'],
            totalvolumenmwh="{0:,.2f}".format(result['TotalVolumenMWh']),
            totalvolumeneurs="{0:,.2f}".format(result['TotalVolumenEURs']),
            sumario=result)


@omieMercadoDiario.route('/TecnologiasDiarias',methods=['GET','POST'])
def ReportDayTechLastAvailableDay():
    """ReportDayTech

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
        from omieMercadoDiarioReports import ReportDayTecnologies
        if day == 'lastavailable':
            day = None
        result = dict(ReportDayTecnologies(market=market,day=day).items())
    except:
        result = {"Error":"No data to sent"}

    ## Setting data to template:
    print result
    ## Possibly some dump would be helpful
    series = list()
    for key,value in result.iteritems():
        if isinstance(value,list) and 'TOTAL' not in key and 'EUR' not in key and key!='VolumenesMWh' and key!='Precios':
            series.append({'name':str(key).replace("Volumenes",""),'data':value})
        else:
            pass
    # series = [if isinstance(value,list) {'name':key,'data':value} for key,value in result.iteritems()]
    print series
    # [{
    #         'name': 'John',
    #         'data': [5, 3, 4, 7, 2]
    #     }, {
    #         'name': 'Jane',
    #         'data': [2, 2, 3, 2, 1]
    #     }, {
    #         'name': 'Joe',
    #         'data': [3, 4, 4, 2, 5]
    #     }]

    if result.has_key("Error"):
        return "no data to plot"
    else:
        return render_template('ReportDayTech.html',
            series = series,
            precios=result['Precios'],
            energia=result['VolumenesMWh'],
            preciomedio=result['PrecioMedio'],
            mediaaritmetica=result['MediaAritmetica'],
            totalvolumenmwh=result['TotalVolumenMWh'],
            totalvolumeneurs=result['TotalVolumenEURs'],
            sumario=result)

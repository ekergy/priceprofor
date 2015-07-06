# -*- coding: utf-8 -*

from flask import Blueprint, Response
from flask import request, render_template, url_for, redirect

import omieinfosys

modellingsys = Blueprint('modellingsys', __name__,url_prefix='/modellingsys', template_folder="plots_templates")

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
    else:
        return obj

@modellingsys.route('/status',methods=['GET'])
def status():
    """status
    Some basic statistics/status on the omie collections:

    Note:
        test using curl->
        curl -H "Content-Type: application/json" http://localhost:5000/omieinfosys/status
    """
    import modellingsysDBManager 
    
    result = modellingsysDBManager.ModellingResults.lastdayaheadindb
    # print result
    tojson = dict()    
    tojson['dayahead'] = result.dayahead
    tojson['baseset'] = result.baseset
    tojson['model'] = result.model
    tojson['errormodel'] = result.errormodel
    tojson['forecasts'] = result.forecasts
     
    try:
        dummy = 1
    except:
        return json.dumps({"Error":"No data to sent"})
    else:
        return json.dumps(tojson,default=jsondefaultvalues)

@modellingsys.route('/lastforecastindb', methods=['POST'])
def lastforecastindb():
    """lastforecastindb

    Note:
    test using curl->
        sin datos
            curl -X POST -H "Content-Type: application/json" -d '{}' http://localhost:5000/modellingsys/lastforecastindb
        con datos
            curl -X POST -H "Content-Type: application/json" -d '{"dayaheadInput": "2015-06-19","modeltypeInput":"hwtes"}' http://localhost:5000/modellingsys/lastforecastindb
    """
    import modellingsysDBManager 
    import omieinfosys

    if request.json:
        dayaheadInput = datetime.datetime.strptime(request.json['dayaheadInput'],'%Y-%m-%d')
        modeltypeInput = request.json['modeltypeInput']
        results = modellingsysDBManager.ModellingResults.objects(__raw__={'dayahead': dayaheadInput,
                                                                          'model.type': modeltypeInput})
        resultsprices = omieinfosys.omieMercadoDiarioDBManager.PreciosWeb.objects(__raw__={'fecha': { '$gte': dayaheadInput,
                                                                                                      '$lte': dayaheadInput + datetime.timedelta(1) } })
        realprices = []
        for precios in resultsprices:
            for valor in precios.PreciosES:
                realprices.append(valor)
        if results:
            for element in results:
                result = element
        try:
            realpricesAUX = list()
            if len(realprices) == 0:
                realpricesAUX = [0]*48
            elif len(realprices) == 24:
                realpricesAUX = realprices + [0]*24
            elif len(realprices) == 48:
                realpricesAUX = realprices
            errorpredictions = list()
            for index in range(len(result.predictions["forecasts"])):
                if realpricesAUX[index] == 0:
                    errorpredictions.append(None)
                else:
                    errorpredictions.append(abs(result.predictions["forecasts"][index] - realpricesAUX[index]))
            tojson = dict()    
            tojson['dayahead'] = result.dayahead
            tojson['baseset'] = result.baseset
            tojson['model'] = result.model
            tojson['errormodel'] = result.errormodel
            tojson['predictions'] = result.predictions
            tojson['errorpredictions'] = errorpredictions
            tojson['realprices'] = realprices
        except:
            return json.dumps({"Error":"No data to sent"})
        else:
            return json.dumps(tojson,default=jsondefaultvalues)
    else:
        try:
            result = modellingsysDBManager.ModellingResults.lastdayaheadindb
            tojson = dict()    
            tojson['dayahead'] = result.dayahead
            tojson['baseset'] = result.baseset
            tojson['model'] = result.model
            tojson['errormodel'] = result.errormodel
            tojson['predictions'] = result.predictions
            tojson['errorpredictions'] = []
            resultsprices = omieinfosys.omieMercadoDiarioDBManager.PreciosWeb.objects(__raw__={'fecha': { '$gte': result.dayahead,
                                                                                                          '$lte': result.dayahead + datetime.timedelta(1) } })
            realprices = []
            for precios in resultsprices:
                for valor in precios.PreciosES:
                    realprices.append(valor)
            tojson['realprices'] = realprices
        except:
            return json.dumps({"Error":"No data to sent"})
        else:
            # tojson['realprices'] = realprices
            return json.dumps(tojson,default=jsondefaultvalues)

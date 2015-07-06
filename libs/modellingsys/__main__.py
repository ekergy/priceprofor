# -*- coding: utf-8 -*-

"""modelling system CLI

Usage:
modellingsys --arnn <dayahead>
modellingsys --hwtes <dayahead>
modellingsys --status
modellingsys --forecasts <dayahead> <modeltype>
modellingsys --populateforecasts <fechaini> <fechafin>

Arguments
<dayahead>                              The dayahead to perform modelling and prediction

Options:
-h --help                               Shows this help page
--arnn <dayahead>                       Use arnn method to perform modelling and construct predictions
--hwtes <dayahead>                      Use hwtes method to perform modelling and construct predictions
--status                                Check last prediction made with configured modelling
--forecasts <dayahead> <modeltype>      Check last prediction made with configured modelling

"""
import sys

from pprint import pprint
from datetime import datetime, timedelta
# importacion correcta aunque eclipse crea que es un error
from docopt import docopt

def execute_hwtes(dayaheadInput=None):
    """perform modelling and construct predictions using hwtes Method
    """
    try:
        from models import hwtes
        if dayaheadInput:
            dayaheadInput = datetime.strptime(dayaheadInput,'%Y-%m-%d')
            hwtes.mainHWTES(dayaheadInput)
        else:
            hwtes.mainHWTES()
    except:
        raise
    else:
        print ''
        # print("execute_hwtes done")
        # pprint(result)

def execute_arnn(dayaheadInput):
    """perform modelling and construct predictions using arnn Method
    """
    try:
        from models import arnn
        if dayaheadInput:
            dayaheadInput = datetime.strptime(dayaheadInput,'%Y-%m-%d')
            arnn.mainARNN(dayaheadInput)
        else:
            arnn.mainARNN()
    except:
        raise
    else:
        print ''
        # print("execute_arnn done")
        # pprint(result)

def execute_forecasts(dayaheadInput,modeltypeInput):
    """
    """
    # print "dayahead->",dayahead,type(dayahead)
    # print "modeltype->",modeltype,type(modeltype)
    dayaheadInput = datetime.strptime(dayaheadInput,'%Y-%m-%d')
    from modellingsysDBManager import ModellingResults
    # results = ModellingResults.objects(dayaheadInput=datetime(2015,6,12))
    # modeltype = 'arnn'
    results = ModellingResults.objects(__raw__={'dayahead': dayaheadInput, 'model.type': modeltypeInput})
    # results = ModellingResults.objects(model__method=modeltype)
    # results = ModellingResults.objects(model__type__=modeltype)
    if results:
    # print results
    # print type(results)
        for element in results:
            result = element
        # print result.to_json()
        # print result.dayahead
        print result.forecasts
        # print result.model['parametros']
        # print result.model['type']
        # print type(result.model['type'])
        # print result['dayahead']
        # fecha = dic[0]['dayahead']['$date']
        # ver[0].save()
        # return results

def check_status():
    """perform modelling and construct predictions using hwtes Method
    """
    result = {'arnn':{"last_dayahead":datetime(2011,1,1)},'hwtes':{"last_dayahead":datetime(2011,1,1)}}
    pprint(result)

arguments = docopt(__doc__,version="alpha")

# python -m modellingsys --hwtes "2015-01-02"
if arguments["--hwtes"]:
    if arguments["--hwtes"] == "now":
        execute_hwtes()
    else:
        execute_hwtes(arguments["--hwtes"])

# python -m modellingsys --arnn "2015-01-01"
if arguments["--arnn"]:
    if arguments["--arnn"] == "now":
        execute_arnn()
    else:
        execute_arnn(arguments["--arnn"])

if arguments["--forecasts"]:
    print execute_forecasts(arguments["--forecasts"],arguments["<modeltype>"])
    # print execute_forecasts(arguments["<dayahead>"],arguments["<modeltype>"])
    # print dayahead

if arguments["--status"]:
    check_status()

# python -m modellingsys --populateforecasts "2015-01-01" "2015-01-03"
if arguments["--populateforecasts"]:
    from models.hwtes import mainHWTES
    from models.arnn import mainARNN
    # print arguments["--populateforecasts"],arguments["<fechaini>"],arguments["<fechafin>"]
    fecha = datetime.strptime(arguments["<fechaini>"],'%Y-%m-%d')
    while fecha <= datetime.strptime(arguments["<fechafin>"],'%Y-%m-%d'):
        print fecha.date()
        try:
            try:
                mainHWTES(fecha)
            except:
                mainHWTES(fecha,retry=True)
        except:
            print "No se ha construido previsiones con hwtes para esta fecha " + str(fecha)
        notarnn = True
        iter = 0
        while (notarnn and iter<3):
            try:
                mainARNN(fecha)
            except:
                notarnn = True
                iter = iter + 1
                print "No se ha construido previsiones con arnn para esta fecha " + str(fecha)
            else:
                notarnn = False
        fecha = fecha + timedelta(1)

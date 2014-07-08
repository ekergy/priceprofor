# -*- coding: utf-8 -*-
'''
Created on 26/06/2014
@author: hmarrao@ekergy
'''

from nvd3 import lineChart, pieChart
from bottle import route, template
from dbpreciosesmanager import preciosDiarios, tecnologiasDiarias
from datetime import datetime, timedelta
from copy import copy

@route('/')
def home():
    '''
    '''
    return template('home.html')

@route('/uikitTemplate.html')
def home2():
    '''
    '''
    return template('uikitTemplate.html')

@route('/multiBar.html')
def home3():
    '''
    '''
    return template('multiBar.html')

@route('/pythonNVD3js.html')
def home4():
    """
    Examples for Python-nvd3 is a Python wrapper for NVD3 graph library.
    NVD3 is an attempt to build re-usable charts and chart components
    for d3.js without taking away the power that d3.js gives you.
    Project location : https://github.com/areski/python-nvd3
    """
    from nvd3 import linePlusBarWithFocusChart
    chart = linePlusBarWithFocusChart(name='linePlusBarChart', x_is_date=True, x_axis_format="%d %b %Y")

    xdata = [1365026400000000, 1365026500000000, 1365026600000000]
    ydata = [-6, 5, -1]
    y2data = [36, 55, 11]
    kwargs = {}
    kwargs['bar'] = True
    extra_serie = {"tooltip": {"y_start": "There is ", "y_end": " calls"},
                   "date_format": "%d %b %Y %H:%S" }
    chart.add_serie(name="Serie 1", y=ydata, x=xdata, extra=extra_serie, **kwargs)

    extra_serie = {"tooltip": {"y_start": "There is ", "y_end": " min"}}
    chart.add_serie(name="Serie 2", y=y2data, x=xdata, extra=extra_serie)


    chart.header_css=['<link media="all" href="/css/nv.d3.css" type="text/css" rel="stylesheet" />']
    chart.header_js=['<script src="/js/jquery.js"></script>','<script src="/d3/d3.min.js" type="text/javascript"></script>','<script src="/d3/nv.d3.js" type="text/javascript"></script>',]
    chart.buildhtml()

    return chart.htmlcontent

# from sys import path
# path.append('libs')
# path.append('wsgi')
# from priceprofor_single_plots import MapaCalorPreciosMercadoDiario
# MapaCalorPreciosMercadoDiario()
@route('/MapaCalorPreciosMercadoDiario.html')
def MapaCalorPreciosMercadoDiario():
    '''
    Mapa de calor para el Mercado Diario. Vamos a enseñar los ultimos 7 dias disponibles.
    Dibujo D3 casi directo. Esta libreria nos permite construir la grafica con los datos.
    Inputs de la plantilla son:
    days = ["Lu", "Ma", "Mx", "Ju", "Vi", "Sa", "Do"],
    times = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"];
    var data = [{"day": 1,"hour": 1, "value": 1},{"day": 1,"hour": 2, "value": 5}]
    '''
    print 'GET Mapa Calor Precios'

    DAYS = 7
    ONEDAY = timedelta(1)
    endDate = datetime.now()
    startDate = endDate - timedelta(DAYS)
    iterDate = startDate
    absList = list()
    orList = list()

    ite = 1
    while (endDate > iterDate):
        print iterDate.date()
        absList.append(str(iterDate.date()))
        dic = preciosDiarios(iterDate)
        priceList = copy(dic['precios'])
        priceList.pop(0)
        [ orList.append({"day": ite, "hour": i+1, "value": priceList[i][1]}) for i in range(24) ]
        iterDate += ONEDAY
        ite += 1
    print ''

    return template('MapaCalorPreciosMercadoDiario.html',data=orList,days=absList)


@route('/PreciosMercadoDiarioNVD3.html')
def PreciosMercadoDiarioNVD3(fecha=None):
    '''
    Esta grafica usa la libreria python nvd3
    '''
    fecha = datetime(2014,6,14)
    print 'GET precios'

    chart = lineChart(name='lineChart', height=400, width=800, x_is_date=False,)
    dic = preciosDiarios(fecha)
    priceDic = copy(dic['precios'])
    priceDic.pop(0)

    orData = list()
    for element in priceDic:
        orData.append(element[1])

    absData = range(24)

    chart.buildhtml()
    chart.add_serie(name="Precios", y=orData, x=absData)
    chart.header_css=['<link media="all" href="/css/nv.d3.css" type="text/css" rel="stylesheet" />']
    chart.header_js=['<script src="/js/jquery.js"></script>','<script src="/d3/d3.min.js" type="text/javascript"></script>','<script src="/d3/nv.d3.js" type="text/javascript"></script>',]
    chart.buildhtml()

    return chart.htmlcontent

@route('/TecnologiasMercadoDiarioNVD3.html')
def TecnologiasMercadoDiarioNVD3(fecha=None):
    '''
    Esta grafica usa la libreria python nvd3
    '''
    fecha = datetime(2014,6,14)
    print 'GET tecnologias'

    def addList(lista):
        suma = 0
        for i in range(0,len(lista)):
            suma = suma + lista[i]
        return suma

    chart = pieChart(name='pieChart', color_category='category20c', height=400, width=400)
    dic = tecnologiasDiarias(fecha)

    hourList = list()
    for element in dic['tecnologias']:
        hourList.append(element.pop(0))

    orData0 = list()
    orData1 = list()
    orData2 = list()
    orData3 = list()
    orData4 = list()
    orData5 = list()
    for element in dic['tecnologias']:
        orData0.append(element[0])
        orData1.append(element[1])
        orData2.append(element[2])
        orData3.append(element[3])
        orData4.append(element[4])
        orData5.append(element[5])

    key0 = orData0.pop(0)
    key1 = orData1.pop(0)
    key2 = orData2.pop(0)
    key3 = orData3.pop(0)
    key4 = orData4.pop(0)
    key5 = orData5.pop(0)

    techDic = dict()
    techDic[key0] = addList(orData0)
    techDic[key1] = addList(orData1)
    techDic[key2] = addList(orData2)
    techDic[key3] = addList(orData3)
    techDic[key4] = addList(orData4)
    techDic[key5] = addList(orData5)

    absData = dic['tecnologias'][0]

    orData = [techDic['FUEL_GAS'], techDic['NUCLEAR'], techDic['REGIMEN_ESPECIAL'],
             techDic['HIDRAULICA_CONVENCIONAL'], techDic['CICLO_COMBINADO'], techDic['CARBON']]

    chart.buildhtml()
    chart.add_serie(name="Tecnologias", y=orData, x=absData)
    chart.header_css=['<link media="all" href="/css/nv.d3.css" type="text/css" rel="stylesheet" />']
    chart.header_js=['<script src="/js/jquery.js"></script>','<script src="/d3/d3.min.js" type="text/javascript"></script>','<script src="/d3/nv.d3.js" type="text/javascript"></script>',]
    chart.buildhtml()

    return chart.htmlcontent

@route('/priceprofor/rest/help/util.html')
def util():
    '''
    '''
    print 'GET'

    return template('util.html')

# -*- coding: utf-8 -*-
'''
Created on 26/06/2014
@author: hmarrao@ekergy
'''


# bottle server imports:
from bottle import route, template
from dbpreciosesmanager import preciosDiarios

@route('/')
def home():
    '''
    '''
    return template('home.html')

@route('/uikitTemplate.html')
def home():
    '''
    '''
    return template('uikitTemplate.html')

@route('/multiBar.html')
def home():
    '''
    '''
    return template('multiBar.html')
    

@route('/pythonNVD3js.html')
def home():
    """
    Examples for Python-nvd3 is a Python wrapper for NVD3 graph library.
    NVD3 is an attempt to build re-usable charts and chart components
    for d3.js without taking away the power that d3.js gives you.

    Project location : https://github.com/areski/python-nvd3
    """
    from nvd3 import stackedAreaChart
    chart = stackedAreaChart(name='stackedAreaChart')

    xdata = [100, 101, 102, 103, 104, 105, 106,]
    ydata = [6, 11, 12, 7, 11, 10, 11]
    ydata2 = [8, 2, 16, 10, 20, 28, 28]
    ydata3 = [9, 54, 16, 12, 18, 20, 28]
    ydata4 = [10, 20, 16, 12, 20, 28, 18]

    extra_serie = {"tooltip": {"y_start": "There is ", "y_end": " min"}}
    chart.add_serie(name="Serie 1", y=ydata, x=xdata, extra=extra_serie)
    chart.add_serie(name="Serie 2", y=ydata2, x=xdata, extra=extra_serie)
    chart.add_serie(name="Serie 3", y=ydata3, x=xdata, extra=extra_serie)
    chart.add_serie(name="Serie 4", y=ydata4, x=xdata, extra=extra_serie)
    chart.buildhtml()


    chart.header_css=['<link media="all" href="/css/nv.d3.css" type="text/css" rel="stylesheet" />']
    chart.header_js=['<script src="/js/jquery.js"></script>','<script src="/d3/d3.min.js" type="text/javascript"></script>','<script src="/d3/nv.d3.js" type="text/javascript"></script>',]
    chart.buildhtml()


    #output_file.write(chart.htmlcontent)
    #---------------------------------------

    #close Html file
    

    return chart.htmlcontent

@route('/MapaCalorPreciosMercadoDiario.html')
def MapaCalorPreciosMercadoDiario():
    '''
    Teste para el Mapa de calor para el Mercado Diario
    Vamos a enseñar los ultimos 7 dias disponibles.
    Inputs de la plantilla son:
    days = ["Lu", "Ma", "Mx", "Ju", "Vi", "Sa", "Do"],
    times = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"];
            Este puede o no ser un input
    var data = [{"day": 1,"hour": 1, "value": 1},{"day": 1,"hour": 2, "value": 5}]
    '''
    from datetime import datetime

    ONEDAY = datetime.timedelta(1)

    dic = preciosDiarios(datetime.now())

    print dic['precios'].pop(0)

    dataValores = [{"day": 1,"hour": i+1,"value": dic['precios'][i][1]} for i in range(24)]

    #dataValores = [{"day": 1,"hour": 1, "value": 1},{"day": 1,"hour": 2, "value": 5},{"day": 1,"hour": 3, "value": 5},{"day": 1,"hour": 4, "value": 5},
    #{"day": 1,"hour": 5, "value": 5},{"day": 1,"hour": 6, "value": 5},{"day": 1,"hour": 7, "value": 5}]
    print dataValores
    daysLabel = ["2012-1-4", "2012-1-3", "2012-1-2", "2012-1-1", "Vi", "Sa", "Do"]

    return template('MapaCalorPreciosMercadoDiario.html',data=dataValores,days=daysLabel)



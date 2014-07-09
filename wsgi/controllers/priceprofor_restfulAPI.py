# -*- coding: utf-8 -*-
'''
Created on 2014-07-07
@author: hmarrao & david
Module containing  the needed controllers that define the Mobile APÎ.
'''

# Server imports
from bottle import route, template
from dbpreciosesmanager import priceAppli

@route('/priceprofor/rest/help', method=['GET'])
def helpinfo():
    '''
    Ayuda de como usar la API:
    '''
    print 'GET'

#     return "Esta es la Página de Ayuda."
    return template('infoutil.html')

@route('/priceprofor/rest/main', method=['GET'])
def maininfo():
    '''
    Main page info and information:
        the last 3 days available in the database.
        each day will include info of: 
        marketvalues = [0 for i in range(24)]
        horamax = {hora: [0-23], precio: float2}
        horamin = {precio: [0-23], precio: float2}

    So last values are:
        YYYY-mm-dd = dict ( marketvalues = [0 for i in range(24)],
                            horamax = {hora: [0-23], precio: float},
                            horamin = {precio: [0-23], precio: float} )
    '''
    print 'GET'

#     valores = dict()
#     valores['2014-07-07'] = {}
#     valores['2014-07-07']['mercado'] = [0 for i in range(24)]
#     valores['2014-07-07']['horamax'] = {'hora' : 15, 'precio': 20.00}
#     valores['2014-07-07']['horamin'] = {'hora' : 5 , 'precio': 10.00}
#     # defining response to format things and give the proper anwser.
#     # as result is already a dict no need to perform conversion
#     # to the data values.
#     # return valores

    priceDic = priceAppli()

    return priceDic

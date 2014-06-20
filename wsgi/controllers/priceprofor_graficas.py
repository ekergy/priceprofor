# -*- coding: utf-8 -*-
'''
Created on 05/2014
@author: hmarrao & david
'''

from bottle import route,template, response, request
from kernelCaracterizacionEnergetica import temporadaConsumoVector
from datautilities import toGoogleDataTable
from dbpreciosesmanager import preciosDiarios
from time import strptime
from datetime import datetime
from pymongo import Connection

def enable_cors(fn):
    '''
    Decorator to enable jquery for a bottle route
    '''
    def _enable_cors(*args, **kwargs):
        '''
        Decorator to enable jquery for a bottle route
        '''
        # set CORS headers
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = \
        'GET, POST, PUT, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = \
        'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
        if request.method != 'OPTIONS':
            #actual request; reply with the actual response
            return fn(*args, **kwargs)
    return _enable_cors

# from sys import path
# path.append('libs')
# path.append('wsgi')
# from controllers.sme_graficas import findLastDayDocument
# findLastDayDocument()
def findLastDayDocument():
    '''
    Extraemos de la base de datos el ultimo documento (en funcion de la fecha interna del propio documento)
    '''
    ''' LOCAL '''
    # collection = Connection(host=None).mercadodiario.precioses
    ''' SERVIDOR '''
    collection = Connection(host='mongodb://hmarrao:hmarrao@ds031117.mongolab.com:31117/mercadodiario').mercadodiario.precioses

    currentDT = datetime(datetime.now().year, datetime.now().month, datetime.now().day)
    cursor = collection.find({"fecha": {"$lte": currentDT}})
    for element in cursor:
        lastelement = element
    return lastelement['fecha']

# from sys import path
# path.append('libs')
# path.append('wsgi')
# from controllers.sme_graficas import relativeExtremes
# relativeExtremes()
def relativeExtremes(dic):
    '''
    '''
    # dic = preciosDiarios(datetime(2014,6,16))

    def dosDigitos(num):
        strNum = str(num)
        if len(strNum)==1:
            return '0'+str(strNum)
        else:
            return strNum

    pricesList = list()
    if dic['precios'] != [[]]:
        for element in dic['precios']:
            pricesList.append(element[1])
        pricesList.pop(0)
        minPrice = min(pricesList)
        posMinPrice = dosDigitos(pricesList.index(min(pricesList)))
        posMinPriceSig = dosDigitos(pricesList.index(min(pricesList))+1)
        maxPrice = max(pricesList)
        posMaxPrice = dosDigitos(pricesList.index(max(pricesList)))
        posMaxPriceSig = dosDigitos(pricesList.index(max(pricesList))+1)
    else:
        minPrice = ''
        posMinPrice =''
        maxPrice = ''
        posMaxPrice = ''
        posMinPriceSig = ''
        posMaxPriceSig = ''
    return minPrice, maxPrice, posMinPrice, posMaxPrice, posMinPriceSig, posMaxPriceSig

@route('/CProfileTemporadas', method=['OPTIONS','POST','GET'])
@enable_cors
def GraficaPerfilTemporada():
    """
    Plantilla de edicion o creacion de contratos
    """
    response.headers['Content-Type'] = 'application/json'
    EnergeticCaracterization = request.json
    teste = eval(str(EnergeticCaracterization))
    result = temporadaConsumoVector(teste)
    return toGoogleDataTable(**{'DataToTransform': result, 'FirstElementAreLabels': True})
#     teste1 = {"436":{"Ocupa":[1,0,0],"Frigo0":[1,"A+"],"Horno0":[1],"Lava0":[1,"A+"],"Vaji":[1],"Micro":[1],"Placa_3":[1],"Seca0":[1,"A+"],"Portatil":[1],"TV":[1],"B_bacon0":[17,"26"],"Rad0":[1,"950"],"AA0":[1],"Termo0":[1],"Zona":[1,"Atlantica"],"V_PVC":[7],"Habs":[1,"5"],"M2":[1,"Mayor o igual a 100 m2"],"Orien":[1,"Norte"],"Vivi":[1,"Bloque de viviendas"],"Anyo":[1,"Entre 1975 y 2005"],"Multi":[1]}}
#     UsersVector = perfilSimulado(teste1)
#     return template('sme_perfil_invierno_verano',
#                      result = result)

@route('/PerfilTemporadas2/<coopname>/<uname>', method='GET')
def GraficaPerfilTemporada(coopname, uname):
    """
    Plantilla de edicion o creacion de contratos
    """
    plotValues = "this is a dummy value"
    print 'hello'
    print ''
    return plotValues

def colorChart(dateTime, minMaxTuple):
    preciosListSeries = list()
    dicSeries = preciosDiarios(dateTime)
    for lista in dicSeries['precios']:
        if lista[0] == 'HORA':
            lista.append({ 'role': 'style' })
        elif lista[1] == minMaxTuple[0]:
            ''' minimo verde '''
            # lista.append('#A5DF00')
            lista.append('#86B404')
        elif lista[1] == minMaxTuple[1]:
            ''' maximo rojo '''
            # lista.append('#FF0000')
            lista.append('#FF0000')
        else:
            # lista.append('#0174DF')
            lista.append('#0080FF')
        preciosListSeries.append(lista)
    # print preciosListSeries
    return preciosListSeries

@route('/PreciosDiarios', method='GET')
# @enable_cors
def graficaPreciosDiariosGET():
    '''
    Plantilla de edicion o creacion de contratos
    '''
    print "esto es el get"
    ''' no se grafica nada en el GET '''
#     noneList = []
#     dateString = ''
#     if dateString == '':
#         dic = preciosDiarios()
    ''' se grafica en el GET el ultimo dia en base de datos '''
    dateTime = findLastDayDocument()
    dic = preciosDiarios(dateTime)
    dateString = str(str(dateTime.day)+'/'+str(dateTime.month)+'/'+str(dateTime.year))
    minMaxTuple = relativeExtremes(dic)
    preciosListSeries = colorChart(dateTime, minMaxTuple)
#     return template('sme_precios_diarios',
    return template('priceprofor_precios_diarios',
#                     preciosList=noneList,
#                     preciosList=dic['precios'],
                    preciosList=preciosListSeries,
                    fecha=dateString,
                    mensaje=dic['mensaje'],
                    minMax=minMaxTuple)

@route('/PreciosDiarios', method='POST')
# @enable_cors
def graficaPreciosDiariosPOST():
    '''
    Plantilla de edicion o creacion de contratos
    '''
    print "esto es el post"
    dateString = request.forms.get("select")
    print dateString
    if dateString == '':
        dic = preciosDiarios()
        minMaxTuple = ('','')
        preciosListSeries = dic['precios']
    else:
        dateTime = datetime.strptime(dateString, '%d/%m/%Y')
        print dateTime
        dic = preciosDiarios(dateTime)
        print dic
        if dic['precios'] == [[]]:
            minMaxTuple = ('','')
            preciosListSeries = dic['precios']
        else:
            minMaxTuple = relativeExtremes(dic)
            preciosListSeries = colorChart(dateTime, minMaxTuple)
#     return template('sme_precios_diarios',
    return template('priceprofor_precios_diarios',
#                     preciosList=dic['precios'],
                    preciosList=preciosListSeries,
                    fecha=dateString,
                    mensaje=dic['mensaje'],
                    minMax=minMaxTuple)

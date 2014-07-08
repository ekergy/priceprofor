# -*- coding: utf-8 -*-
'''
Created on 05/2014
@author: hmarrao & david
'''

from bottle import route,template, response, request
from kernelCaracterizacionEnergetica import temporadaConsumoVector
from datautilities import toGoogleDataTable
from dbpreciosesmanager import preciosDiarios, tecnologiasDiarias
# from time import strptime
from datetime import datetime, timedelta, date
from pymongo import Connection
from dbpreciosesmanager import populatePrecios
from omelinfosys.dbstudydatamanager import populateStudyData

@route('/populatePrecios')
def index():
    '''
    created index.html
    '''
    try:
        # listDaysUpdated = populatePrecios()
        populatePrecios()
        #return '<strong>Put here profor index.html modificado</strong>'
    except:
        raise
        return 'fallo actualizacion'
    else:
        return 'actualizacion base de datos'

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

def populatePreciosActualiza(fn):
    '''
    Decorator to enable jquery for a bottle route
    '''
    def _populatePreciosActualiza(*args, **kwargs):
        # set CORS headers
        populatePrecios()
        #actual request; reply with the actual response
        return fn(*args, **kwargs)

    return _populatePreciosActualiza

def populateTecnologiasActualiza(fn):
    '''
    Decorator to enable jquery for a bottle route
    '''
    def _populateTecnologiasActualiza(*args, **kwargs):
        # dateString = request.forms.get("select")
        # dateTime = datetime.strptime(dateString, '%d/%m/%Y')
        # populateStudyData(dateTime)
        # set CORS headers
        populateStudyData()
        #actual request; reply with the actual response
        return fn(*args, **kwargs)

    return _populateTecnologiasActualiza

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
#     collection = Connection(host=None).mercadodiario.precioses
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

# @route('/PerfilTemporadas2/<coopname>/<uname>', method='GET')
# def GraficaPerfilTemporada2(coopname, uname):
#     """
#     Plantilla de edicion o creacion de contratos
#     """
#     plotValues = "this is a dummy value"
#     print 'hello'
#     print ''
#     return plotValues

def colorChart(dateTime, minMaxTuple):
    preciosListSeries = list()
    dicSeries = preciosDiarios(dateTime)
    for lista in dicSeries['precios']:
        if lista[0] == 'HORA':
            lista.append({ 'role': 'style' })
        elif lista[1] == minMaxTuple[0]:
            ''' minimo verde '''
            # lista.append('#86B404')
            lista.append('#109618')
        elif lista[1] == minMaxTuple[1]:
            ''' maximo rojo '''
            # lista.append('#FF0000')
            lista.append('#dc3912')
        else:
            # lista.append('#0080FF')
            lista.append('#0099c6')
        preciosListSeries.append(lista)
    # print preciosListSeries
    return preciosListSeries

@route('/PreciosDiarios', method='GET')
# @populatePreciosActualiza
@enable_cors
def graficaPreciosDiariosGET():
    '''
    Plantilla de edicion o creacion de contratos
    '''
    print "GET priceprofor"
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
    print preciosListSeries
#     return template('sme_precios_diarios',
    return template('priceprofor_precios_diarios',
#                     preciosList=noneList,
#                     preciosList=dic['precios'],
                    preciosList=preciosListSeries,
                    fecha=dateString,
                    mensaje=dic['mensaje'],
                    minMax=minMaxTuple)

@route('/PreciosDiarios', method='POST')
@enable_cors
def graficaPreciosDiariosPOST():
    '''
    Plantilla de edicion o creacion de contratos
    '''
    print "POST priceprofor"
    dateString = request.forms.get("select")
    # print dateString
    if dateString == '':
        dic = preciosDiarios()
        minMaxTuple = ('','')
        preciosListSeries = dic['precios']
    else:
        dateTime = datetime.strptime(dateString, '%d/%m/%Y')
        # print dateTime
        dic = preciosDiarios(dateTime)
        # print dic
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

# from sys import path
# path.append('libs')
# path.append('wsgi')
# from controllers.sme_graficas import findLastDayDocument
# findLastDayDocument()
def findLastDayDocumentTechnology():
    '''
    Extraemos de la base de datos el ultimo documento (en funcion de la fecha interna del propio documento)
    '''
    ''' LOCAL '''
#     collection = Connection(host=None).OMIEData.OMIEStudyData
    ''' SERVIDOR '''
    collection = Connection(host='mongodb://hmarrao:hmarrao@ds031117.mongolab.com:31117/mercadodiario').mercadodiario.tecnologiases

    currentDT = datetime(datetime.now().year, datetime.now().month, datetime.now().day)
    cursor = collection.find({"fecha": {"$lte": currentDT}})
    for element in cursor:
        lastelement = element
    return lastelement['fecha']

@route('/TecnologiasDiarias', method='GET')
# @populateTecnologiasActualiza
@enable_cors
def graficaTecnologiasDiariasGET():
    '''
    Plantilla de edicion o creacion de contratos
    '''
    print "GET technologyprofor"
    ''' no se grafica nada en el GET '''
#     noneList = []
#     dateString = ''
#     if dateString == '':
#         dic = preciosDiarios()
    ''' se grafica en el GET el ultimo dia en base de datos '''
    dateTime = findLastDayDocumentTechnology()
#     dic = preciosDiarios(dateTime)
    dic = tecnologiasDiarias(dateTime)
    dateString = str(str(dateTime.day)+'/'+str(dateTime.month)+'/'+str(dateTime.year))
#     minMaxTuple = relativeExtremes(dic)
#     preciosListSeries = colorChart(dateTime, minMaxTuple)
#     preciosListSeries = dic['precios']
    tecnologiasListSeries = dic['tecnologias']
#     return template('sme_precios_diarios',
#     return tecnologiasListSeries,dateString
    return template('priceprofor_tecnologias_diarias',
#                     preciosList=noneList,
#                     preciosList=dic['precios'],
#                     preciosList=preciosListSeries,
                    tecnologiasList=tecnologiasListSeries,
                    fecha=dateString,
                    mensaje=dic['mensaje'],
#                     minMax=minMaxTuple
                    )

@route('/TecnologiasDiarias', method='POST')
@enable_cors
def graficaTecnologiasDiariasPOST():
    '''
    Plantilla de edicion o creacion de contratos
    '''
    print "POST technologyprofor"
    dateString = request.forms.get("select")
    # print dateString
    if dateString == '':
#         dic = preciosDiarios()
        dic = tecnologiasDiarias()
#         minMaxTuple = ('','')
#         preciosListSeries = dic['precios']
        tecnologiasListSeries = dic['tecnologias']
    else:
        dateTime = datetime.strptime(dateString, '%d/%m/%Y')
        # print dateTime
#         dic = preciosDiarios(dateTime)
        dic = tecnologiasDiarias(dateTime)
        # print dic
#         if dic['precios'] == [[]]:
        if dic['tecnologias'] == [[]]:
#             minMaxTuple = ('','')
#             preciosListSeries = dic['precios']
            tecnologiasListSeries = dic['tecnologias']
        else:
#             minMaxTuple = relativeExtremes(dic)
#             preciosListSeries = colorChart(dateTime, minMaxTuple)
            tecnologiasListSeries = dic['tecnologias']
#     return template('sme_precios_diarios',
    return template('priceprofor_tecnologias_diarias',
#                     preciosList=dic['precios'],
#                     preciosList=preciosListSeries,
                    tecnologiasList=tecnologiasListSeries,
                    fecha=dateString,
                    mensaje=dic['mensaje'],
#                     minMax=minMaxTuple
                    )

@route('/ModelosPrediccion', method='GET')
@enable_cors
def graficaModelosPrediccionGET():
    '''
    '''
    print "GET"

    dateTime = findLastDayDocumentTechnology()
    dic = tecnologiasDiarias(dateTime)
    dateString = str(str(dateTime.day)+'/'+str(dateTime.month)+'/'+str(dateTime.year))

    collection = Connection(host=None).mercadodiario.modelosHTES
    dayahead = datetime(2014,05,19)
    resultsdayahead = collection.find({ "dayahead" : {"$in": [dayahead]} })

#     arrayTDT = list()
#     arrayTDT.append(['Date', 'Precio'])
#     for element in resultsdayahead:
#         if element['tipo'] == 'working':
#             dt = datetime(element['fecha'].year, element['fecha'].month, element['fecha'].day, element['hora'])
#             arrayTDT.append([str(date.strftime(dt, '%Y/%m/%d %H:%M:%S')), element['PreciosES']])
#     tecnologiasListSeries = arrayTDT

#     VAR0 = list()
#     VAR1 = list()
#     VAR2 = list()
#     arrayTDT = list()
#     arrayTDT.append(['Date', 'Working','Model'])
#     for element in resultsdayahead:
#         if element['tipo'] == 'working':
#             dt = datetime(element['fecha'].year, element['fecha'].month, element['fecha'].day, element['hora'])
#             VAR0.append(str(date.strftime(dt, '%Y/%m/%d %H:%M:%S')))
#         if element['tipo'] == 'working':
#             VAR1.append(element['PreciosES'])
#         if element['tipo'] == 'model':
#             VAR2.append(element['PreciosES'])
#     for index in range(len(VAR0)):
#         arrayTDT.append([ VAR0[index], VAR1[index], VAR2[index] ])
#     tecnologiasListSeries = arrayTDT

    VAR0 = list()
    VAR1 = list()
    VAR2 = list()
    VAR3 = list()
    VAR4 = list()
    VAR5 = list()
#     VAR6 = list()
#     VAR7 = list()
    arrayTDT = list()
#     emptyValue = 'null'
    emptyValue = -100

    arrayTDT.append( ['Date', 'Working', 'Model', 'Teste', {'type':'number', 'role':'interval'}, {'type':'number', 'role':'interval'}, 'Dayahead'] )
#     arrayTDT.append( ['DateTime', 'Data', 'Model', 'Prediction', {'type':'number', 'role':'interval'}, {'type':'number', 'role':'interval'}, {'type':'number', 'role':'interval'}, {'type':'number', 'role':'interval'}, 'Dayahead'] )
    for element in resultsdayahead:
        if element['fecha'] <= dayahead + timedelta(2):
#         if element['fecha'] >= datetime(2014,4,19) and element['fecha'] <= datetime(2014,5,21):
            # print element['fecha']
            if element['tipo'] == 'working' or element['tipo'] == 'teste':
                dt = datetime(element['fecha'].year, element['fecha'].month, element['fecha'].day, element['hora'])
                VAR0.append(str(date.strftime(dt, '%Y/%m/%d %H:%M:%S')))

            if element['tipo'] == 'working':
                VAR1.append(element['PreciosES'])
            elif element['tipo'] == 'teste':
                VAR1.append(emptyValue)
            if element['tipo'] == 'model':
                VAR2.append(element['PreciosES'])
            elif element['tipo'] == 'teste':
                VAR2.append(emptyValue)

            if element['tipo'] == 'teste':
                VAR3.append(element['PreciosES'])
            elif element['tipo'] == 'working':
                VAR3.append(emptyValue)
            if element['tipo'] == 'lower80':
                VAR4.append(element['PreciosES'])
            elif element['tipo'] == 'working':
                VAR4.append(emptyValue)
            if element['tipo'] == 'upper80':
                VAR5.append(element['PreciosES'])
            elif element['tipo'] == 'working':
                VAR5.append(emptyValue)

#             if element['tipo'] == 'lower95':
#                 VAR6.append(element['PreciosES'])
#             elif element['tipo'] == 'working':
#                 VAR6.append(emptyValue)
#             if element['tipo'] == 'upper95':
#                 VAR7.append(element['PreciosES'])
#             elif element['tipo'] == 'working':
#                 VAR7.append(emptyValue)

    for index in range(len(VAR0)):
        arrayTDT.append([ VAR0[index], VAR1[index], VAR2[index], VAR3[index], VAR4[index], VAR5[index], -100 ])
#         arrayTDT.append([ VAR0[index], VAR1[index], VAR2[index], VAR3[index], VAR4[index], VAR5[index], VAR6[index], VAR7[index], -100 ])

    arrayTDTda = list()
    for index in range(len(arrayTDT)):
#         if arrayTDT[index][0] == '2014/05/19 00:00:00':
        if arrayTDT[index][0] == date.strftime(dayahead, '%Y/%m/%d %H:%M:%S'):
            daList = list()
            for element in arrayTDT[index]:
                daList.append(element)
            daList.pop(6)
            daList.insert(6,100)
            arrayTDTda.append(daList)
        arrayTDTda.append(arrayTDT[index])

    for index in range(len(arrayTDTda)):
        if arrayTDTda[index][0] > '2014/05/18 00:00:00' and arrayTDTda[index][0] < '2014/05/19 01:00:00':
            print arrayTDTda[index]

    print ''

    tecnologiasListSeries = arrayTDTda

    print arrayTDT
    print ''

    print dayahead
    print ''

#     print len(VAR0)
#     print len(VAR1)
#     print len(VAR2)
#     print len(VAR3)
#     print ''

    return template('priceprofor_modelos_prediccion',
                    tecnologiasList=tecnologiasListSeries,
                    fecha=dateString,
                    mensaje=dic['mensaje'],
                    )

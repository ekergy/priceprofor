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
from json import dumps

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

# from sys import path
# path.append('libs')
# path.append('wsgi')
# from controllers.priceprofor_graficas import relativeExtremes, preciosDiarios
# from datetime import datetime
# dateTime = datetime(2014,7,9)
# dic = preciosDiarios(dateTime)
# relativeExtremes(dic)
def relativeExtremes(dic):
    """
    Esta funcion devuelve el par maximo y el par minimo de una lista en que los elementos es un par de valores.
    return a list/tuple  (minPrice, maxPrice, posMinPrice, posMaxPrice, posMinPriceSig, posMaxPriceSig)
    """
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
        maxPrice = max(pricesList)
        posMinPrice = dosDigitos(pricesList.index(min(pricesList)))
        posMinPriceSig = dosDigitos(pricesList.index(min(pricesList))+1)
        posMaxPrice = dosDigitos(pricesList.index(max(pricesList)))
        posMaxPriceSig = dosDigitos(pricesList.index(max(pricesList))+1)
    else:
        minPrice = ''
        maxPrice = ''
        posMinPrice =''
        posMaxPrice = ''
        posMinPriceSig = ''
        posMaxPriceSig = ''
    return minPrice, maxPrice, posMinPrice, posMaxPrice, posMinPriceSig, posMaxPriceSig
#     return minPrice, maxPrice

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
            ''' estandar azul '''
            # lista.append('#0099c6')
            lista.append('#3366cc')
        preciosListSeries.append(lista)
    # print preciosListSeries
    return preciosListSeries

def averageList(lista):
    suma=0.0
    for i in range(0,len(lista)):
        suma=suma+lista[i]
    media = suma/len(lista)
    return round(media, 2)

def lineChart(dateTime, preciosList, meanList):
    meanType = list()
    palabraType = list()
    meanType.append(meanList)
    palabraType.append('PRECIO MEDIO')
    for index in range(len(preciosList)):
        if preciosList[index][0] == 'HORA':
            preciosList[index] = preciosList[index]+palabraType
        else:
            preciosList[index] = preciosList[index]+meanType
    print ''
    print 'preciosList'
    print preciosList
    print ''
    return preciosList

def lineChartMulti(dateTime, preciosList, meanList, previsionEolicaList, previsionDemandaList, energiaGestionadaList):
    meanType = list()
    palabraType = list()

    palabraTypeEolica = list()
    palabraTypeDemanda = list()
    palabraTypeEG = list()

    ''' los precios dibujados corresponden al ultimo dia que tenemos datos de tecnologias '''

    meanType.append(meanList)
    palabraType.append('PRECIO MEDIO')

    palabraTypeEolica.append('PREVISION EOLICA')
    palabraTypeDemanda.append('PREVISION DEMANDA')
    palabraTypeDemanda.append('ENERGIA GESTIONADA')

    for index in range(len(preciosList)):
        if preciosList[index][0] == 'HORA':
            preciosList[index] = preciosList[index] + palabraTypeEolica + palabraTypeDemanda + palabraTypeEG
        else:
            ''' todos los vectores salvo "preciosList" van un lugar por detras en el indice '''
            preciosList[index] = preciosList[index] + [previsionEolicaList[index-1]] + [previsionDemandaList[index-1]] + [energiaGestionadaList[index-1]]

    ''' si no queremos representar el precio ni su color, dada el diferente orden de magnitud '''
    for element in preciosList:
        del element[1]
    for element in preciosList:
        del element[1]

#     print ''
#     print preciosList
#     print ''

    return preciosList

def lineChartMultiPrice(dateTime, preciosList, meanList, previsionEolicaList, previsionDemandaList, energiaGestionadaList):
    meanType = list()
    palabraType = list()

    palabraTypeEolica = list()
    palabraTypeDemanda = list()
    palabraTypeEG = list()

    ''' los precios dibujados corresponden al ultimo dia que tenemos datos de tecnologias '''

    meanType.append(meanList)
    palabraType.append('PRECIO MEDIO')

    palabraTypeEolica.append('PREVISION EOLICA')
    palabraTypeDemanda.append('PREVISION DEMANDA')
    palabraTypeDemanda.append('ENERGIA GESTIONADA')

    pricesVector = list()
    for element in preciosList:
        pricesVector.append(element[1])
#     del pricesVector[0]

#     print pricesVector
#     print ''

    ''' al dividir dos numeros enteros, es necesario convertir uno de ellos a float '''

    preciosListCoefficient = list()
    for index in range(len(pricesVector)):
        if index == 0:
            preciosListCoefficient.append(pricesVector[index])
        if index != 0:
            preciosListCoefficient.append(round(pricesVector[index] / 180.0,4))
#     print 'preciosListCoefficient'
#     print preciosListCoefficient
#     print ''

    for index in range(len(preciosListCoefficient)):
        preciosList[index][1] = preciosListCoefficient[index]

    previsionDemandaListCoefficient = list()
    for index in range(len(previsionDemandaList)):
        previsionDemandaListCoefficient.append(round(previsionDemandaList[index] / float(previsionDemandaList[index]),4))
#     print 'previsionDemandaListCoefficient'
#     print previsionDemandaListCoefficient
#     print ''

    previsionEolicaListCoefficient = list()
    for index in range(len(previsionDemandaList)):
        previsionEolicaListCoefficient.append(round(previsionEolicaList[index] / float(previsionDemandaList[index]),4))
#     print 'previsionEolicaListCoefficient'
#     print previsionEolicaListCoefficient
#     print ''

    energiaGestionadaListCoefficient = list()
    for index in range(len(previsionDemandaList)):
        energiaGestionadaListCoefficient.append(round(energiaGestionadaList[index] / float(previsionDemandaList[index]),4))
#     print 'energiaGestionadaListCoefficient'
#     print energiaGestionadaListCoefficient
#     print ''

    for index in range(len(preciosList)):
        if preciosList[index][0] == 'HORA':
            # preciosList[index] = preciosList[index] + palabraTypeEolica + palabraTypeDemanda + palabraTypeEG
            # preciosList[index] = preciosList[index] + palabraTypeEolica + palabraTypeDemanda + palabraTypeEG
            preciosList[index] = preciosList[index] + palabraTypeEolica + palabraTypeEG + palabraTypeDemanda
        else:
            ''' todos los vectores salvo "preciosList" van un lugar por detras en el indice '''
            # preciosList[index] = preciosList[index] + [previsionEolicaList[index-1]] + [previsionDemandaList[index-1]] + [energiaGestionadaList[index-1]]
            # preciosList[index] = preciosList[index] + [previsionEolicaListCoefficient[index-1]] + [previsionDemandaListCoefficient[index-1]] + [energiaGestionadaListCoefficient[index-1]]
            preciosList[index] = preciosList[index] + [previsionEolicaListCoefficient[index-1]] + [energiaGestionadaListCoefficient[index-1]] + [previsionDemandaListCoefficient[index-1]]

#     ''' si no queremos representar el precio ni su color, dada el diferente orden de magnitud '''
#     for element in preciosList:
#         del element[1]
#     for element in preciosList:
#         del element[1]

    print ''
    print preciosList
    print ''

    return preciosList

@route('/PreciosDiarios', method='GET')
# @enable_cors
def graficaPreciosDiariosGET():
    '''
    Plantilla de edicion o creacion de contratos
    '''
    print "GET"
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
    preciosList = colorChart(dateTime, minMaxTuple)

    vector = list()
    for element in range(1,len(dic['precios'])):
        vector.append(dic['precios'][element][1])
    meanList = averageList(vector)
    preciosList = lineChart(dateTime, preciosList, meanList)

#     return template('sme_precios_diarios',
    return template('priceprofor_precios_diarios',
#                     preciosList=noneList,
#                     preciosList=dic['precios'],
                    preciosList=preciosList,
                    fecha=dateString,
                    mensaje=dic['mensaje'],
                    minMax=minMaxTuple,
                    meanList=meanList)

@route('/PreciosDiarios', method='POST')
# @enable_cors
def graficaPreciosDiariosPOST():
    '''
    Plantilla de edicion o creacion de contratos
    '''
    print "POST"
    dateString = request.forms.get("select")
    # print dateString
    if dateString == '':
        dic = preciosDiarios()
        minMaxTuple = ('','')
        preciosList = dic['precios']
        meanList = None
    else:
        dateTime = datetime.strptime(dateString, '%d/%m/%Y')
        # print dateTime
        dic = preciosDiarios(dateTime)
        # print dic
        if dic['precios'] == [[]]:
            minMaxTuple = ('','')
            preciosList = dic['precios']
            meanList = None
        else:
            minMaxTuple = relativeExtremes(dic)
            preciosList = colorChart(dateTime, minMaxTuple)
            vector = list()
            for element in range(1,len(dic['precios'])):
                vector.append(dic['precios'][element][1])
            meanList = averageList(vector)
            preciosList = lineChart(dateTime, preciosList, meanList)

#     return template('sme_precios_diarios',
    return template('priceprofor_precios_diarios',
#                     preciosList=dic['precios'],
                    preciosList=preciosList,
                    fecha=dateString,
                    mensaje=dic['mensaje'],
                    minMax=minMaxTuple,
                    meanList=meanList)

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
    Callback de '/ModelosPrediccion'.
    Este callback tiene que Buscar el ultimo documento dsiponible en la collection de Previsiones.

    Este codigo incluye tanto modelo (working, model) como prediccion (teste, intervals)
    '''
    dateTime = findLastDayDocumentTechnology()
    dic = tecnologiasDiarias(dateTime)
    dateString = str(str(dateTime.day)+'/'+str(dateTime.month)+'/'+str(dateTime.year))

    collection = Connection(host=None).mercadodiario.modelosHTES
#     dayahead = datetime(2014,7,14)
#     dayahead = datetime(2014,6,1)
    dayahead = datetime(2014,6,6)
    resultsdayahead = collection.find({ "dayahead" : {"$in": [dayahead]} })

    VAR0 = list()
    VAR1 = list()
    VAR2 = list()
    VAR3 = list()
    VAR4 = list()
    VAR5 = list()
#     VAR6 = list()
#     VAR7 = list()
    arrayTDT = list()
    emptyValue = None

    arrayTDT.append( ['Fechayhora', 'Datos', 'Modelo', 'Prediccion', {'type':'number', 'role':'interval'}, {'type':'number', 'role':'interval'}] )
    for element in resultsdayahead:
        if element['fecha'] <= dayahead + timedelta(1) and element['fecha'] >= dayahead - timedelta(7):
            # print element['fecha']
            if element['tipo'] == 'working' or element['tipo'] == 'teste':
                dt = datetime(element['fecha'].year, element['fecha'].month, element['fecha'].day, element['hora'])
                # VAR0.append(str(date.strftime(dt, '%Y/%m/%d %H:%M:%S')))
                VAR0.append(str(date.strftime(dt, '%Y/%m/%d %H:%M')))

            if element['tipo'] == 'working':
                VAR1.append(round(element['PreciosES'],2))
            elif element['tipo'] == 'teste':
                VAR1.append(emptyValue)
            if element['tipo'] == 'model':
                VAR2.append(round(element['PreciosES'],2))
            elif element['tipo'] == 'teste':
                VAR2.append(emptyValue)

            if element['tipo'] == 'teste':
                VAR3.append(round(element['PreciosES'],2))
            elif element['tipo'] == 'working':
                VAR3.append(emptyValue)
            if element['tipo'] == 'lower80':
                VAR4.append(round(element['PreciosES'],2))
            elif element['tipo'] == 'working':
                VAR4.append(emptyValue)
            if element['tipo'] == 'upper80':
                VAR5.append(round(element['PreciosES'],2))
            elif element['tipo'] == 'working':
                VAR5.append(emptyValue)

#             if element['tipo'] == 'lower95':
#                 VAR6.append(round(element['PreciosES'],2))
#             elif element['tipo'] == 'working':
#                 VAR6.append(emptyValue)
#             if element['tipo'] == 'upper95':
#                 VAR7.append(round(element['PreciosES'],2))
#             elif element['tipo'] == 'working':
#                 VAR7.append(emptyValue)

    for index in range(len(VAR0)):
        arrayTDT.append([ VAR0[index], VAR1[index], VAR2[index], VAR3[index], VAR4[index], VAR5[index]])

#     arrayTDTda = list()
#     for index in range(len(arrayTDT)):
#         if arrayTDT[index][0] == date.strftime(dayahead, '%Y/%m/%d %H:%M:%S'):
#             daList = list()
#             for element in arrayTDT[index]:
#                 daList.append(element)
#             daList.pop(6)
#             daList.insert(6,100)
#             arrayTDTda.append(daList)
#         arrayTDTda.append(arrayTDT[index])
#     for index in range(len(arrayTDTda)):
#         if arrayTDTda[index][0] > '2014/05/18 00:00:00' and arrayTDTda[index][0] < '2014/05/19 01:00:00':
#             print arrayTDTda[index]

    print 'DAYAHEAD'
    print dayahead.date()
    print ''
    print arrayTDT
    print ''

    ''' json.dumps interpreta "None" de python como "null" para google '''
    return template('priceprofor_modelos_prediccion',
                    modelosPrediccionList=dumps(arrayTDT),
                    fecha=dateString,
                    mensaje=dic['mensaje'],
                    )

@route('/GraphicPrediction', method='GET')
@enable_cors
def graphicpredictionGET():
    '''
    '''
    dateTime = findLastDayDocumentTechnology()
    dic = tecnologiasDiarias(dateTime)
    dateString = str(str(dateTime.day)+'/'+str(dateTime.month)+'/'+str(dateTime.year))

    collection = Connection(host=None).mercadodiario.modelosHTES
#     dayahead = datetime(2014,7,14)
#     dayahead = datetime(2014,6,1)
    dayahead = datetime(2014,6,6)
    resultsdayahead = collection.find({ "dayahead" : {"$in": [dayahead]} })

    VAR0 = list()
#     VAR1 = list()
#     VAR2 = list()
    VAR3 = list()
    VAR4 = list()
    VAR5 = list()
#     VAR6 = list()
#     VAR7 = list()
    arrayTDT = list()
    emptyValue = None

#     arrayTDT.append( ['Fechayhora', 'Datos', 'Modelo', 'Prediccion', {'type':'number', 'role':'interval'}, {'type':'number', 'role':'interval'}] )
    arrayTDT.append( ['Fechayhora', 'Prediccion', {'type':'number', 'role':'interval'}, {'type':'number', 'role':'interval'}] )
    for element in resultsdayahead:
#         if element['fecha'] <= dayahead + timedelta(1) and element['fecha'] >= dayahead - timedelta(7):
        if element['fecha'] <= dayahead + timedelta(1) and element['fecha'] >= dayahead:
            # print element['fecha']
            if element['tipo'] == 'working' or element['tipo'] == 'teste':
                dt = datetime(element['fecha'].year, element['fecha'].month, element['fecha'].day, element['hora'])
                # VAR0.append(str(date.strftime(dt, '%Y/%m/%d %H:%M:%S')))
                VAR0.append(str(date.strftime(dt, '%Y/%m/%d %H:%M')))

#             if element['tipo'] == 'working':
#                 VAR1.append(round(element['PreciosES'],2))
#             elif element['tipo'] == 'teste':
#                 VAR1.append(emptyValue)
#             if element['tipo'] == 'model':
#                 VAR2.append(round(element['PreciosES'],2))
#             elif element['tipo'] == 'teste':
#                 VAR2.append(emptyValue)

            if element['tipo'] == 'teste':
                VAR3.append(round(element['PreciosES'],2))
            elif element['tipo'] == 'working':
                VAR3.append(emptyValue)
            if element['tipo'] == 'lower80':
                VAR4.append(round(element['PreciosES'],2))
            elif element['tipo'] == 'working':
                VAR4.append(emptyValue)
            if element['tipo'] == 'upper80':
                VAR5.append(round(element['PreciosES'],2))
            elif element['tipo'] == 'working':
                VAR5.append(emptyValue)

#             if element['tipo'] == 'lower95':
#                 VAR6.append(round(element['PreciosES'],2))
#             elif element['tipo'] == 'working':
#                 VAR6.append(emptyValue)
#             if element['tipo'] == 'upper95':
#                 VAR7.append(round(element['PreciosES'],2))
#             elif element['tipo'] == 'working':
#                 VAR7.append(emptyValue)

    for index in range(len(VAR0)):
#         arrayTDT.append([ VAR0[index], VAR1[index], VAR2[index], VAR3[index], VAR4[index], VAR5[index]])
        arrayTDT.append([ VAR0[index], VAR3[index], VAR4[index], VAR5[index]])

#     arrayTDTda = list()
#     for index in range(len(arrayTDT)):
#         if arrayTDT[index][0] == date.strftime(dayahead, '%Y/%m/%d %H:%M:%S'):
#             daList = list()
#             for element in arrayTDT[index]:
#                 daList.append(element)
#             daList.pop(6)
#             daList.insert(6,100)
#             arrayTDTda.append(daList)
#         arrayTDTda.append(arrayTDT[index])
#     for index in range(len(arrayTDTda)):
#         if arrayTDTda[index][0] > '2014/05/18 00:00:00' and arrayTDTda[index][0] < '2014/05/19 01:00:00':
#             print arrayTDTda[index]

    print 'DAYAHEAD'
    print dayahead.date()
    print ''
    print arrayTDT
    print ''

    ''' json.dumps interpreta "None" de python como "null" para google '''
#     return template('priceprofor_modelos_prediccion',
    return template('priceprofor_prediccion',
                    modelosPrediccionList=dumps(arrayTDT),
                    fecha=dateString,
                    mensaje=dic['mensaje'],
                    )

@route('/DataPrediction', method='GET')
@enable_cors
def datapredictionGET():
    '''
    arrayTDT
    es el vector arrayTDT del metodo anterior llamada "PrediccionGrafica"
    '''
    arrayTDT = [['Fechayhora', 'Prediccion', {'role': 'interval', 'type': 'number'}, {'role': 'interval', 'type': 'number'}], ['2014/06/06 00:00', 53.1, 41.62, 64.57], ['2014/06/06 01:00', 49.64, 37.92, 61.35], ['2014/06/06 02:00', 48.6, 37.02, 60.18], ['2014/06/06 03:00', 50.03, 38.31, 61.76], ['2014/06/06 04:00', 49.12, 37.31, 60.92], ['2014/06/06 05:00', 50.03, 38.97, 61.09], ['2014/06/06 06:00', 53.77, 44.11, 63.43], ['2014/06/06 07:00', 54.32, 44.3, 64.35], ['2014/06/06 08:00', 57.31, 47.76, 66.86], ['2014/06/06 09:00', 56.73, 47.56, 65.9], ['2014/06/06 10:00', 57.98, 49.39, 66.58], ['2014/06/06 11:00', 59.89, 51.08, 68.7], ['2014/06/06 12:00', 58.27, 49.31, 67.23], ['2014/06/06 13:00', 58.92, 49.99, 67.86], ['2014/06/06 14:00', 54.46, 45.04, 63.88], ['2014/06/06 15:00', 51.72, 41.84, 61.6], ['2014/06/06 16:00', 53.54, 43.03, 64.05], ['2014/06/06 17:00', 56.11, 45.71, 66.51], ['2014/06/06 18:00', 55.49, 45.37, 65.61], ['2014/06/06 19:00', 57.53, 47.59, 67.48], ['2014/06/06 20:00', 57.78, 47.73, 67.82], ['2014/06/06 21:00', 57.79, 48.38, 67.2], ['2014/06/06 22:00', 60.86, 49.0, 72.71], ['2014/06/06 23:00', 57.97, 48.42, 67.52], ['2014/06/07 00:00', 58.81, 46.4, 71.22], ['2014/06/07 01:00', 57.54, 45.17, 69.91], ['2014/06/07 02:00', 55.09, 42.96, 67.23], ['2014/06/07 03:00', 55.94, 39.36, 72.52], ['2014/06/07 04:00', 55.09, 42.82, 67.36], ['2014/06/07 05:00', 54.87, 39.23, 70.52], ['2014/06/07 06:00', 53.4, 39.73, 67.06], ['2014/06/07 07:00', 47.09, 32.91, 61.27], ['2014/06/07 08:00', 47.18, 33.67, 60.68], ['2014/06/07 09:00', 46.77, 33.8, 59.74], ['2014/06/07 10:00', 49.52, 37.37, 61.68], ['2014/06/07 11:00', 51.27, 38.81, 63.73], ['2014/06/07 12:00', 49.77, 37.1, 62.45], ['2014/06/07 13:00', 51.04, 38.41, 63.68], ['2014/06/07 14:00', 47.03, 33.72, 60.35], ['2014/06/07 15:00', 42.7, 28.73, 56.67], ['2014/06/07 16:00', 43.58, 30.01, 57.14], ['2014/06/07 17:00', 45.97, 33.07, 58.86], ['2014/06/07 18:00', 44.53, 32.04, 57.02], ['2014/06/07 19:00', 47.74, 35.44, 60.04], ['2014/06/07 20:00', 49.56, 35.4, 63.72], ['2014/06/07 21:00', 54.51, 41.85, 67.17], ['2014/06/07 22:00', 54.4, 40.95, 67.85], ['2014/06/07 23:00', 51.82, 38.31, 65.33]]
    return dumps(arrayTDT)

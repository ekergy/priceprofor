# -*- coding: utf-8 -*-
'''
Created on 05/2014
@author: hmarrao & david
'''

# from time import strptime
# from omelinfosys.dbstudydatamanager import DBStudyData
from bottle import route, template, response, request
from kernelCaracterizacionEnergetica import temporadaConsumoVector
from datautilities import toGoogleDataTable
from dbpreciosesmanager import preciosDiarios, tecnologiasDiarias
from datetime import datetime, timedelta, date
from pymongo import Connection
from json import dumps
from dbpreciosesmanager import populatePrecios
from omelinfosys.dbstudydatamanager import populateStudyData
from dbpreciosesmanager import realMongo, exploradorporenergiagestionada
from utilities import findLastDayDocumentPrice, findLastDayDocumentTechnology

@route('/exploradorporenergiagestionada')
def exploradorporenergiagestionadaGET():
    '''
    '''
    fechaIni = datetime(2014,9,1)
    fechaFin = datetime(2014,10,28)

    try:
        # return 'try'
        resultados = exploradorporenergiagestionada(fechaIni,fechaFin)
        # print resultados
        return str(resultados)
    except:
        raise
        return 'except'
    else:
        return 'ok'

@route('/populatePrecios')
def indexprecios():
    '''
    '''
    try:
        populatePrecios()
    except:
        raise
        return 'fallo en la actualizacion de precios'
    else:
        return 'precios actualizados'

@route('/populateTecnologias')
def indextecnologias():
    '''
    '''
    try:
        populateStudyData()
    except:
        raise
        return 'fallo en la actualizacion de tecnologias'
    else:
        return 'tecnologias actualizadas'

# @route('/machineCygnus')
# def machinecygnusCONNECTION():
#     '''
#     created index.html
#     '''
#     try:
#         print 'ssh'
#         # ssh indizen@192.168.1.154
#     except:
#         raise
#         return 'yes'
#     else:
#         return 'no'

####################################################################################################

# To schedule your scripts to run on a periodic basis, add the scripts to 
# your application's .openshift/cron/{minutely,hourly,daily,weekly,monthly}/
# directories (and commit and redeploy your application).
# 
# Example: A script .openshift/cron/hourly/crony added to your application
#          will be executed once every hour.
#          Similarly, a script .openshift/cron/weekly/chronograph added
#          to your application will be executed once every week.

####################################################################################################

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
#     print ''
#     print 'preciosList'
#     print preciosList
#     print ''
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
#     for element in preciosList:
#         del element[1]
#     for element in preciosList:
#         del element[1]

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
#             preciosListCoefficient.append(round(pricesVector[index] / 180.0,4))
            preciosListCoefficient.append(round(pricesVector[index] / 90.0,4))
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

#     print ''
#     print preciosList
#     print ''

    return preciosList

@route('/PreciosDiarios', method='GET')
# @populatePreciosActualiza
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
    dateTime = findLastDayDocumentPrice()
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

    ''' instancia al metodo de clase DBStudyData '''
#     ins = DBStudyData()
#     dateTime = ins.findLastRecordInDB()['fecha']
#     del ins

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

# @route('/PredictionModelsHWTES', method='GET')
@route('/PredictionModels', method='GET')
@enable_cors
def graphicpredictionmodelsGET():
    '''
    Callback de '/PredictionModels'.
    Este callback tiene que Buscar el ultimo documento dsiponible en la collection de Previsiones.

    Este codigo incluye tanto modelo (working, model) como prediccion (teste, intervals)
    '''
    dateTime = findLastDayDocumentTechnology()
    dic = tecnologiasDiarias(dateTime)
    dateString = str(str(dateTime.day)+'/'+str(dateTime.month)+'/'+str(dateTime.year))

    ''' LOCAL '''
#     collection = Connection(host=None).mercadodiario.modelosHWTES
    ''' SERVIDOR '''
    collection = Connection(host='mongodb://hmarrao:hmarrao@ds031117.mongolab.com:31117/mercadodiario').mercadodiario.modelosHWTES

    ''' el dia relevante a graficar es el dayahead y sus predicciones de precio '''
    # dayahead = datetime(2014,6,1)
    currentDate = datetime(datetime.now().year,datetime.now().month,datetime.now().day)
    dayahead = currentDate + timedelta(1)

    ''' a partir de las 15:00 se podria ejecutar esta linea de codigo '''
#     dayahead = currentDate + timedelta(2)

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
                # VAR0.append(str(date.strftime(dt, '%Y/%m/%d %H:%M')))
                VAR0.append(str(date.strftime(dt, '%d/%m/%Y %H:%M')))

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
    # print arrayTDT
    # print ''

    ''' json.dumps interpreta "None" de python como "null" para google '''
    return template('priceprofor_modelo_prediccion',
                    modelosPrediccionList=dumps(arrayTDT),
                    fecha=dateString,
                    mensaje=dic['mensaje'],
                    )

@route('/PredictionModelsARNN', method='GET')
@enable_cors
def graphicpredictionmodelsarnnGET():
    '''
    Callback de '/PredictionModels'.
    Este callback tiene que Buscar el ultimo documento dsiponible en la collection de Previsiones.

    Este codigo incluye tanto modelo (working, model) como prediccion (teste, intervals)
    '''
    dateTime = findLastDayDocumentTechnology()
    dic = tecnologiasDiarias(dateTime)
    dateString = str(str(dateTime.day)+'/'+str(dateTime.month)+'/'+str(dateTime.year))

    ''' LOCAL '''
    collection = Connection(host=None).mercadodiario.modelosARNN
    ''' SERVIDOR '''
#     collection = Connection(host='mongodb://hmarrao:hmarrao@ds031117.mongolab.com:31117/mercadodiario').mercadodiario.modelosARNN

    ''' el dia relevante a graficar es el dayahead y sus predicciones de precio '''
    # dayahead = datetime(2014,6,1)
    currentDate = datetime(datetime.now().year,datetime.now().month,datetime.now().day)
    dayahead = currentDate + timedelta(1)
#     DAYAHEAD = datetime(2014,10,7)

    ''' a partir de las 15:00 se podria ejecutar esta linea de codigo '''
#     dayahead = currentDate + timedelta(2)

#     resultsdayahead = collection.find({ "dayahead" : {"$in": [dayahead]} })
    resultsdayahead = collection.find({ "dayaheadNN" : {"$in": [dayahead]} })

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
                # VAR0.append(str(date.strftime(dt, '%Y/%m/%d %H:%M')))
                VAR0.append(str(date.strftime(dt, '%d/%m/%Y %H:%M')))

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
    # print arrayTDT
    # print ''

    ''' json.dumps interpreta "None" de python como "null" para google '''
    return template('priceprofor_modelo_prediccion_ARNN',
                    modelosPrediccionList=dumps(arrayTDT),
                    fecha=dateString,
                    mensaje=dic['mensaje'],
                    )

# from sys import path
# path.append('libs')
# path.append('wsgi')
# from controllers.priceprofor_RESTful_API import forecastArrayTDT
# forecastArrayTDT()
def forecastArrayTDT():
    '''
    '''

    ''' LOCAL '''
#     collection = Connection(host=None).mercadodiario.modelosHWTES
    ''' SERVIDOR '''
    collection = Connection(host='mongodb://hmarrao:hmarrao@ds031117.mongolab.com:31117/mercadodiario').mercadodiario.modelosHWTES

#     dayahead = datetime(2014,7,14)
#     dayahead = datetime(2014,6,1)
#     dayahead = datetime(2014,6,6)
    currentDate = datetime(datetime.now().year,datetime.now().month,datetime.now().day)
    dayahead = currentDate + timedelta(1)
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
#     print arrayTDT
#     print ''

    return arrayTDT

'''
collection = Connection(host=None).mercadodiario.modelosHWTES
/usr/bin/python2.7 /home/david/workspace/electraPROFOR/ElectricityMarket/ExponentialSmoothing/testeHWTES_robjects.py
'''

@route('/PredictionModelsHWTESreal', method='GET')
@enable_cors
def graphicpredictionmodelshwtesrealGET():
    '''
    Callback de '/PredictionModels'.
    Este callback tiene que Buscar el ultimo documento dsiponible en la collection de Previsiones.

    Este codigo incluye tanto modelo (working, model) como prediccion (teste, intervals)
    '''
    dateTime = findLastDayDocumentTechnology()
    dic = tecnologiasDiarias(dateTime)
    dateString = str(str(dateTime.day)+'/'+str(dateTime.month)+'/'+str(dateTime.year))

    ''' LOCAL '''
#     collection = Connection(host=None).mercadodiario.modelosHWTES
    ''' SERVIDOR '''
    collection = Connection(host='mongodb://hmarrao:hmarrao@ds031117.mongolab.com:31117/mercadodiario').mercadodiario.modelosHWTES

    ''' el dia relevante a graficar es el dayahead y sus predicciones de precio '''
    currentDate = datetime(datetime.now().year,datetime.now().month,datetime.now().day)
    dayahead = currentDate + timedelta(1)

#     dayahead = datetime(2014,6,1)
#     dayahead = currentDate

    ''' a partir de las 15:00 se podria ejecutar esta linea de codigo '''
#     dayahead = currentDate + timedelta(2)

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

    fecha_aux = datetime.now()

    if fecha_aux.hour in [0,1,2,3,4,5,6,7,8,9,10,11,12,13]:
        realLine = 0
    elif fecha_aux.hour in [14,15,16,17,18,19,20,21,22,23]:
        realLine = 1

    # print ''
    # print fecha_aux.hour

    ''' codigo replicado para simular una hora de hoy a partir de las 15:00 para que existan precios dayahead '''
#     hourNew = 14
#     if fecha_aux.replace(hour=hourNew).hour in [0,1,2,3,4,5,6,7,8,9,10,11,12,13]:
#         realLine = 0
#     elif fecha_aux.replace(hour=hourNew).hour in [14,15,16,17,18,19,20,21,22,23]:
#         realLine = 1
#     # print ''
#     # print fecha_aux.replace(hour=hourNew).hour

    if realLine == 0:
        arrayTDT.append( ['Fechayhora', 'Datos', 'Modelo', 'Prediccion', {'type':'number', 'role':'interval'}, {'type':'number', 'role':'interval'}] )
    elif realLine == 1:
        arrayTDT.append( ['Fechayhora', 'Datos', 'Modelo', 'Prediccion', {'type':'number', 'role':'interval'}, {'type':'number', 'role':'interval'}, 'Real'] )

#     arrayTDT.append( ['Fechayhora', 'Datos', 'Modelo', 'Prediccion', {'type':'number', 'role':'interval'}, {'type':'number', 'role':'interval'}] )
#     arrayTDT.append( ['Fechayhora', 'Datos', 'Modelo', 'Prediccion', {'type':'number', 'role':'interval'}, {'type':'number', 'role':'interval'}, 'Real'] )
    for element in resultsdayahead:
        if element['fecha'] <= dayahead + timedelta(1) and element['fecha'] >= dayahead - timedelta(7):
            # print element['fecha']
            if element['tipo'] == 'working' or element['tipo'] == 'teste':
                dt = datetime(element['fecha'].year, element['fecha'].month, element['fecha'].day, element['hora'])
                # VAR0.append(str(date.strftime(dt, '%Y/%m/%d %H:%M:%S')))
                # VAR0.append(str(date.strftime(dt, '%Y/%m/%d %H:%M')))
                VAR0.append(str(date.strftime(dt, '%d/%m/%Y %H:%M')))

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

##################################################

    horasEnUnDia = 24
    horasGraficadas = len(VAR0)

    ''' VAR8 longitud actual 216 '''
    zerosListINI = [None] * (horasGraficadas - horasEnUnDia * 2)
#     zerosListINI = [None] * (216 - horasEnUnDia * 2)
    zerosListFIN = [None] * horasEnUnDia
    VAR8 = zerosListINI + realMongo() + zerosListFIN

#     print VAR8
#     print len(VAR8)
#     print ''

##################################################

    for index in range(len(VAR0)):
        if realLine == 0:
            arrayTDT.append([ VAR0[index], VAR1[index], VAR2[index], VAR3[index], VAR4[index], VAR5[index]])
        elif realLine == 1:
            arrayTDT.append([ VAR0[index], VAR1[index], VAR2[index], VAR3[index], VAR4[index], VAR5[index], VAR8[index]])

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
    # print arrayTDT
    # print ''

    ''' json.dumps interpreta "None" de python como "null" para google '''
    return template('priceprofor_modelo_prediccion_HWTES_real',
                    modelosPrediccionList=dumps(arrayTDT),
                    fecha=dateString,
                    mensaje=dic['mensaje'],
                    )

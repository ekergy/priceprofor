# -*- coding: utf-8 -*-
'''
Created on 05/2014
@author: hmarrao & david
'''

from os import path
from dbmodelosesmanager import DBModelosES
direc = path.abspath(__file__)
machine = direc[direc.find("e")+2:direc.find("w")-1]

# from utilities import validafecha, omiepreciosurl, stringtofloat, cambiohoraverano, cambiohorainvierno
# from utilities import stringtofloat
# from csv import reader
# from omelinfosys.dbrawdatamanager import DBRawData
from pymongo import Connection
from datetime import datetime, timedelta, date
from utilities import omiepreciosurl, cambiohoraverano, cambiohorainvierno
from urllib2 import urlopen
from omelinfosys.omelhandlers import PreciosMibelHandler, getpreciosmibelfromweb
from omelinfosys.dbstudydatamanager import DBStudyData

# from sys import path
# path.append('libs')
# from dbpreciosesmanager import DBPreciosES
# hostOpenShift = 'mongodb://hmarrao:hmarrao@ds031117.mongolab.com:31117/mercadodiario'
# DBPreciosES.connectiondetails['host'] = hostOpenShift
# from datetime import datetime
# startDT = datetime(2014,10,1)
# from dbpreciosesmanager import populatePrecios
# populatePrecios(startDT)
def populatePrecios(startDate=None, endDate=None):
    '''
    PRECIOS actualiza la base de datos de PRECIOS del servidor
    recordar que el metodo populatePrecios esta gobernado por una clase (cofirmar la conexion)

    populatePrecios por si solo gestiona la actualizacion de base de datos en LOCAL o SERVIDOR
    '''
    try:
        currentDate = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        availableDate = currentDate
        if startDate == None:
            docu = findLastPriceDocument()
            startDate = docu['fecha']
        if startDate > availableDate:
                startDate = availableDate
                # Disponemos de los datos de la web de la "OMIE" del dia actual
        if endDate == None:
            currentDate = datetime(datetime.now().year,datetime.now().month,datetime.now().day)
            # no se actualizan los precios "dayahead" de mañana publicados hoy a las 13:00
            endDate = currentDate
        if endDate > availableDate:
                endDate = availableDate
    except:
        raise
    else:
        listCHV = list()
        listCHI = list()
        for indi in range(endDate.year - startDate.year + 1):
            fechaCHV = cambiohoraverano(startDate.year + indi)
            fechaCHI = cambiohorainvierno(startDate.year + indi)
            listCHV.append(fechaCHV)
            listCHI.append(fechaCHI)

        iterDate = startDate
        ONEDAY = timedelta(1)
        while (endDate >= iterDate):
            print 'Updating',iterDate.date()
            ins = DBPreciosES()
            # print ins.getCollection()
            ins.fecha = iterDate
            priceDay = getpreciosmibelfromweb(ins.fecha)['PreciosES']

            if len(priceDay) == 24:
                pass
            elif len(priceDay) == 23:
                horaCHV = 3
                priceDay.insert(horaCHV,priceDay[horaCHV-1])
            elif len(priceDay) == 25:
                horaCHI = 3
                priceDay.pop(horaCHI)

            for i in range(len(priceDay)):
                ins.hora = i
                ins.priceHour = priceDay[ins.hora]
                ins.updatedbprecioses()
            del ins

            if currentDate == iterDate:
                raise Exception('En la web del OMIE no hay datos nuevos')

            iterDate += ONEDAY

# from sys import path
# path.append('libs')
# from dbpreciosesmanager import findLastPriceDocument
# findLastPriceDocument()
def findLastPriceDocument():
    '''
    Extraemos de la base de datos el ultimo documento
    (en funcion de la fecha interna del propio documento)
    Hacer la query sin la fecha como input
    '''
    ins = DBPreciosES()
    collection = ins.getCollection()
    # cursor = collection.find().sort("fecha",-1).limit(1)
    cursor = collection.find().sort([("fecha",-1),("hora",-1)]).limit(1)
    for element in cursor:
        # print element['hora']
        # fecha = element['fecha']
        docu = element
    del ins
    return docu

# from sys import path
# path.append('libs')
# from dbpreciosesmanager import findFirstPriceDocument
# findFirstPriceDocument()
def findFirstPriceDocument():
    '''
    Extraemos de la base de datos el ultimo documento
    (en funcion de la fecha interna del propio documento)
    Hacer la query sin la fecha como input
    '''
    ins = DBPreciosES()
    collection = ins.getCollection()
    # cursor = collection.find().sort("fecha",-1).limit(1)
    cursor = collection.find().sort([("fecha",1),("hora",1)]).limit(1)
    for element in cursor:
        # print element['hora']
        # fecha = element['fecha']
        docu = element
    del ins
    return docu

####################################################################################################

# from sys import path
# path.append('libs')
# from datetime import datetime
# fecha = datetime(2014,1,1)
# from dbpreciosesmanager import getpreciosesfromweb
# getpreciosesfromweb(fecha)
def getpreciosesfromweb(fecha):
        '''
        This is the main method so the usage of PreciosMibelHandler is more strainfoward.
        '''
        try:
            ''' Se comenta validafecha dado que si existen los precios de dia de mañana '''
            # validafecha(fecha)
            toparsePRECIOS = urlopen(omiepreciosurl(fecha))
        except:
            raise
        else:
            Precios = PreciosMibelHandler(toparsePRECIOS)
            return {"PreciosES": Precios.precioses}
        #finally:
        #    del toparsePRECIOS,Precios

####################################################################################################

# from sys import path
# path.append('libs')
# from omelinfosys.dbpreciosesmanager import mercadodiarioD3
# mercadodiarioD3()
def mercadodiarioD3():
    '''
    '''

# from pymongo import Connection
# collection = Connection().mercadodiario.precioses

# cursor = collection.find()
# for element in cursor:
#     print element

# from datetime import datetime
# cursor = collection.find({"fecha": {"$gte": datetime(2014,3,1), "$lte": datetime(2014,3,2)} })
# for element in cursor:
#     print element

    ins = DBPreciosES()
    collection = ins.getCollection()
    # cursor = collection.find({u'fecha': datetime(2014, 1, 1)})
    # cursor = collection.find({"fecha": {"$gte": datetime(2014,1,1), "$lte": datetime(2014,4,30)} })
    cursor = collection.find({"fecha": {"$gte": datetime(2011,1,1), "$lte": datetime(2014,4,30)} })
    # cursor = collection.find()
    listD3 = list()
    for element in cursor:
        listD3.append(element)

    listCSV = list()
    for element in listD3:
        newDT = datetime(element['fecha'].year, element['fecha'].month, element['fecha'].day, element['hora'])
        # listCSV.append([element['fecha'],element['hora'],element['PreciosES']])
        listCSV.append([newDT,element['hora'],element['PreciosES']])

    thelist = listCSV
    rutaData = '/home/'+machine+'/workspace/profordes/data/mercadodiario/'
    # f = open(rutaData+"sp500.txt","w")
    f = open(rutaData+"sp500.csv","w")
    thefile = f
    thefile.write("date,price\n")
    # thefile.write("datetime,hour,price\n")
    for item in thelist:
        thefile.write("%s" % item[0])
        # thefile.write(",")
        # thefile.write("%s" %item[1])
        thefile.write(",")
        thefile.write("%s\n" %item[2])
    f.close()
#     return listD3

# from sys import path
# path.append('libs')
# from dbpreciosesmanager import preciosDiarios
# preciosDiarios()
def preciosDiarios(fechayhora=None):
    '''
    notar que en el proyecto "profordes" dentro del script con el mismo nombre que este
    esta implementado el metodo "populatePrecios" que actualiza esta misma base de datos

    transformar fechayhora en un date de mongo.

    '''
    if fechayhora is None:
        fechayhora = None
    else:
        fechayhora = datetime(fechayhora.year,fechayhora.month,fechayhora.day,)

    dic = dict()
    priceList = list()
    nameList = [ 'HORA', 'PRECIO' ]
    hourList = ['00-01','01-02','02-03','03-04','04-05','05-06','06-07','07-08','08-09','09-10','10-11','11-12',
                '12-13','13-14','14-15','15-16','16-17','17-18','18-19','19-20','20-21','21-22','22-23','23-00']
    messageList = ''
    # noneList = [None, None]
    # noneList = [0, 0]
    noneList = []

    ins = DBPreciosES()
    collection = ins.getCollection()

    cursor = collection.find({ "fecha": {"$in": [fechayhora]} })
    if fechayhora == None:
        priceList.append(noneList)
        messageList = 'Se debe seleccionar una fecha del calendario'
    elif  cursor.count() == 0:
        priceList.append(noneList)
        messageList = 'No hay datos de la fecha seleccionada'
    else:
        priceList.append(nameList)
        indice = 0
        for element in cursor:
                vectorList = [ hourList[indice], element['PreciosES']  ]
                priceList.append(vectorList)
                indice = indice + 1
    dic['fecha'] = fechayhora
    dic['precios'] = priceList
    dic['mensaje'] = messageList
    del ins
    return dic

# from sys import path
# path.append('libs')
# from dbtecnologiasesmanager import tecnologiasDiarias
# tecnologiasDiarias()
def tecnologiasDiarias(fecha=None, hora=None):
    '''
    '''
#     ''' fecha dummy '''
#     fecha = datetime(2014,5,20)
    dic = dict()
    technologyList = list()
    nameList = [ 'HORA',
                'NUCLEAR', 'REGIMEN_ESPECIAL', 'HIDRAULICA_CONVENCIONAL',
                'CARBON', 'CICLO_COMBINADO', 'FUEL_GAS' ]
    hourList = ['00-01','01-02','02-03','03-04','04-05','05-06','06-07','07-08','08-09','09-10','10-11','11-12',
                '12-13','13-14','14-15','15-16','16-17','17-18','18-19','19-20','20-21','21-22','22-23','23-00']
    messageList = ''
    noneList = []

    ins_study = DBStudyData()
    collection = ins_study.getCollection()

    ''' un dia '''
    cursor = collection.find({ "fecha": {"$in": [fecha]} })
    ''' una hora '''
#     cursor = collection.find({ "fecha": {"$in": [fecha]}, "hora": {"$in": [0]} })

    currentDate = datetime(datetime.now().year,datetime.now().month,datetime.now().day)

    if fecha == None:
        technologyList.append(noneList)
        messageList = 'Se debe seleccionar una fecha del calendario'
    elif  fecha == currentDate:
        technologyList.append(noneList)
        messageList = 'Existen datos de tecnologias 3 dias atras'
    elif  fecha == currentDate - timedelta(1):
        technologyList.append(noneList)
        messageList = 'Existen datos de tecnologias 2 dias atras'
    elif  fecha == currentDate - timedelta(2):
        technologyList.append(noneList)
        messageList = 'Existen datos de tecnologias 1 dia atras'
    elif  cursor.count() == 0:
        technologyList.append(noneList)
        messageList = 'No hay datos de la fecha seleccionada'
    else:
        technologyList.append(nameList)
        indice = 0
        for element in cursor:
            vectorList = [ hourList[indice],
                           element['NUCLEAR'], element['REGIMEN_ESPECIAL'], element['HIDRAULICA_CONVENCIONAL'],
                           element['CARBON'], element['CICLO_COMBINADO'], element['FUEL_GAS']  ]
            technologyList.append(vectorList)
            indice = indice + 1
    dic['fecha'] = fecha
    dic['tecnologias'] = technologyList
    dic['mensaje'] = messageList
#     print dic
#     print dic['tecnologias']
#     print dic['tecnologias'][0]
#     print dic['tecnologias'][1]
    del ins_study
    return dic

# from sys import path
# path.append('libs')
# from dbpreciosesmanager import priceAppli
# priceAppli()
def priceAppli():
    '''
    Proporciona un json con vector precios y horas precio maximo/minimo (3 ultimos dias)
    Intenta sacar los ultimos 3 dias disponibles SIN USAR FECHA como input a la query

    O sea busca todas las fechas ordenalas y quedate con los ultimos 3 registros que por cierto ya vienen
    ordenados y no hay que comprobar nada, si garantizamos que la base de datos esta siempre actualizada
    Hay que actualizar este metodo. No esta usando bien la configuracion de base de datos y esto invalida
    el cambio de db a la hora desarrollar en "full local"
    '''

    def maxList(priceList):
        '''
        '''
        maxIndexList = list()
        for index in range(len(priceList)):
            if priceList[index] == max(priceList):
                maxValue = priceList[index]
                maxIndexList.append(index)
        return {'precio': maxValue, 'hora': maxIndexList}

    def minList(priceList):
        '''
        '''
        minIndexList = list()
        for index in range(len(priceList)):
            if priceList[index] == min(priceList):
                minValue = priceList[index]
                minIndexList.append(index)
        return {'precio': minValue, 'hora': minIndexList}

    priceDic = dict()
    # currentDate = datetime(datetime.now().year, datetime.now().month, datetime.now().day)

    ins = DBPreciosES()
    collection = ins.getCollection()

    docu = findLastPriceDocument()

    today = docu['fecha']
    yesterday = today - timedelta(1)
    beforeyesterday = today - timedelta(2)

    cursor = collection.find({ "fecha": {"$in": [today]} })
    priceList = list()
    for element in cursor:
        priceList.append(element['PreciosES'])
    priceDic[date.strftime(today, '%Y-%m-%d')] = {'mercado': priceList,
                                                  'horamax': maxList(priceList),
                                                  'horamin': minList(priceList) }

    cursor = collection.find({ "fecha": {"$in": [yesterday]} })
    priceList = list()
    for element in cursor:
        priceList.append(element['PreciosES'])
    priceDic[date.strftime(yesterday, '%Y-%m-%d')] = {'mercado': priceList,
                                                   'horamax': maxList(priceList),
                                                   'horamin': minList(priceList) }

    cursor = collection.find({ "fecha": {"$in": [beforeyesterday]} })
    priceList = list()
    for element in cursor:
        priceList.append(element['PreciosES'])
    priceDic[date.strftime(beforeyesterday, '%Y-%m-%d')] = {'mercado': priceList,
                                                   'horamax': maxList(priceList),
                                                   'horamin': minList(priceList) }

    del ins
    return priceDic

####################################################################################################

# from sys import path
# path.append('libs')
# from dbpreciosesmanager import forecastAppli
# forecastAppli()
def forecastAppli():
    '''
    Proporciona un json con vector precios de previsiones y confianzas (2 dias siguientes)
    Intenta sacar los siguientes 2 dias disponibles SIN USAR FECHA como input a la query

    O sea busca todas as fechas ordenalas y quedate con los ultimos 3 registros que por cierto ya vienen
    ordenados y no hay que comprobar nada, si garantizamos que la base de datos esta siempre actualizada
    Hay que actualizar este metodo. No esta usando bien la configuracion de base de datos y esto invalida
    el cambio de db a la hora desarrollar en "full local"
    '''

    '''
    {"2014-07-21": ... ,
     "2014-07-22": {"prevision": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    "confianza": [[0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0],
                                  [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0]]}
     "2014-07-23": ... ,}
    '''

    forecastDic = dict()
    # currentDate = datetime(datetime.now().year, datetime.now().month, datetime.now().day)

    ins_modelos = DBModelosES()
    collection = ins_modelos.getCollection()

    dayahead = findLastForecastDocument()
    twodayahead = dayahead + timedelta(1)

    ''' dayahead '''
    cursor = collection.find({ "dayahead": {"$in": [dayahead]},
                               "fecha": {"$in": [dayahead]},
                               "tipo": {"$in": ["teste"]} })
    forecastList = list()
    for element in cursor:
#         forecastList.append(element['PreciosES'])
        forecastList.append(round(element['PreciosES'],2))

    ''' upper80 dayahead '''
    cursor = collection.find({ "dayahead": {"$in": [dayahead]},
                               "fecha": {"$in": [dayahead]},
                               "tipo": {"$in": ["upper80"]} })
    upper80List = list()
    for element in cursor:
        upper80List.append(element['PreciosES'])

    ''' lower80 dayahead '''
    cursor = collection.find({ "dayahead": {"$in": [dayahead]},
                               "fecha": {"$in": [dayahead]},
                               "tipo": {"$in": ["lower80"]} })
    lower80List = list()
    for element in cursor:
        lower80List.append(element['PreciosES'])

    confidenceList = list()
    for index in range(len(forecastList)):
        confidenceList.append([ lower80List[index], upper80List[index] ])

    forecastDic[date.strftime(dayahead, '%Y-%m-%d')] = {'prevision': forecastList,
                                                        'confianza': confidenceList }

    ''' twodayahead '''
    cursor = collection.find({ "dayahead": {"$in": [dayahead]},
                               "fecha": {"$in": [twodayahead]},
                               "tipo": {"$in": ["teste"]} })
    forecastList = list()
    for element in cursor:
        forecastList.append(round(element['PreciosES'],2))

    ''' upper80 twodayahead '''
    cursor = collection.find({ "dayahead": {"$in": [dayahead]},
                               "fecha": {"$in": [twodayahead]},
                               "tipo": {"$in": ["upper80"]} })
    upper80List = list()
    for element in cursor:
        upper80List.append(element['PreciosES'])

    ''' lower80 twodayahead '''
    cursor = collection.find({ "dayahead": {"$in": [dayahead]},
                               "fecha": {"$in": [twodayahead]},
                               "tipo": {"$in": ["lower80"]} })
    lower80List = list()
    for element in cursor:
        lower80List.append(element['PreciosES'])

    confidenceList = list()
    for index in range(len(forecastList)):
        confidenceList.append([ lower80List[index], upper80List[index] ])

    forecastDic[date.strftime(twodayahead, '%Y-%m-%d')] = {'prevision': forecastList,
                                                           'confianza': confidenceList }

    del ins_modelos
    return forecastDic

# from sys import path
# path.append('libs')
# from dbpreciosesmanager import findLastForecastDocument
# findLastForecastDocument()
def findLastForecastDocument():
    '''
    Extraemos de la base de datos el ultimo documento
    (en funcion de la fecha interna del propio documento)
    Hacer la query sin la fecha como input
    '''
    ins_modelos = DBModelosES()
    collection = ins_modelos.getCollection()

    cursor = collection.find().sort([("dayahead",-1)]).limit(1)
    for element in cursor:
        # print element
        dayahead = element['dayahead']

    del ins_modelos
    return dayahead

####################################################################################################

# from sys import path
# path.append('libs')
# from dbpreciosesmanager import findPredictionDayahead
# findPredictionDayahead()
def findPredictionDayahead():
    '''
    '''
    currentDate = datetime(datetime.now().year,datetime.now().month,datetime.now().day)
    DAYAHEAD = currentDate + timedelta(1)

    ins_modelos = DBModelosES()
    collection = ins_modelos.getCollection()

    cursor = collection.find({ "dayahead" : {"$in": [DAYAHEAD]}, "tipo": {"$in": ["teste"]}})
    vector = list()
    for element in cursor:
        if element['fecha'] == DAYAHEAD:
            vector.append(round(element['PreciosES'],2))
    del ins_modelos
    return vector

# from sys import path
# path.append('libs')
# from dbpreciosesmanager import findPriceCurrentDate
# findPriceCurrentDate()
def findPriceCurrentDate():
    '''
    '''
    currentDate = datetime(datetime.now().year,datetime.now().month,datetime.now().day)

    ins = DBPreciosES()
    collection = ins.getCollection()

    cursor = collection.find({ "fecha" : {"$in": [currentDate]}})
    vector = list()
    for element in cursor:
        if element['fecha'] == currentDate:
            vector.append(element['PreciosES'])
    del ins
    return vector

####################################################################################################

# from sys import path
# path.append('libs')
# from dbpreciosesmanager import realMongo
# realMongo()
def realMongo():
    '''
    '''
    ins = DBPreciosES()
    collection = ins.getCollection()

    fecha_aux = datetime.now()

    'today'
#     fecha = fecha_aux.replace(hour=0, minute=0, second=0, microsecond=0)
    'dayahead'
    fecha = fecha_aux.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(1)

#     print fecha.date()
#     print ''

#     cursor = collection.find({"fecha": {"$gte": fecha, "$lte": fecha}}).sort("fecha",1)
    cursor = collection.find({"fecha": {"$in": [fecha]}}).sort("fecha",1)
    realPrices = list()
    for element in cursor:
        # print element
        realPrices.append(element['PreciosES'])

#     print realPrices
#     print ''

    horasEnUnDia = 24
    if realPrices == []:
        ''' con valores cero funciona '''
#         realPrices = [0] * horasEnUnDia
        ''' con valore -1 funciona y no se ve en la grafica '''
        realPrices = [-1] * horasEnUnDia
        ''' con None no funciona ni siquiera con la funcion dumps() '''
#         realPrices = [None] * horasEnUnDia
#         print 'web precios dayahead vacia'

    del ins
    return realPrices

# from sys import path
# path.append('libs')
# from dbpreciosesmanager import testeMongo
# testeMongo()
def testeMongo():
    '''
    '''
    ins_modelos = DBModelosES()
    collection = ins_modelos.getCollection()

    fecha_aux = datetime.now()

    'today'
#     fecha = fecha_aux.replace(hour=0, minute=0, second=0, microsecond=0)
    'dayahead'
    fecha = fecha_aux.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(1)

#     cursor = collection.find({"dayahead": {"$gte": fecha, "$lte": fecha}}).sort("fecha",1)
    cursor = collection.find({"dayahead": {"$in": [fecha]}, "tipo": "teste"}).sort("fecha",1)
    testePrices = list()
    for element in cursor:
        # print element
        testePrices.append(element['PreciosES'])

#     print testePrices
#     print ''

#     horasEnUnDia = 24
#     if testePrices == []:
# #         testePrices = [None] * horasEnUnDia
#         testePrices = [0] * horasEnUnDia
#         print ''
#         print 'web precios dayahead vacia'
#         print ''

    print ''
    print fecha.date()
    print ''
    print testePrices
    print ''
    print len(testePrices)

    del ins_modelos
#     return testePrices

# from sys import path
# path.append('libs')
# from dbpreciosesmanager import errorMongo
# errorMongo()
def errorMongo():
    '''
    para hacer un test del correcto funcionamiento conviene estudiar un dia anterior al dia actual
    currentDate = "el dia actual" (que deberia ser mañana a partir de las 14:00)
    dayahead = "el dia actual" (que deberia ser mañana)
    '''
    # robo mongo

    # var fecha = ISODate("2014-10-07 00:00:00.000Z");
    # db.modelosARNN.find({dayaheadNN: {$in: [fecha]} });

    # var fecha = ISODate("2014-10-07 00:00:00.000Z");
    # db.precioses.find({dayaheadNN: {$in: [fecha]} });

    ins = DBPreciosES()
    collection = ins.getCollection()

    '''
    dayahead
    solo hay datos disponibles del precio de mañana a partir de las 14:00 horas
    por ese motivo redefinimos el valor dayahead intencionadamente al dia actual
    '''
    dayahead = datetime(2014,10,28)

    horaenundia = 24
#     currentDate = datetime(datetime.now().year,datetime.now().month,datetime.now().day)
#     dayahead = currentDate + timedelta(1)

    print ''
    print 'dayahead'
    print dayahead.date()
    print ''

#     cursor = collection.find({ "dayaheadNN": {"$in": [dayahead]}, "fecha": {"$in": [currentDate]}, "tipo": {"$in": ["working"]} })
    cursor = collection.find({ "fecha": {"$in": [dayahead]} })
    working = list()
    for element in cursor:
        working.append(element['PreciosES'])

    print 'working'
    print working
    print len(working)
    print ''

    ins_modelos = DBModelosES()
    collection = ins_modelos.getCollection()

    cursor = collection.find({ "dayaheadNN": {"$in": [dayahead]}, "tipo": {"$in": ["teste"]} })
    testeNN = list()
    for element in cursor:
        testeNN.append(element['PreciosES'])

    ''' selecciono el primer dia (de los dos dias que se han predicho) '''
    if len(testeNN) == horaenundia*2:
        testeNN = testeNN[:horaenundia]

    print 'testeNN'
    print testeNN
    print len(testeNN)
    print ''

    del ins_modelos

    ins_modelos = DBModelosES()
    collection = ins_modelos.getCollection()

    cursor = collection.find({ "dayahead": {"$in": [dayahead]}, "tipo": {"$in": ["teste"]} })
    testeHW = list()
    for element in cursor:
        testeHW.append(element['PreciosES'])

    ''' selecciono el primer dia (de los dos dias que se han predicho) '''
    if len(testeHW) == horaenundia*2:
        testeHW = testeHW[:horaenundia]

    print 'testeHW'
    print testeHW
    print len(testeHW)
    print ''

    rootECM_HWTES = errorCuadraticoMedio(testeHW, working)
    print 'rootECM_HWTES'
    print rootECM_HWTES
    print ''

    rootECM_ARNN = errorCuadraticoMedio(testeNN, working)
    print 'rootECM_ARNN'
    print rootECM_ARNN

    del ins_modelos
    del ins

def errorCuadraticoMedio(working, teste):
    '''
    calcula la raiz del error cuadratico medio sqrtECM
    '''
    horaenundia = 24
#     error2 = 0.0
    error2 = sum(map(lambda x1,x2: (float(x2)-float(x1))**2, working, teste))
    #for indi in range(0,self.N):
    #    error1 = (abs( float(self.opciones['Observaciones'][indi]) - float(self.opciones['Predicciones'][indi])))**2
    #    #error1 = (abs( float(self.opciones['Observaciones'][indi]) ))**2
    #    error2 += error1
    error = error2 / horaenundia
#     ECM = round(error,2)
    rootECM = round(error**(0.50),2)
#     return ECM
    return rootECM

####################################################################################################

# from sys import path
# path.append('libs')
# from dbpreciosesmanager import preciosSemanales
# preciosSemanales()
def preciosSemanales(fechayhora=None):
    '''
    buscar fechas distintas de verano, donde la energia gestionada supere a la prevision demanda
    ya que esto suele significar que el precio es muy bajo porque se ha cubierto toda la demanda
    dividir todo entre la prevision demanda
    funcion actualmente en desarrollo
    '''
    dataHourList = list()
    dataDayList = list()
    dataWeekList = list()

    ins = DBPreciosES()
    collection = ins.getCollection()

    # fecha dummty
    fechayhora = datetime(2014,7,19)

    cursor = collection.find({ "fecha": {"$in": [fechayhora]} })
    for element in cursor:
        # dataDayList = [ element['fecha'], element['hora'], element['PreciosES'] ]
        dataHourList = [ element['fecha'] + timedelta(hours=element['hora']), element['PreciosES'] ]
        dataDayList.append(dataHourList)

    print ''
    print 'vector de fechas'
    print ''
    print dataDayList
    dataWeekList.append(dataDayList)

####################################################################################################

# from sys import path
# path.append('libs')
# from datetime import datetime
# fechaIni = datetime(2014,9,1)
# fechaFin = datetime(2014,10,28)
# from dbpreciosesmanager import exploradorporenergiagestionada
# exploradorporenergiagestionada(fechaIni,fechaFin)
def exploradorporenergiagestionada(fechaIni,fechaFin):
    '''
    Esta funcion realiza la consulta a mongo a los registros de tecnologiases y ordenados por ENERGIA_GESTIONADA.
    El objetivo de este metodo es alimentar el controlador "/exploradorporenergiagestionada".
    El formato que tiene que tener este resultado es:
    [ {el registro tal cual sale de mongo} ]
    '''

    # rellenar este metodo con lo que haga falta para tener lo mismo que tenemos si en robo mongo si hacemos
    #     var fechaStart = ISODate("2014-09-01 00:00:00.000Z");
    #     var fechaEnd = ISODate("2014-10-28 00:00:00.000Z");
    #     db.tecnologiases.find({fecha: {$gte: fechaStart, $lte: fechaEnd} }).sort({ENERGIA_GESTIONADA:1})

    browserResults = []

    ins_study = DBStudyData()
    collection = ins_study.getCollection()

    # ordenacion de menor a mayor con el positivo "1" y ordenacion de mayor a menor con el negativo "-1"
    cursor = collection.find({'fecha': {'$gte': fechaIni, '$lte': fechaFin} }).sort([('ENERGIA_GESTIONADA',1)])

    for element in cursor:
        browserResults.append(element)

    del ins_study
    return browserResults

####################################################################################################

# from sys import path
# path.append('libs')
# from dbpreciosesmanager import DBPreciosES
# ins = DBPreciosES()
class DBPreciosES(object):
    '''
    '''
    connectiondetails = dict(host=None)
#     connectiondetails = dict()

    def __init__(self):
        '''
        SET COLLECTION NAME IN MONGO
        No need for user uname or coopid
        '''

        ''' LOCAL '''
#         self.connectiondetails['host'] = None
        ''' SERVIDOR '''
#         self.connectiondetails['host'] = 'mongodb://hmarrao:hmarrao@ds031117.mongolab.com:31117/mercadodiario'

        self.connectiondetails['host'] = self.connectiondetails['host']
        self.connectiondetails['db_name'] = 'mercadodiario'
        self.connectiondetails['coll_name'] = 'precioses'
        self.setCollection()

    def updatedbprecioses(self):
        '''
        # insert or update
        # no olvidar de poner un sort por fecha y luego por hora
        '''
        try:
            self.setCollection()
            collection = self.getCollection()
            results = collection.find({ "fecha": {"$in" : [self.fecha]}, "hora": {"$in": [self.hora]} })
            jsontoinsert = dict()
            jsontoinsert['fecha'] = self.fecha
            jsontoinsert['hora'] = self.hora
            jsontoinsert['PreciosES'] = self.priceHour
            # print jsontoinsert
            if results.count() == 0:
                collection.insert(jsontoinsert)
            if results.count() == 1:
                collection.update({"fecha": {"$in": [self.fecha]} , "hora" : {"$in" : [self.hora]} }, {"$set": jsontoinsert})
            if results.count() > 1:
                raise Exception('La base de datos tiene mas de un registro para la fecha dada')
        except:
            raise
        else:
            self.setCollection(), jsontoinsert

    def getCollection(self):
        '''
        Get mongo collection cursor
        '''
        return self._collection

#     def setCollection(self, conndetails=None):
    def setCollection(self, connectiondetails=None):
        '''
        Sets collection to be used
        '''
        self._connection = Connection(host=self.connectiondetails['host'])
        self._db = self._connection[self.connectiondetails['db_name']]
        self._collection = self._db[self.connectiondetails['coll_name']]

    def delCollection(self):
        '''
        Remove cursors from mongo database and collections
        '''
        self._connection.close()
        del self._db, self._collection

    Collection = property(getCollection,
                          setCollection,
                          delCollection,
                          "La collection para hacer las queries")

    def setprecios(self, fechayprecio):
        '''
        Ignora los dias de cambio de hora con la regla de la hora 3.
        '''
        try:
            self.setCollection()
            collection = self.getCollection()
            # Should be something like isert or update:
            collection.insert(fechayprecio)
        except:
            raise
        else:
            self.delCollection()

    # from sys import path
    # path.append('libs')
    # from omelinfosys.dbpreciosesmanager import DBPreciosES
    # ins = DBPreciosES()
    # from datetime import datetime
    # fecha = datetime(2014,1,1)
    # ins.getprecio(fecha)
    def getprecio(self, fecha, hora):
    # def getprecio(self, fechayhora):
        '''
        fechayhora es un datetime con hora.
        '''
        try:
            dic = dict()
            self.setCollection()
            collection = self.getCollection()
            # print fecha
            # print hora
            # print fechayhora
            # print fechayhora.hour
            results = collection.find({ "fecha": {"$in" : [fecha]}, "hora": {"$in": [hora]} })
            # results = collection.find({ "fecha": {"$in" : [fechayhora]}, "hora": {"$in": [fechayhora.hour]} })
            for result in results:
                # print result
                dic = result
        except:
            raise
        else:
            self.delCollection()
            # print dic
            # print dic['PreciosES']
            return dic['PreciosES']

    def getprecios(self, fechaStart, fechaEnd=None):
        try:
            self.setCollection()
#             collection = self.getCollection()

        except:
            raise
        else:
            self.delCollection()
        # return [fechayprecio]

    def getallprecios(self):
        try:
            self.setCollection()
#             collection = self.getCollection()
            # no olvidar de poner un sort por fecha y luego por hora.
#             results = collection.find()
        except:
            raise
        else:
            self.delCollection()
        # return [fechayprecio]

    def getlastpreciodate(self):
        '''
        Esto tiene que devolver la ultima fecha disponible en base de datos.
        O sea esto tiene que devolver un datetime.datetime 
        '''
        try:
            self.setCollection()
#             collection = self.getCollection()

        except:
            raise
        else:
            self.delCollection()
        # return fechayprecio

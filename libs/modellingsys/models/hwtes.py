# -*- coding: utf-8 -*-
"""
"""

# import paths
from os import path
direc = path.abspath(__file__)
machine = direc[direc.find("e")+2:direc.find("w")-1]
import sys
sys.path.append('/home/'+machine+'ruta')

# import R objects
from rpy2.robjects import FloatVector
from rpy2.robjects.packages import importr
from rpy2 import robjects

# import python modules
from datetime import datetime, timedelta
from operator import itemgetter
from pymongo import Connection

# loading R packages
stats = importr('stats')
base = importr('base')
forecast = importr('forecast')

def studioHWTES(period,datos0Hora,datos1Hora,miHora):
    """

    Notes of developers:
        

    """
    prices = FloatVector(datos0Hora)

    timeseries = fullfunctionR('''
        f <- function(prices, period, argNil2, argNil3) {
        timeseries <- ts(prices, frequency=period, start=c(0))
        }
        ''', prices, period)

    # numberperiods
    fullfunctionR('''
        f <- function(timeseries, period, argNil2, argNil3) {
        numberperiods <- length(timeseries) / period
        }
        ''', timeseries, period)

    holtwinters = fullfunctionR('''
        f <- function(timeseries, argNil1, argNil2, argNil3) {
        holtwinters = HoltWinters(timeseries)
        }
        ''', timeseries)

    # alpha
    timeseries = fullfunctionR('''
        f <- function(holtwinters, argNil1, argNil2, argNil3) {
        holtwinters$alpha
        }
        ''', holtwinters)

    # beta
    fullfunctionR('''
        f <- function(holtwinters, argNil1, argNil2, argNil3) {
        holtwinters$beta
        }
        ''', holtwinters)

    # gamma
    fullfunctionR('''
        f <- function(holtwinters, argNil1, argNil2, argNil3) {
        holtwinters$gamma
        }
        ''', holtwinters)

    forecast = fullfunctionR('''
        f <- function(holtwinters, period, argNil2, argNil3) {
        forecast = forecast.HoltWinters(holtwinters,h=period,level=c(80,95))
        }
        ''', holtwinters, period)

    x = fullfunctionR('''
        f <- function(forecast, argNil1, argNil2, argNil3) {
        x = forecast$x
        }
        ''', forecast)
    data = x[period:]

    model = fullfunctionR('''
        f <- function(forecast, argNil1, argNil2, argNil3) {
        model = forecast$fitted
        }
        ''', forecast)

    prediction = fullfunctionR('''
        f <- function(forecast, argNil1, argNil2, argNil3) {
        prediction = forecast$mean
        }
        ''', forecast)

    y = datos1Hora
    real = y[:period]

    lower = fullfunctionR('''
        f <- function(forecast, argNil1, argNil2, argNil3) {
        lower = forecast$lower
        }
        ''', forecast)

    upper = fullfunctionR('''
        f <- function(forecast, argNil1, argNil2, argNil3) {
        upper = forecast$upper
        }
        ''', forecast)

    return data, model, prediction, real, lower, upper

def fullfunctionR(docstring_r_function,res=0, dat=0, dat2=0, dat3=0):
    """funcionR
    Auxilary function to contruct a R function using robjects like a decorator
    """
    robjects.r(docstring_r_function)
    # r_f = robjects.globalenv['f']
    # print ''
    # print(r_f.r_repr())
    r_f = robjects.r['f']
    var = r_f(res, dat, dat2, dat3)
    # print ''
    # print var
    return var

def mongodbHWTES(collection, listSort, listPast, listFuture):
    """
    """
    # print ''
    # print 'MONGO DB'
    # print ''

    for jsontoinsert in listSort:
        fecha = jsontoinsert['fecha']
        # if jsontoinsert['hora'] == 0:
        #     print fecha.date()
        hora = jsontoinsert['hora']
        tipo = jsontoinsert['tipo']
        dayahead = jsontoinsert['dayahead']
        results = collection.find({ "fecha" : {"$in": [fecha]}, "hora": {"$in": [hora]}, "tipo": {"$in": [tipo]}, "dayahead": {"$in": [dayahead]} })
        if results.count() == 0:
            collection.insert(jsontoinsert)
        if results.count() == 1:
            collection.update({ "fecha" : {"$in" : [fecha]},
                                "hora" : {"$in" : [hora]},
                                "tipo" : {"$in" : [tipo]},
                                "dayahead" : {"$in" : [dayahead]},
                                },
                              { "$set" : jsontoinsert })
        if results.count() > 1:
            raise Exception('La base de datos tiene mas de un registro para la dada fecha.')

def hourHWTES(listDict, database, miHora):
    """hourHWTES

    listDict    This
    database    This is the mongo database Connection.
    miHora      This is the hour to perform method calculation

    """

    per = 28
    currentDate = datetime(datetime.now().year,datetime.now().month,datetime.now().day)
    DAYAHEAD = currentDate + timedelta(1)

    startDate0 = DAYAHEAD - timedelta(2*per)
    endDate0 = DAYAHEAD
    startDate1 = DAYAHEAD
    endDate1 = DAYAHEAD + timedelta(per)

    # if miHora == 0:
    #     print ''
    #     print 'MODELO HWTES'
    #     print ''
    #     print startDate0.date()
    #     print endDate0.date()
    #     print ''
    #     print startDate1.date()
    #     print endDate1.date()

    collection = database.precioses

    cursor = collection.find({"fecha": {"$gte": startDate0, "$lt": endDate0}, "hora": miHora}).sort("fecha",1)
    previousData = list()
    for element in cursor:
        previousData.append(element['PreciosES'])

    cursor = collection.find({"fecha": {"$gt": startDate1, "$lte": endDate1}, "hora": miHora})
    laterData = list()
    for element in cursor:
        laterData.append(element['PreciosES'])

    listaVector=studioHWTES(per,previousData,laterData,miHora)

    workingSet=listaVector[0]
    modelSet=listaVector[1]
    testeSet=listaVector[2]
    realSet=listaVector[3]
    lowerSet=listaVector[4]
    upperSet=listaVector[5]

    realSet = realSet[:per]

    workingSetPY = workingSet
    modelSetPY = modelSet
#     realSetPY = realSet
    testeSetPY = testeSet

    listPast = list()
    fecha = DAYAHEAD - timedelta(per*1)
    while fecha < endDate0:
        listPast.append(fecha)
        fecha = fecha + timedelta(1)

    listFuture = list()
    fecha = startDate1
    while fecha < endDate1:
        listFuture.append(fecha)
        fecha = fecha + timedelta(1)

    upper80=list()
    upper95=list()
    lower80=list()
    lower95=list()
    for indi5 in range(0,len(upperSet)/2):
        upper80.append(round(upperSet[indi5],2))
    for indi5 in range(len(upperSet)/2,len(upperSet)):
        upper95.append(round(upperSet[indi5],2))
    for indi6 in range(0,len(lowerSet)/2):
        lower80.append(round(lowerSet[indi6],2))
    for indi6 in range(len(lowerSet)/2,len(lowerSet)):
        lower95.append(round(lowerSet[indi6],2))

    indi = 0
    for indi in range(len(workingSetPY)):
        listDict.append({'fecha': listPast[indi], 'hora': miHora, 'PreciosES': workingSetPY[indi], 'tipo': 'working', 'dayahead': DAYAHEAD})
        listDict.append({'fecha': listPast[indi], 'hora': miHora, 'PreciosES': modelSetPY[indi], 'tipo': 'model', 'dayahead': DAYAHEAD})
        indi = indi + 1

    indi = 0
    for indi in range(len(testeSetPY)):
        listDict.append({'fecha': listFuture[indi], 'hora': miHora, 'PreciosES': testeSetPY[indi], 'tipo': 'teste', 'dayahead': DAYAHEAD})
#             listDict.append({'fecha': listFuture[indi], 'hora': miHora, 'PreciosES': realSetPY[indi], 'tipo': 'real', 'dayahead': DAYAHEAD})
        listDict.append({'fecha': listFuture[indi], 'hora': miHora, 'PreciosES': upper80[indi], 'tipo': 'upper80', 'dayahead': DAYAHEAD})
        listDict.append({'fecha': listFuture[indi], 'hora': miHora, 'PreciosES': upper95[indi], 'tipo': 'upper95', 'dayahead': DAYAHEAD})
        listDict.append({'fecha': listFuture[indi], 'hora': miHora, 'PreciosES': lower80[indi], 'tipo': 'lower80', 'dayahead': DAYAHEAD})
        listDict.append({'fecha': listFuture[indi], 'hora': miHora, 'PreciosES': lower95[indi], 'tipo': 'lower95', 'dayahead': DAYAHEAD})
        indi = indi + 1

    listW = list()
    listM = list()
    listT = list()
#     listR = list()
    listU8 = list()
    listU9 = list()
    listL8 = list()
    listL9 = list()

    for element in listDict:
        if element['tipo'] == 'working':
            listW.append(element)
        if element['tipo'] == 'model':
            listM.append(element)
        if element['tipo'] == 'teste':
            listT.append(element)
#         if element['tipo'] == 'real':
#             listR.append(element)
        if element['tipo'] == 'upper80':
            listU8.append(element)
        if element['tipo'] == 'upper95':
            listU9.append(element)
        if element['tipo'] == 'lower80':
            listL8.append(element)
        if element['tipo'] == 'lower95':
            listL9.append(element)

    listWsort = sorted(listW, key=itemgetter('fecha','hora'))
    listMsort = sorted(listM, key=itemgetter('fecha','hora'))
    listTsort = sorted(listT, key=itemgetter('fecha','hora'))
#     listRsort = sorted(listR, key=itemgetter('fecha','hora'))
    listU8sort = sorted(listU8, key=itemgetter('fecha','hora'))
    listU9sort = sorted(listU9, key=itemgetter('fecha','hora'))
    listL8sort = sorted(listL8, key=itemgetter('fecha','hora'))
    listL9sort = sorted(listL9, key=itemgetter('fecha','hora'))

    listWprice = list()
    listMprice = list()
    listTprice = list()
#     listRprice = list()
    listU8price = list()
    listU9price = list()
    listL8price = list()
    listL9price = list()
    for element in listWsort:
        listWprice.append(element['PreciosES'])
    for element in listMsort:
        listMprice.append(element['PreciosES'])
    for element in listTsort:
        listTprice.append(element['PreciosES'])
#     for element in listRsort:
#         listRprice.append(element['PreciosES'])
    for element in listU8sort:
        listU8price.append(element['PreciosES'])
    for element in listU9sort:
        listU9price.append(element['PreciosES'])
    for element in listL8sort:
        listL8price.append(element['PreciosES'])
    for element in listL9sort:
        listL9price.append(element['PreciosES'])

    return listWsort, listMsort, listTsort, listU8sort, listU9sort, listL8sort, listL9sort

def mainHWTES():
    """
    """
    listDict = list()

    database = Connection(host='mongodb://hmarrao:hmarrao@ds031117.mongolab.com:31117/mercadodiario').mercadodiario
    horasDelDia = range(24)
    for miHora in horasDelDia:
        listWsort, listMsort, listTsort, listU8sort, listU9sort, listL8sort, listL9sort = hourHWTES(listDict, database, miHora)

    listPast2 = listWsort[(28-7)*24:] + listMsort[(28-7)*24:]
    listFuture2 = listTsort[0:2*24] + listU8sort[0:2*24] + listU9sort[0:2*24] + listL8sort[0:2*24] + listL9sort[0:2*24]
    listSort = listPast2 + listFuture2

    collection = database.modelosHWTES
    mongodbHWTES(collection, listSort, listPast2, listFuture2)

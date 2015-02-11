# -*- coding: utf-8 -*-
"""arnn
auto regressive neural network
"""

import rpy2.robjects as robjects

from datetime import datetime, timedelta
from pymongo import Connection
from operator import itemgetter
from rpy2.robjects import FloatVector

# codigo necesario para importar el paquete arnn.R
f = file("/home/david/workspace/packagesR/arnn.R")
code = ''.join(f.readlines())
result = robjects.r(code)

# import R objects
from rpy2.robjects.packages import importr

# loading R packages
stats = importr('stats')
base = importr('base')
forecast = importr('forecast')

def studioARNN(lags2, per, vector, vector2):
    """studioARNN
    Realiza los calculos de modelado y prediccion HWTES

    Arguments:
        lags2: 2,3,4,...
        per: 28
        vector: [45.28, 51.54, 20.0, 44.38, 20.0, 44.08, 35.68, ... ]
        vector2: [42.67, 47.32, ...]

    Result:
        workingSet=listaVector[0]
        modelSet=listaVector[1]
        testeSet=listaVector[2]
        realSet=listaVector[3]
        lowerSet=listaVector[4]
        upperSet=listaVector[5]

    Notes of developers:

        lags: lista de regazos iniciales de la serie utilizados como entrada
        neu: numero de neuronas presentes en la capa oculta de la red neuronal
        w.max: rango de variacion
        restarts: repeticiones que realiza
        seed: semillas introducidas
        lambda: parametro de regularizacion
        maxit: numero que permite mayor dilatacion en las bandas verticales

        lags: no puede empezar en 0 y debe tener distinta longitud que la otra variable "neu"
                lo habitual es que la "neu" sea casi siempre menor que "lags" para evitar error
                e incluso a veces la diferencia es de 2 unidades, para que no de ningun error
                u otras veces necesita empezar en lags1 por 2 o 3, en vez de comunmente por 1
        neu y lags: numeros altos ralentizan la ejecucion, sobretodo para el parametro "neu",
                      y todavia es incierto, pero puede ser un valor mayor que otro, lo que si
                      parece ocurrir es que si neu<lags funciona pero si no debe ser neu>>>lags
        w.max: puede tomar valores menores a 2.0 pero conviene que este entre 0.0005 y 0.001
        restarts: lo tipico es que este entre 1 y 10, pero a mayor valor mayor tiempo tarda
        seed: puede tomar valores entre 1 y N, pero es preferible que este entre 1000 y 1500
        neu: si toma el valor 30, el modelo se ajusta mucho, pero los IC no son muy fiables,
               pero por ej, el valor 28 puede ser optimo en general, y nunca debe ser muy bajo
    """
    num = per + lags2

    workingSetRO = fullfunctionR('''
            f <- function(vectorTS, num, argNil2, argNil3) {
            # x <- ts(WWWusage, s=1, f=1)
            vectorTS[0:num]
            # x <- ts(vectorTS[0:num], s=1, f=1)
            x <- ts(vectorTS, s=1, f=1)
            }
            ''', vector, num, 0, 0)

    neu = 7
    lags1 = 1

    res_fit = fullfunctionR('''
            f <- function(x, lags1, lags2, neu) {
            # fit <- arnn(x=x, lags=lags1:lags2, isMLP=FALSE, H=neu, w.max=0.0005, restarts=1, seed=1500, lambda=0, optim.control=list(maxit=2000))
            fit <- arnn(x=x, lags=lags1:lags2, H=neu)
            }
            ''', workingSetRO, lags1, lags2, neu)

    # information about the fitted model
    #     robjects.r(
    #             '''
    #             f <- function(fit, argNil, argNil2, argNil3) {
    #             summary(fit)
    #             }
    #             ''')
    #     res_summary = funcionR(res_fit, 0, 0, 0)


    # in-sample errors
    # robjects.r(
    #         '''
    #         f <- function(fit, argNil, argNil2, argNil3) {
    #         accuracy(fit)
    #         }
    #         ''')
    # res_fit_accuracy = funcionR(res_fit, 0, 0, 0)

    res_fit1 = fullfunctionR('''
            f <- function(vectorTS, fit, argNil2, argNil3) {
            fit1 <- arnn(x=vectorTS, model=fit)
            }
            ''', workingSetRO, res_fit, 0, 0)

    # one-step forecasts
    # robjects.r(
    #         '''
    #         f <- function(fit, argNil, argNil2, argNil3) {
    #         fitted(fit)
    #         }
    #         ''')
    # fit = funcionR(res_fit, 0, 0, 0)

    # workingSet
    workingSetRO = fullfunctionR('''
            f <- function(fit, argNil, argNil2, argNil3) {
            fit$x
            }
            ''', res_fit, 0, 0, 0)

    # Se acorta el vector workingSet en tantas posiciones como valor tenga lags2
    workingSetRO = workingSetRO[lags2:]

    con = 0
    workingSetPY = list()
    for indiceWS in range(len(workingSetRO)):
        workingSetPY.append(workingSetRO[con])
        con = con + 1

    # modelSet
    modelSetRO = fullfunctionR('''
            f <- function(fit, fit1, argNil2, argNil3) {
            #fit$fitted
            #fitted(fit1)
            fitted(fit)
            }
            ''', res_fit, res_fit1, 0, 0)

    con = 0
    modelSetPY = list()
    for indiceWS in range(len(modelSetRO)):
        modelSetPY.append(modelSetRO[con])
        con = con + 1

    # accuracy and fitted
    # robjects.r(
    #         '''
    #         f <- function(vectorTS, fit1, argNil2, argNil3) {
    #         accuracy(fitted(fit1)[76:96], vectorTS[81:100])
    #         }
    #         ''')
    # res_fit1_accuracy = funcionR(workingSet, res_fit1, 0, 0)

    intCon1 = 80
    intCon2 = 95
    res_fore = fullfunctionR(
            '''
            f <- function(fit, per, intCon1, intCon2) {
            #fore <- forecast(fit, h=per, level=c(intCon1,intCon2), fan=FALSE, bootstrap=FALSE, seed=1234, npaths=1000)
            #fore <- forecast(fit, h=per, level=c(intCon1,intCon2), fan=FALSE, bootstrap=FALSE, seed=1500)
            #fore <- forecast(fit, h=per, level=c(intCon1,intCon2), fan=FALSE, bootstrap=FALSE, seed=1234, npaths=1000)
            #fore <- forecast(fit, h=per, level=c(intCon1,intCon2), fan=FALSE, bootstrap=FALSE, seed=1500, npaths=1000)
            fore <- forecast(fit, h=per, level=c(intCon1,intCon2))
            }
            ''', res_fit, per, intCon1, intCon2)

    # realSet
    realSetRO = fullfunctionR('''
            f <- function(vector2, per, argNil2, argNil3) {
            vector2[0:per]
            # x <- ts(vector2[0:per], s=(num+1), f=1)
            x <- ts(vector2[0:per], s=1, f=1)
            }
            ''', vector2, per, 0, 0)

    con = 0
    realSetPY = list()
    for indiceWS in range(len(realSetRO)):
        realSetPY.append(realSetRO[con])
        con = con + 1

    # testeSet
    testeSetRO = fullfunctionR('''
            f <- function(fore, argNil, argNil2, argNil3) {
            fore$mean
            }
            ''', res_fore, 0, 0, 0)

    con = 0
    testeSetPY = list()
    for indiceWS in range(len(testeSetRO)):
        testeSetPY.append(testeSetRO[con])
        con = con + 1

    # lowerSet
    lowerSet = fullfunctionR(
            '''
            f <- function(fore, argNil1, argNil2, argNil3) {
            #lowerSet <- fore[8]
            lowerSet <- fore$lower
            }
            ''', res_fore, 0, 0, 0)

    # upperSet
    upperSet = fullfunctionR('''
            f <- function(fore, argNil1, argNil2, argNil3) {
            #lowerSet <- fore[9]
            upperSet <- fore$upper
            }
            ''', res_fore, 0, 0, 0)

    listaVector = [per, lags2, realSetRO, testeSetRO, workingSetPY, modelSetPY, testeSetPY, realSetPY, upperSet, lowerSet]
    return listaVector

def fullfunctionR(docstring_r_function,res=0, dat=0, dat2=0, dat3=0):
    """fullfuncionR
    Auxilary function to contruct a R function using robjects like a decorator

    Arguments:
        docstring_r_function: argumento que varia en funcion del uso que se le de

    Result:
        a function interface with R defined function at docstring_r_function.
        the type is a rpy2.robjects + the needed class to operate with the R implemented function.

    Notes of developers:
        A esta funcion no se le puede pasar un arg None, porque no reconoce dicho tipo de dato
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

def mongodbARNN(collection, listSort, listPast, listFuture):
    '''mongodbARNN
    Gestiona la carga de datos en mongodb

    Arguments:
        collection: nombre de la coleccion
        listSort: todos los datos ordenados
        listPast: datos de trabajo y modelado anteriores al dayaheadNN
        listFuture: datos predichos posteriores al dayaheadNN

    Result:
        Inserta informacion en base de datos
    '''
    print 'MONGO DB'
    print ''
    # print DAYAHEAD.date()
    # print ''

    for jsontoinsert in listSort:
        fecha = jsontoinsert['fecha']
        if jsontoinsert['hora'] == 0:
            print fecha.date()
        hora = jsontoinsert['hora']
        tipo = jsontoinsert['tipo']
        dayahead = jsontoinsert['dayaheadNN']
        results = collection.find({ "fecha" : {"$in": [fecha]}, "hora": {"$in": [hora]}, "tipo": {"$in": [tipo]}, "dayaheadNN": {"$in": [dayahead]} })
        if results.count() == 0:
            collection.insert(jsontoinsert)
        if results.count() == 1:
            collection.update({ "fecha" : {"$in" : [fecha]},
                                "hora" : {"$in" : [hora]},
                                "tipo" : {"$in" : [tipo]},
                                "dayaheadNN" : {"$in" : [dayahead]},
                                },
                              { "$set" : jsontoinsert })
        if results.count() > 1:
            raise Exception('La base de datos tiene mas de un registro para la dada fecha.')

def hourARNN(listDict, database, miHora):
    """hourARNN
    Descarga datos de precios, los trata a traves de la funcion studioHWTES y los reordena asignandoles una fecha

    Arguments:
        listDict    Esta es una lista auxiliar para tratar los valores de los precios
        database    This is the mongo database Connection
        miHora      This is the hour to perform method calculation

    Result:
        Devuelve una lista de vectores de precios tratados e intervalos de confianza
    """

    print ''
    print 'miHora'
    print miHora

    # lags2 = 2, 3, 4
    lags2 = 3
    per = 28

    currentDate = datetime(datetime.now().year,datetime.now().month,datetime.now().day)
    # En la bbdd de mongodb el dayahead para el metodomv  arnn se llama dayaheadNN
    DAYAHEAD = currentDate + timedelta(1)

    startDate0 = DAYAHEAD - timedelta(per) - timedelta(lags2)
    endDate0 = DAYAHEAD
    startDate1 = DAYAHEAD
    endDate1 = DAYAHEAD + timedelta(per)

    collection = database.precioses

    cursor = collection.find({"fecha": {"$gte": startDate0, "$lt": endDate0}, "hora": miHora})
    previousData = list()
    for element in cursor:
        previousData.append(element['PreciosES'])

    cursor = collection.find({"fecha": {"$gt": startDate1, "$lte": endDate1}, "hora": miHora})
    laterData = list()
    for element in cursor:
        laterData.append(element['PreciosES'])

    precios = previousData
    vector = FloatVector(precios)
    precios2 = laterData
    vector2 = FloatVector(precios2)

    listaVector = studioARNN(lags2, per, vector, vector2)

    per = listaVector[0]
    lags2 = listaVector[1]

    # realSetRO = listaVector[2]
    # testeSetRO = listaVector[3]

    workingSetPY = listaVector[4]
    modelSetPY = listaVector[5]
    testeSetPY = listaVector[6]
    # realSetPY = listaVector[7]
    upperSet = listaVector[8]
    lowerSet = listaVector[9]

    # lower
    lowerData = FloatVector(lowerSet)
    lowerLength = len(lowerData)

    lower80 = list()
    for index in range(0,lowerLength/2):
        lower80.append(round(lowerData[index],2))

    lower95 = list()
    for index in range(lowerLength/2,lowerLength):
        lower95.append(round(lowerData[index],2))

    # uppper
    upperData = FloatVector(upperSet)
    upperLength = len(upperData)

    upper80 = list()
    for index in range(0,upperLength/2):
        upper80.append(round(upperData[index],2))

    upper95 = list()
    for index in range(upperLength/2,upperLength):
        upper95.append(round(upperData[index],2))

    listPast = list()
    # Tiene que contener un periodo menos, que se usa para modelar
    fecha = DAYAHEAD - timedelta(per*1)
    # Si la condicion contiene un igual, toma un valor mas que el correspondiente al periodo de 28
    while fecha < endDate0:
        listPast.append(fecha)
        fecha = fecha + timedelta(1)

    listFuture = list()
    fecha = startDate1
    while fecha < endDate1:
        listFuture.append(fecha)
        fecha = fecha + timedelta(1)

    # Para las 24 horas del dia, uno los datos para que esten a nivel diario y se puedan graficar
    indi = 0
    for indi in range(len(workingSetPY)):
        listDict.append({'fecha': listPast[indi], 'hora': miHora, 'PreciosES': workingSetPY[indi], 'tipo': 'working', 'dayaheadNN': DAYAHEAD})
        listDict.append({'fecha': listPast[indi], 'hora': miHora, 'PreciosES': modelSetPY[indi], 'tipo': 'model', 'dayaheadNN': DAYAHEAD})
        indi = indi + 1
    indi = 0
    for indi in range(len(testeSetPY)):
        listDict.append({'fecha': listFuture[indi], 'hora': miHora, 'PreciosES': testeSetPY[indi], 'tipo': 'teste', 'dayaheadNN': DAYAHEAD})
        # listDict.append({'fecha': listFuture[indi], 'hora': miHora, 'PreciosES': realSetPY[indi], 'tipo': 'real', 'dayaheadNN': DAYAHEAD})
        listDict.append({'fecha': listFuture[indi], 'hora': miHora, 'PreciosES': upper80[indi], 'tipo': 'upper80', 'dayaheadNN': DAYAHEAD})
        listDict.append({'fecha': listFuture[indi], 'hora': miHora, 'PreciosES': upper95[indi], 'tipo': 'upper95', 'dayaheadNN': DAYAHEAD})
        listDict.append({'fecha': listFuture[indi], 'hora': miHora, 'PreciosES': lower80[indi], 'tipo': 'lower80', 'dayaheadNN': DAYAHEAD})
        listDict.append({'fecha': listFuture[indi], 'hora': miHora, 'PreciosES': lower95[indi], 'tipo': 'lower95', 'dayaheadNN': DAYAHEAD})
        indi = indi + 1

    listW = list()
    listM = list()
    listT = list()
    # listR = list()
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
        # if element['tipo'] == 'real':
        #     listR.append(element)
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
    # listRsort = sorted(listR, key=itemgetter('fecha','hora'))
    listU8sort = sorted(listU8, key=itemgetter('fecha','hora'))
    listU9sort = sorted(listU9, key=itemgetter('fecha','hora'))
    listL8sort = sorted(listL8, key=itemgetter('fecha','hora'))
    listL9sort = sorted(listL9, key=itemgetter('fecha','hora'))

    listWprice = list()
    listMprice = list()
    listTprice = list()
    # listRprice = list()
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
    # for element in listRsort:
    #     listRprice.append(element['PreciosES'])
    for element in listU8sort:
        listU8price.append(element['PreciosES'])
    for element in listU9sort:
        listU9price.append(element['PreciosES'])
    for element in listL8sort:
        listL8price.append(element['PreciosES'])
    for element in listL9sort:
        listL9price.append(element['PreciosES'])

        return listWsort, listMsort, listTsort, listU8sort, listU9sort, listL8sort, listL9sort

def mainARNN():
    """mainHWTES
    Se encarga de definir la bbdd, llamar a las funciones del codigo y finalmente selecciona parte de los datos
    """
    listDict = list()
    database = Connection(host='mongodb://hmarrao:hmarrao@ds031117.mongolab.com:31117/mercadodiario').mercadodiario
    horasDelDia = range(24)
    for miHora in horasDelDia:
        listWsort, listMsort, listTsort, listU8sort, listU9sort, listL8sort, listL9sort = hourARNN(listDict, database, miHora)

    # si limito la carga en base de datos a una semana
    listPast2 = listWsort[(28-7)*24:] + listMsort[(28-7)*24:]
    # si limito la carga en base de datos a dos dias
    listFuture2 = listTsort[0:2*24] + listU8sort[0:2*24] + listU9sort[0:2*24] + listL8sort[0:2*24] + listL9sort[0:2*24]
    listSort = listPast2 + listFuture2

    collection = Connection(host=None).mercadodiario.modelosARNN
    mongodbARNN(collection, listSort, listPast2, listFuture2)

# -*- coding: utf-8 -*-
'''
Created on 15/07/2014
@author: hmarrao & david
'''
# SERVER
from bottle import route, template

# LOCAL
from datetime import datetime
from priceprofor_graficas import preciosDiarios, tecnologiasDiarias
from priceprofor_graficas import findLastDayDocument, findLastDayDocumentTechnology, findLastDayDocumentThree
from priceprofor_graficas import relativeExtremes, colorChart, averageList, lineChart
from priceprofor_graficas import lineChartMulti, lineChartMultiPrice
from omelinfosys.reehandlers import getdemandeforcast, getpreveoldd
from omelinfosys.dbstudydatamanager import DBRawData
from priceprofor_estadisticas import estadisticasPrecios, estadisticasTecnologias

# from sys import exit
# exit(0)

# # Otra forma de definir un controlador
# route('/PreciosHorariosAlt', method='GET',callback=precioshorarios)

def maxList(priceList):
    '''
    '''
    maximo = max(priceList)
    maxIndexList = list()
    for index in range(len(priceList)):
        if priceList[index] == maximo:
            maxValue = priceList[index]
            maxIndexList.append(index)
#             maxIndexList.append(timeFormat(index))
#             maxIndexList.append(dosDigitos(index))
    return {'precio': maxValue, 'hora': maxIndexList}

def minList(priceList):
    '''
    '''
    minimo = min(priceList)
    minIndexList = list()
    for index in range(len(priceList)):
        if priceList[index] == minimo:
            minValue = priceList[index]
            minIndexList.append(index)
#             minIndexList.append(timeFormat(index))
#             minIndexList.append(dosDigitos(index))
    return {'precio': minValue, 'hora': minIndexList}

# def dosDigitos(num):
#     '''
#     '''
#     strNum = str(num)
#     if len(strNum)==1:
#         return '0'+str(strNum)
#     else:
#         return strNum

# def timeFormat(hours, minutes=0, seconds=0):
#     '''
#     '''
#     # return "%02d:%02d:%02d" % (hours, minutes, seconds)
#     return "%02d:%02d" % (hours, minutes)

@route('/PreciosHorarios', method='GET')
def precioshorarios():
    """
    """

    '''
    dejar la tabla sola y la pantalla de dos graficas y tabla igual ambas que la del ultimo dia en html
    corregir la precision a dos decimales de los precios en la grafica de modelos de prediccion
    ha de haber 2 metodos de find last document dependiendo de si son precios o tecnologias
    '''

    ''' DATETIME '''
    pricesDT = findLastDayDocument()
#     pricesDT = datetime(2014,7,12)

    ''' PRICES '''
    dic = preciosDiarios(pricesDT)
    minmax = relativeExtremes(dic)

    precios = list()
    for element in dic['precios']:
        precios.append(element[1])
    precios.pop(0)

    preciosList = colorChart(pricesDT, minmax)
    vector = list()
    for element in range(1,len(dic['precios'])):
        vector.append(dic['precios'][element][1])
    meanList = averageList(vector)
    preciosList = lineChart(pricesDT, preciosList, meanList)

    priceMIN=minList(precios)['precio']
    priceMAX=maxList(precios)['precio']
    hoursMIN=minList(precios)['hora']
    hoursMAX=maxList(precios)['hora']

    ''' TECHNOLOGIES '''
    technologyDT = findLastDayDocumentTechnology()
    dic = tecnologiasDiarias(technologyDT)
    tecnologiasList = dic['tecnologias']

    ''' FORECASTS '''
    previsionEolicaList = getpreveoldd(technologyDT)
    previsionDemandaList = getdemandeforcast(technologyDT)

    ins = DBRawData()
    ins.set_fecha(technologyDT)
    ins.getDataFromWeb()
    energiaGestionadaList = ins.ProduccionyDemandaES['TOTAL_DEMANDA']

    return template('priceprofor_precios_horarios', pricesDT=pricesDT, technologyDT=technologyDT,
                    minmax=minmax, priceMIN=priceMIN, priceMAX=priceMAX, hoursMIN=hoursMIN, hoursMAX=hoursMAX,
                    preciosList=preciosList, meanList=meanList,
                    tecnologiasList=tecnologiasList, energiaGestionadaList=energiaGestionadaList,
                    previsionEolicaList=previsionEolicaList, previsionDemandaList=previsionDemandaList)

@route('/PreciosHorariosUltimoDia', method='GET')
def precioshorariosultimodia():
    """
    """

    ''' DATETIME '''
    pricesDT = findLastDayDocument()
#     pricesDT = datetime(2014,7,12)

    ''' PRICES '''
    dic = preciosDiarios(pricesDT)
    minmax = relativeExtremes(dic)

    precios = list()
    for element in dic['precios']:
        precios.append(element[1])
    precios.pop(0)

    preciosList = colorChart(pricesDT, minmax)
    vector = list()
    for element in range(1,len(dic['precios'])):
        vector.append(dic['precios'][element][1])
    meanList = averageList(vector)
    preciosList = lineChart(pricesDT, preciosList, meanList)

    priceMIN=minList(precios)['precio']
    priceMAX=maxList(precios)['precio']
    hoursMIN=minList(precios)['hora']
    hoursMAX=maxList(precios)['hora']

    return template('priceprofor_precios_horarios_ultimo_dia', pricesDT=pricesDT,
                    minmax=minmax, priceMIN=priceMIN, priceMAX=priceMAX, hoursMIN=hoursMIN, hoursMAX=hoursMAX,
                    preciosList=preciosList, meanList=meanList
                    )

@route('/EnergiaGestionada', method='GET')
def energiagestionada():
    """
    """

    ''' DATETIME '''
    technologyDT = findLastDayDocumentTechnology()
#     technologyDT = datetime(2014,7,12)

    ''' PRICES '''
    dic = preciosDiarios(technologyDT)
    minmax = relativeExtremes(dic)

    precios = list()
    for element in dic['precios']:
        precios.append(element[1])
    precios.pop(0)

    preciosList = colorChart(technologyDT, minmax)
    vector = list()
    for element in range(1,len(dic['precios'])):
        vector.append(dic['precios'][element][1])
    meanList = averageList(vector)
    preciosList = lineChart(technologyDT, preciosList, meanList)

#     priceMIN=minList(precios)['precio']
#     priceMAX=maxList(precios)['precio']
#     hoursMIN=minList(precios)['hora']
#     hoursMAX=maxList(precios)['hora']

    ''' FORECASTS '''
    previsionEolicaList = getpreveoldd(technologyDT)
    previsionDemandaList = getdemandeforcast(technologyDT)

    ins = DBRawData()
    ins.set_fecha(technologyDT)
    ins.getDataFromWeb()
    energiaGestionadaList = ins.ProduccionyDemandaES['TOTAL_DEMANDA']

    return template('priceprofor_energia_gestionada', technologyDT=technologyDT,
                    preciosList=preciosList, meanList=meanList,
                    energiaGestionadaList=energiaGestionadaList,
                    previsionEolicaList=previsionEolicaList, previsionDemandaList=previsionDemandaList)

<<<<<<< HEAD
''' este error significa que no reconoce la letra del abecedario que va despues de la "n" '''
# SyntaxError: Non-ASCII character '\xc3' in file wsgi/controllers/priceprofor_precioshorarios.py on line 240, but no encoding declared; see http://www.python.org/peps/pep-0263.html for details

@route('/EstadisticasPrecios', method='GET')
def estadisticasprecios():
    """
    """

    ''' DATETIME '''
    technologyDT = findLastDayDocumentTechnology()
#     technologyDT = datetime(2014,7,12)

    ''' PRICES '''
    dic = preciosDiarios(technologyDT)
    minmax = relativeExtremes(dic)

    precios = list()
    for element in dic['precios']:
        precios.append(element[1])
    precios.pop(0)

    preciosList = colorChart(technologyDT, minmax)
    vector = list()
    for element in range(1,len(dic['precios'])):
        vector.append(dic['precios'][element][1])
    meanList = averageList(vector)
    preciosList = lineChart(technologyDT, preciosList, meanList)

#     priceMIN=minList(precios)['precio']
#     priceMAX=maxList(precios)['precio']
#     hoursMIN=minList(precios)['hora']
#     hoursMAX=maxList(precios)['hora']

    ''' FORECASTS '''
    previsionEolicaList = getpreveoldd(technologyDT)
    previsionDemandaList = getdemandeforcast(technologyDT)

    ins = DBRawData()
    ins.set_fecha(technologyDT)
    ins.getDataFromWeb()
    energiaGestionadaList = ins.ProduccionyDemandaES['TOTAL_DEMANDA']

#     periodoOrdinal = ["A", "B", "C", "C",
#                       "D", "D", "E", "E"]

    periodoTemporal = ["Dia actual", "Dia anterior", "Semana actual", "Semana anterior", "Mes actual", "Mes anterior",
                       "Estacion actual", "Estacion anterior", "Año actual", "Año anterior"]

    promediosDesde = estadisticasPrecios()[1]
    promediosHasta = estadisticasPrecios()[2]

    periodoDesde = [promediosDesde[0].date(), promediosDesde[1].date(), promediosDesde[2].date(), promediosDesde[3].date(), promediosDesde[4].date(),
                    promediosDesde[5].date(), promediosDesde[6].date(), promediosDesde[7].date(), promediosDesde[8].date(), promediosDesde[9].date()]

    periodoHasta = [promediosHasta[0].date(), promediosHasta[1].date(), promediosHasta[2].date(), promediosHasta[3].date(), promediosHasta[4].date(),
                    promediosHasta[5].date(), promediosHasta[6].date(), promediosHasta[7].date(), promediosHasta[8].date(), promediosHasta[9].date()]

    promediosPrecios = estadisticasPrecios()[0]

#     print periodoTemporal
#     print promediosPrecios

    return template('priceprofor_estadisticas_precios', technologyDT=technologyDT,
                    preciosList=preciosList, meanList=meanList,
                    energiaGestionadaList=energiaGestionadaList,
                    previsionEolicaList=previsionEolicaList, previsionDemandaList=previsionDemandaList,
                    periodoDesde=periodoDesde, periodoHasta=periodoHasta, periodoTemporal=periodoTemporal, promediosPrecios=promediosPrecios)

@route('/EstadisticasTecnologias', method='GET')
def estadisticastecnologias():
    """
    """

    ''' DATETIME '''
    technologyDT = findLastDayDocumentTechnology()
#     technologyDT = datetime(2014,7,12)

    ''' PRICES '''
    dic = preciosDiarios(technologyDT)
    minmax = relativeExtremes(dic)

    precios = list()
    for element in dic['precios']:
        precios.append(element[1])
    precios.pop(0)

    preciosList = colorChart(technologyDT, minmax)
    vector = list()
    for element in range(1,len(dic['precios'])):
        vector.append(dic['precios'][element][1])
    meanList = averageList(vector)
    preciosList = lineChart(technologyDT, preciosList, meanList)

#     priceMIN=minList(precios)['precio']
#     priceMAX=maxList(precios)['precio']
#     hoursMIN=minList(precios)['hora']
#     hoursMAX=maxList(precios)['hora']

    ''' FORECASTS '''
    previsionEolicaList = getpreveoldd(technologyDT)
    previsionDemandaList = getdemandeforcast(technologyDT)

    ins = DBRawData()
    ins.set_fecha(technologyDT)
    ins.getDataFromWeb()
    energiaGestionadaList = ins.ProduccionyDemandaES['TOTAL_DEMANDA']

#     periodoOrdinal = ["A", "B", "C", "C",
#                       "D", "D", "E", "E"]

    periodoTemporal = ["Dia actual", "Dia anterior", "Semana actual", "Semana anterior", "Mes actual", "Mes anterior",
                       "Estacion actual", "Estacion anterior", "Año actual", "Año anterior"]

    promediosDesde = estadisticasTecnologias()[6]
    promediosHasta = estadisticasTecnologias()[7]

    periodoDesde = [promediosDesde[0].date(), promediosDesde[1].date(), promediosDesde[2].date(), promediosDesde[3].date(), promediosDesde[4].date(),
                    promediosDesde[5].date(), promediosDesde[6].date(), promediosDesde[7].date(), promediosDesde[8].date(), promediosDesde[9].date()]

    periodoHasta = [promediosHasta[0].date(), promediosHasta[1].date(), promediosHasta[2].date(), promediosHasta[3].date(), promediosHasta[4].date(),
                    promediosHasta[5].date(), promediosHasta[6].date(), promediosHasta[7].date(), promediosHasta[8].date(), promediosHasta[9].date()]

    promediosTecnologias = estadisticasTecnologias()[0:6]

#     print periodoTemporal
#     print promediosPrecios

    return template('priceprofor_estadisticas_tecnologias', technologyDT=technologyDT,
                    preciosList=preciosList, meanList=meanList,
                    energiaGestionadaList=energiaGestionadaList,
                    previsionEolicaList=previsionEolicaList, previsionDemandaList=previsionDemandaList,
                    periodoDesde=periodoDesde, periodoHasta=periodoHasta, periodoTemporal=periodoTemporal, promediosTecnologias=promediosTecnologias)

=======
>>>>>>> cff9831602d1b2bbe1bac8186a6d6d467dc96a7e
@route('/EnergiaGestionadaValores', method='GET')
def energiagestionadavalores():
    """
    son los valores de energia absolutos de tecnologias
    """

    ''' DATETIME '''
#     pricesDT = findLastDayDocument()
    pricesDT = findLastDayDocumentThree()
    technologyDT = findLastDayDocumentTechnology()
#     pricesDT = datetime(2014,7,12)

    ''' PRICES '''
    dic = preciosDiarios(pricesDT)
    minmax = relativeExtremes(dic)

    precios = list()
    for element in dic['precios']:
        precios.append(element[1])
    precios.pop(0)

    preciosList = colorChart(pricesDT, minmax)
    vector = list()
    for element in range(1,len(dic['precios'])):
        vector.append(dic['precios'][element][1])

    ''' FORECASTS '''
    previsionEolicaList = getpreveoldd(technologyDT)
    previsionDemandaList = getdemandeforcast(technologyDT)

    ins = DBRawData()
    ins.set_fecha(technologyDT)
    ins.getDataFromWeb()
    energiaGestionadaList = ins.ProduccionyDemandaES['TOTAL_DEMANDA']

    meanList = averageList(vector)
    # preciosList = lineChartMulti(pricesDT, preciosList, meanList, previsionEolicaList, previsionDemandaList, energiaGestionadaList)
    preciosList = lineChartMulti(technologyDT, preciosList, meanList, previsionEolicaList, previsionDemandaList, energiaGestionadaList)

#     priceMIN=minList(precios)['precio']
#     priceMAX=maxList(precios)['precio']
#     hoursMIN=minList(precios)['hora']
#     hoursMAX=maxList(precios)['hora']

    return template('priceprofor_energia_gestionada_valores', pricesDT=pricesDT, technologyDT=technologyDT,
                    # minmax=minmax, priceMIN=priceMIN, priceMAX=priceMAX, hoursMIN=hoursMIN, hoursMAX=hoursMAX,
                    preciosList=preciosList, meanList=meanList
                    )

@route('/EnergiaGestionadaCoeficientes', method='GET')
def energiagestionadacoeficientes():
    """
    son los valores de energia relativos de tecnologias
    al final se ha mantenido el periodo dia (no semana)
    """

    ''' DATETIME '''
#     pricesDT = findLastDayDocument()
    pricesDT = findLastDayDocumentThree()
#     pricesDT = datetime(2014,7,12)

    technologyDT = findLastDayDocumentTechnology()
#     technologyDT = datetime(2014,1,5)

    ''' demanda > gestionada '''
#     technologyDT = datetime(2014,1,1)
    ''' demanda = gestionada '''
#     technologyDT = datetime(2014,3,1)
    ''' demanda < gestionada '''
#     technologyDT = datetime(2014,4,1)

    ''' PRICES '''
    dic = preciosDiarios(pricesDT)
    minmax = relativeExtremes(dic)

    precios = list()
    for element in dic['precios']:
        precios.append(element[1])
    precios.pop(0)

    preciosList = colorChart(pricesDT, minmax)
    vector = list()
    for element in range(1,len(dic['precios'])):
        vector.append(dic['precios'][element][1])

    ''' FORECASTS '''
    previsionEolicaList = getpreveoldd(technologyDT)
    previsionDemandaList = getdemandeforcast(technologyDT)

    ins = DBRawData()
    ins.set_fecha(technologyDT)
    ins.getDataFromWeb()
    energiaGestionadaList = ins.ProduccionyDemandaES['TOTAL_DEMANDA']

    meanList = averageList(vector)
    # preciosList = lineChartMulti(pricesDT, preciosList, meanList, previsionEolicaList, previsionDemandaList, energiaGestionadaList)
    preciosList = lineChartMultiPrice(technologyDT, preciosList, meanList, previsionEolicaList, previsionDemandaList, energiaGestionadaList)

#     priceMIN=minList(precios)['precio']
#     priceMAX=maxList(precios)['precio']
#     hoursMIN=minList(precios)['hora']
#     hoursMAX=maxList(precios)['hora']

    return template('priceprofor_energia_gestionada_coeficientes', pricesDT=pricesDT, technologyDT=technologyDT,
                    # minmax=minmax, priceMIN=priceMIN, priceMAX=priceMAX, hoursMIN=hoursMIN, hoursMAX=hoursMAX,
                    preciosList=preciosList, meanList=meanList
                    )

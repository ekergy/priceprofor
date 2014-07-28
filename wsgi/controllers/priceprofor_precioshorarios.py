'''
Created on 15/07/2014
@author: hmarrao & david
'''
# SERVER
from bottle import route, template

# LOCAL
from datetime import datetime
from priceprofor_graficas import preciosDiarios, tecnologiasDiarias
from priceprofor_graficas import findLastDayDocument, findLastDayDocumentTechnology
from priceprofor_graficas import relativeExtremes, colorChart, averageList, lineChart
from omelinfosys.reehandlers import getdemandeforcast, getpreveoldd
from omelinfosys.dbstudydatamanager import DBRawData

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
    @TODO:
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

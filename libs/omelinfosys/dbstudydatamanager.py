# -*- coding: utf-8 -*-
'''
Created on 02/2013
@author: hmarrao & david
'''
from pymongo import Connection
from datetime import datetime, timedelta
from dbrawdatamanager import DBRawData
from datosEnFaltaEnergias import centralEuropeanTime, datosEnFalta, diasEnFalta
from omelinfosys.omelhandlers import ProduccionMibelHandler
from utilities import omieproduccionurl
from urllib2 import urlopen
# from utilities import validafecha

'''
{'PreciosES': {'vector_vacio': []},
 'PrevisionDemandaES': {'elemento_cero': [datetime.datetime(2011, 3, 7, 0, 0),
   datetime.datetime(2011, 3, 8, 0, 0),
   datetime.datetime(2011, 3, 19, 0, 0),
   datetime.datetime(2011, 4, 21, 0, 0),
   datetime.datetime(2011, 5, 2, 0, 0),
   datetime.datetime(2011, 8, 19, 0, 0)],
  'vector_vacio': [datetime.datetime(2011, 4, 23, 0, 0)]},
 'PrevisionEolicaES': {'elemento_cero': [], 'vector_vacio': []},
 'ProduccionyDemandaES': {'fecha_vacia': []},
 'fecha': {'cambio_hora': [datetime.datetime(2011, 3, 27, 0, 0),
   datetime.datetime(2011, 10, 30, 0, 0),
   datetime.datetime(2012, 3, 25, 0, 0),
   datetime.datetime(2012, 10, 28, 0, 0),
   datetime.datetime(2013, 3, 31, 0, 0),
   datetime.datetime(2013, 10, 27, 0, 0)]}}
'''

'''
en local, el siguiente metodo actualiza manualmente la base de datos de precios y tecnologias
'''

'''
ConnectionFailure: could not connect to ds031117.mongolab.com:31117: timed out

este error es porque no se puede acceder a la base de datos de openshift temporalmente
'''

# from sys import path
# path.append('libs')

# from datetime import datetime
# startDate = datetime(2011,1,1)
# endDate = datetime(2013,12,31)

# from omelinfosys.dbstudydatamanager import populateStudyData
# populateStudyData(startDate,endDate)
# populateStudyData(startDate)
# populateStudyData()
def populateStudyData(startDate=None, endDate=None):
    '''
    TECNOLOGIAS actualiza la base de datos de TECNOLOGIAS del servidor

    Metodos de usabilidad con las clases definidas
    This Method will performe the following operations:data = response.read()
    1st:    Gathering informacion of StudyDataES collection. Last data inserted.
    2nd:    Gathering informacion of RawData collection. Last data available.
    3rd:    Study data won't take into account the change of hour days with the following logic:
            23 hours day: hour 3 will be replicated.
            25 hours day: hour 3 will be removed.
    Sustituimos el nombre TOTAL_DEMANDA por el de ENERGIA_GESTIONADA segun se define en la web de
    http://www.esios.ree.es/web-publica/
    '''
    try:
        # ONEHOUR = timedelta(seconds=3600)
        ONEDAY = timedelta(1)
        if startDate == None:
            startDate = findLastStudyDocument()
        # Disponemos de los datos de la web de la "REE" con 3 dias de retraso
        currentDate = datetime(datetime.now().year,datetime.now().month,datetime.now().day)
        if endDate == None:
            if startDate == currentDate:
                endDate = currentDate
            elif startDate == currentDate - timedelta(1):
                endDate = startDate - timedelta(1)
            elif startDate == currentDate - timedelta(2):
                endDate = startDate - timedelta(2)
            else:
                endDate = currentDate - timedelta(3)
    except:
        raise
    else:
        listCHV = list()
        listCHI = list()
        for indi in range(endDate.year - startDate.year + 1):
            fechaCHV, fechaCHI = centralEuropeanTime(startDate.year + indi)
            listCHV.append(fechaCHV)
            listCHI.append(fechaCHI)

        emptyPD, zeroPD = diasEnFalta()
        listDT = emptyPD + zeroPD
        iterDate = startDate
        while (endDate >= iterDate):
            print iterDate.date()

            ins_raw = DBRawData()
            # print ins_raw.getCollection()
            ins_raw.set_fecha(iterDate)
            ins_raw.getDataFromWeb()

            ''' si no hay datos en la base de datos falla '''

            for i in range(24):
                ins_study = DBStudyData()
                # print ins_study.getCollection()
                ins_study.fecha = iterDate
                ins_study.hora = i

                ''' PRODUCCION '''
                ins_study.NUCLEAR = ins_raw.ProduccionyDemandaES['NUCLEAR'][i]
                ins_study.HIDRAULICA_CONVENCIONAL = ins_raw.ProduccionyDemandaES['HIDRAULICA_CONVENCIONAL'][i]
                ins_study.REGIMEN_ESPECIAL = ins_raw.ProduccionyDemandaES['REGIMEN_ESPECIAL_A_MERCADO'][i]
                ins_study.CARBON = ins_raw.ProduccionyDemandaES['CARBON_IMPORTACION'][i]
                ins_study.CICLO_COMBINADO = ins_raw.ProduccionyDemandaES['CICLO_COMBINADO'][i]
                ins_study.HIDRAULICA_BOMBEO = ins_raw.ProduccionyDemandaES['CONSUMO_DE_BOMBEO'][i]
                ins_study.TERMICO_CON_PRIMA = ins_raw.ProduccionyDemandaES['TOTAL_TERMICA_(3+4+5+6+7+8)'][i]
                ins_study.IMPORTACION_FRANCIA = ins_raw.ProduccionyDemandaES['IMPORTACION_FRANCIA'][i]
                ins_study.IMPORTACION_PORTUGAL = ins_raw.ProduccionyDemandaES['IMPORTACION_PORTUGAL'][i]
                ins_study.IMPORTACION_MARRUECOS = ins_raw.ProduccionyDemandaES['IMPORTACION_MARRUECOS'][i]
                ins_study.IMPORTACION_ANDORRA = ins_raw.ProduccionyDemandaES['IMPORTACION_ANDORRA'][i]

                if iterDate not in listDT:
                    ins_study.ENERGIA_GESTIONADA = ins_raw.ProduccionyDemandaES['TOTAL_DEMANDA'][i]
                    ins_study.REGIMEN_ESPECIAL_A_DISTRIBUCION = ins_raw.ProduccionyDemandaES['REGIMEN_ESPECIAL_A_DISTRIBUCION'][i]
                    ins_study.FUEL_GAS = ins_raw.ProduccionyDemandaES['FUEL_+_GAS_REGIMEN_ORDINARIO_(SIN_PRIMA)'][i]
                    ins_study.UNIDADES_GENERICAS = ins_raw.ProduccionyDemandaES['UNIDADES_GENERICAS_SUBASTAS_DISTRIBUCION'][i]

                    ''' DEMANDA '''
                    ins_study.TOTAL_DEMANDA_NACIONAL_CLIENTES = ins_raw.ProduccionyDemandaES['TOTAL_DEMANDA_NACIONAL_CLIENTES_(21+22+23)'][i]
                    ins_study.TOTAL_CONSUMO_BOMBEO = ins_raw.ProduccionyDemandaES['TOTAL_CONSUMO_BOMBEO_(24)'][i]
                    ins_study.TOTAL_EXPORTACIONES = ins_raw.ProduccionyDemandaES['TOTAL_EXPORTACIONES_(25+26+27+28+29)'][i]
                    ins_study.TOTAL_GENERICAS = ins_raw.ProduccionyDemandaES['TOTAL_GENERICAS_(30+31)'][i]

                if iterDate in listCHV:
                    chVERANO(ins_raw, ins_study)
                elif iterDate in listCHI:
                    chINVIERNO(ins_raw, ins_study)
                elif iterDate in listDT:
                    dic = datosEnFalta(iterDate)

                    # if i == 0:
                    #     print dic
                    if dic['PreciosES']:
                        ins_study.Precios = dic['PreciosES'][i]
                    else:
                        ins_study.Precios = ins_raw.PreciosES[i]
                    if dic['PrevisionEolicaES']:
                        ins_study.PrevisionEolica = dic['PrevisionEolicaES'][i]
                    else:
                        ins_study.PrevisionEolica = ins_raw.PrevisionEolicaES[i]
                    if dic['PrevisionDemandaES']:
                        ins_study.PrevisionDemanda = dic['PrevisionDemandaES'][i]
                    else:
                        ins_study.PrevisionDemanda = ins_raw.PrevisionDemandaES[i]

#                         if dic['ProduccionyDemandaES']:
#                             ins_study.NUCLEAR = ins_raw.dic['ProduccionyDemandaES']['NUCLEAR'][i]
#                             ins_study.HIDRAULICA_CONVENCIONAL = ins_raw.dic['ProduccionyDemandaES']['HIDRAULICA_CONVENCIONAL'][i]
#                             ins_study.CARBON = ins_raw.dic['ProduccionyDemandaES']['CARBON_IMPORTACION'][i]
#                             ins_study.CICLO_COMBINADO = ins_raw.dic['ProduccionyDemandaES']['CICLO_COMBINADO'][i]
#                             ins_study.HIDRAULICA_BOMBEO = ins_raw.dic['ProduccionyDemandaES']['CONSUMO_DE_BOMBEO'][i]
#                             ins_study.TERMICO_CON_PRIMA = ins_raw.dic['ProduccionyDemandaES']['TOTAL_TERMICA_(3+4+5+6+7+8)'][i]
#                             ins_study.IMPORTACION_FRANCIA = ins_raw.dic['ProduccionyDemandaES']['IMPORTACION_FRANCIA'][i]
#                             ins_study.IMPORTACION_PORTUGAL = ins_raw.dic['ProduccionyDemandaES']['IMPORTACION_PORTUGAL'][i]
#                             ins_study.IMPORTACION_MARRUECOS = ins_raw.dic['ProduccionyDemandaES']['IMPORTACION_MARRUECOS'][i]
#                             ins_study.IMPORTACION_ANDORRA = ins_raw.dic['ProduccionyDemandaES']['IMPORTACION_ANDORRA'][i]
#
#                             if iterDate not in listDT:
#                                 ins_study.ENERGIA_GESTIONADA = ins_raw.dic['ProduccionyDemandaES']['TOTAL_DEMANDA'][i]
#                                 ins_study.REGIMEN_ESPECIAL = ins_raw.dic['ProduccionyDemandaES']['REGIMEN_ESPECIAL_A_DISTRIBUCION'][i]
#                                 ins_study.FUEL_GAS = ins_raw.dic['ProduccionyDemandaES']['FUEL_+_GAS_REGIMEN_ORDINARIO_(SIN_PRIMA)'][i]
#                                 ins_study.UNIDADES_GENERICAS = ins_raw.dic['ProduccionyDemandaES']['UNIDADES_GENERICAS_SUBASTAS_DISTRIBUCION'][i]
# 
#                                 ins_study.TOTAL_DEMANDA_NACIONAL_CLIENTES = ins_raw.dic['ProduccionyDemandaES']['TOTAL_DEMANDA_NACIONAL_CLIENTES_(21+22+23)'][i]
#                                 ins_study.TOTAL_CONSUMO_BOMBEO = ins_raw.dic['ProduccionyDemandaES']['TOTAL_CONSUMO_BOMBEO_(24)'][i]
#                                 ins_study.TOTAL_EXPORTACIONES = ins_raw.dic['ProduccionyDemandaES']['TOTAL_EXPORTACIONES_(25+26+27+28+29)'][i]
#                                 ins_study.TOTAL_GENERICAS = ins_raw.dic['ProduccionyDemandaES']['TOTAL_GENERICAS_(30+31)'][i]
#                         else:
#                             pass

                else:
                    ins_study.Precios = ins_raw.PreciosES[i]
                    ins_study.PrevisionEolica = ins_raw.PrevisionEolicaES[i]
                    ins_study.PrevisionDemanda = ins_raw.PrevisionDemandaES[i]

                ins_study.insertorupdatedataintodb()

            if currentDate == iterDate + timedelta(3):
                raise Exception('En la web del OMIE no hay datos de hoy, ayer y antes de ayer')

            iterDate += ONEDAY

def chVERANO(ins_raw, ins_study):
    ''' VERANO '''
    # Al cambiar de hora a verano pasamos de la hora 2:00 a la 3:00 (haremos ambos datos iguales)
    horaCHV = 3
    preci = ins_raw.PreciosES
    if len(preci) == 23:
        preci.insert(horaCHV,preci[horaCHV-1])
        for i in range(len(preci)):
            ins_study.Precios = preci[i]
        del preci
    eoli = ins_raw.PrevisionEolicaES
    if len(eoli) == 23:
        eoli.insert(horaCHV,eoli[horaCHV-1])
        for i in range(len(eoli)):
            ins_study.PrevisionEolica = eoli[i]
        del eoli
    deman = ins_raw.PrevisionDemandaES
    if len(deman) == 23:
        deman.insert(horaCHV,deman[horaCHV-1])
        for i in range(len(deman)):
            ins_study.PrevisionDemanda = deman[i]
        del deman

def chINVIERNO(ins_raw, ins_study):
        ''' INVIERNO '''
        # Al cambiar de hora a invierno pasamos de la hora 3:00 a la 2:00 (eliminamos el dato 3:00)
        horaCHI = 3
        preci = ins_raw.PreciosES
        if len(preci) == 25:
            preci.pop(horaCHI)
            for i in range(len(preci)):
                ins_study.Precios = preci[i]
            del preci
        eoli = ins_raw.PrevisionEolicaES
        if len(eoli) == 25:
            eoli.pop(horaCHI)
            for i in range(len(eoli)):
                ins_study.PrevisionEolica = eoli[i]
            del eoli
        deman = ins_raw.PrevisionDemandaES
        if len(deman) == 25:
            deman.pop(horaCHI)
            for i in range(len(deman)):
                ins_study.PrevisionDemanda = deman[i]
            del deman

# from sys import path
# path.append('libs')
# from omelinfosys.dbstudydatamanager import findLastStudyDocument
# findLastStudyDocument()
def findLastStudyDocument():
    '''
    Extraemos de la base de datos el ultimo documento (en funcion de la fecha interna del propio documento)
    '''
    ins_study = DBStudyData()
    collection = ins_study.getCollection()

#     currentDT = datetime.now()
#     cursor = collection.find({"fecha": {"$lte": currentDT}})
#     for element in cursor:
#         lastelement = element

    # cursor = collection.find().sort("fecha",-1).limit(1)
    cursor = collection.find().sort([("fecha",-1),("hora",-1)]).limit(1)
    for element in cursor:
        # print element
        # print element['hora']
        fecha = element['fecha']
        # fecha.replace(hour=0, minute=0, second=0, microsecond=0)
    del ins_study

#     return lastelement['fecha']
    return fecha

####################################################################################################

def gettecnologiasesfromweb(fecha):
        '''
        This is the main method so the usage of PreciosMibelHandler is more strainfoward.
        '''
        try:
            # validafecha(fecha)
            # The marginalpdbc data have the Spanish and the Portuguese prices.
            toparsePRODUCCION = urlopen(omieproduccionurl(fecha))
        except:
            raise
        else:
            Produccion = ProduccionMibelHandler(toparsePRODUCCION)
            # return {"ProduccionyDemandaMIBEL":Produccion.ProduccionyDemandaMIBEL,"ProduccionyDemandaES":Produccion.ProduccionyDemandaES,"ProduccionyDemandaPT":Produccion.ProduccionyDemandaPT}
            return {"ProduccionyDemandaES":Produccion.ProduccionyDemandaES}
        #finally:
        #    del toparsePRECIOS,Precios

####################################################################################################

# # from sys import path
# # path.append('libs')
# # from omelinfosys.dbstudydatamanager import populateStudyDataLocal
# # populateStudyDataLocal()
# def populateStudyDataLocal(startDate=None, endDate=None):
#     '''
#     TECNOLOGIAS actualiza la base de datos de TECNOLOGIAS del servidor
# 
#     Metodos de usabilidad con las clases definidas
#     This Method will performe the following operations:data = response.read()
#     1st:    Gathering informacion of StudyDataES collection. Last data inserted.
#     2nd:    Gathering informacion of RawData collection. Last data available.
#     3rd:    Study data won't take into account the change of hour days with the following logic:
#             23 hours day: hour 3 will be replicated.
#             25 hours day: hour 3 will be removed.
#     Sustituimos el nombre TOTAL_DEMANDA por el de ENERGIA_GESTIONADA segun se define en la web de
#     http://www.esios.ree.es/web-publica/
#     '''
#     try:
#         # ONEHOUR = timedelta(seconds=3600)
#         ONEDAY = timedelta(1)
#         if startDate == None:
#             startDate = findLastStudyDocumentLocal()
#         # Disponemos de los datos de la web de la "REE" con 3 dias de retraso
#         currentDate = datetime(datetime.now().year,datetime.now().month,datetime.now().day)
#         if endDate == None:
#             if startDate == currentDate:
#                 endDate = currentDate
#             elif startDate == currentDate - timedelta(1):
#                 endDate = startDate - timedelta(1)
#             elif startDate == currentDate - timedelta(2):
#                 endDate = startDate - timedelta(2)
#             else:
#                 endDate = currentDate - timedelta(3)
#     except:
#         raise
#     else:
#         listCHV = list()
#         listCHI = list()
#         for indi in range(endDate.year - startDate.year + 1):
#             fechaCHV, fechaCHI = centralEuropeanTime(startDate.year + indi)
#             listCHV.append(fechaCHV)
#             listCHI.append(fechaCHI)
# 
#         emptyPD, zeroPD = diasEnFalta()
#         listDT = emptyPD + zeroPD
#         iterDate = startDate
#         while (endDate >= iterDate):
#             print iterDate.date()
#             ins_raw = DBRawData()
#             # ins_raw.connection = Connection(host=None)
#             ins_raw.connectiondetails['host'] = None
#             ins_raw.set_fecha(iterDate)
#             ins_raw.getDataFromWeb()
# 
#             ''' si no hay datos en la base de datos falla '''
#             for i in range(24):
#                 ins_study = DBStudyData()
# 
#                 ins_study.fecha = iterDate
#                 ins_study.hora = i
# 
#                 ''' PRODUCCION '''
#                 ins_study.NUCLEAR = ins_raw.ProduccionyDemandaES['NUCLEAR'][i]
#                 ins_study.HIDRAULICA_CONVENCIONAL = ins_raw.ProduccionyDemandaES['HIDRAULICA_CONVENCIONAL'][i]
#                 ins_study.REGIMEN_ESPECIAL = ins_raw.ProduccionyDemandaES['REGIMEN_ESPECIAL_A_MERCADO'][i]
#                 ins_study.CARBON = ins_raw.ProduccionyDemandaES['CARBON_IMPORTACION'][i]
#                 ins_study.CICLO_COMBINADO = ins_raw.ProduccionyDemandaES['CICLO_COMBINADO'][i]
#                 ins_study.HIDRAULICA_BOMBEO = ins_raw.ProduccionyDemandaES['CONSUMO_DE_BOMBEO'][i]
#                 ins_study.TERMICO_CON_PRIMA = ins_raw.ProduccionyDemandaES['TOTAL_TERMICA_(3+4+5+6+7+8)'][i]
#                 ins_study.IMPORTACION_FRANCIA = ins_raw.ProduccionyDemandaES['IMPORTACION_FRANCIA'][i]
#                 ins_study.IMPORTACION_PORTUGAL = ins_raw.ProduccionyDemandaES['IMPORTACION_PORTUGAL'][i]
#                 ins_study.IMPORTACION_MARRUECOS = ins_raw.ProduccionyDemandaES['IMPORTACION_MARRUECOS'][i]
#                 ins_study.IMPORTACION_ANDORRA = ins_raw.ProduccionyDemandaES['IMPORTACION_ANDORRA'][i]
# 
#                 if iterDate not in listDT:
#                     ins_study.ENERGIA_GESTIONADA = ins_raw.ProduccionyDemandaES['TOTAL_DEMANDA'][i]
#                     ins_study.REGIMEN_ESPECIAL_A_DISTRIBUCION = ins_raw.ProduccionyDemandaES['REGIMEN_ESPECIAL_A_DISTRIBUCION'][i]
#                     ins_study.FUEL_GAS = ins_raw.ProduccionyDemandaES['FUEL_+_GAS_REGIMEN_ORDINARIO_(SIN_PRIMA)'][i]
#                     ins_study.UNIDADES_GENERICAS = ins_raw.ProduccionyDemandaES['UNIDADES_GENERICAS_SUBASTAS_DISTRIBUCION'][i]
# 
#                     ''' DEMANDA '''
#                     ins_study.TOTAL_DEMANDA_NACIONAL_CLIENTES = ins_raw.ProduccionyDemandaES['TOTAL_DEMANDA_NACIONAL_CLIENTES_(21+22+23)'][i]
#                     ins_study.TOTAL_CONSUMO_BOMBEO = ins_raw.ProduccionyDemandaES['TOTAL_CONSUMO_BOMBEO_(24)'][i]
#                     ins_study.TOTAL_EXPORTACIONES = ins_raw.ProduccionyDemandaES['TOTAL_EXPORTACIONES_(25+26+27+28+29)'][i]
#                     ins_study.TOTAL_GENERICAS = ins_raw.ProduccionyDemandaES['TOTAL_GENERICAS_(30+31)'][i]
# 
#                 if iterDate in listCHV:
#                     chVERANO(ins_raw, ins_study)
#                 elif iterDate in listCHI:
#                     chINVIERNO(ins_raw, ins_study)
#                 elif iterDate in listDT:
#                     dic = datosEnFalta(iterDate)
# 
#                     # if i == 0:
#                     #     print dic
#                     if dic['PreciosES']:
#                         ins_study.Precios = dic['PreciosES'][i]
#                     else:
#                         ins_study.Precios = ins_raw.PreciosES[i]
#                     if dic['PrevisionEolicaES']:
#                         ins_study.PrevisionEolica = dic['PrevisionEolicaES'][i]
#                     else:
#                         ins_study.PrevisionEolica = ins_raw.PrevisionEolicaES[i]
#                     if dic['PrevisionDemandaES']:
#                         ins_study.PrevisionDemanda = dic['PrevisionDemandaES'][i]
#                     else:
#                         ins_study.PrevisionDemanda = ins_raw.PrevisionDemandaES[i]
# 
# #                         if dic['ProduccionyDemandaES']:
# #                             ins_study.NUCLEAR = ins_raw.dic['ProduccionyDemandaES']['NUCLEAR'][i]
# #                             ins_study.HIDRAULICA_CONVENCIONAL = ins_raw.dic['ProduccionyDemandaES']['HIDRAULICA_CONVENCIONAL'][i]
# #                             ins_study.CARBON = ins_raw.dic['ProduccionyDemandaES']['CARBON_IMPORTACION'][i]
# #                             ins_study.CICLO_COMBINADO = ins_raw.dic['ProduccionyDemandaES']['CICLO_COMBINADO'][i]
# #                             ins_study.HIDRAULICA_BOMBEO = ins_raw.dic['ProduccionyDemandaES']['CONSUMO_DE_BOMBEO'][i]
# #                             ins_study.TERMICO_CON_PRIMA = ins_raw.dic['ProduccionyDemandaES']['TOTAL_TERMICA_(3+4+5+6+7+8)'][i]
# #                             ins_study.IMPORTACION_FRANCIA = ins_raw.dic['ProduccionyDemandaES']['IMPORTACION_FRANCIA'][i]
# #                             ins_study.IMPORTACION_PORTUGAL = ins_raw.dic['ProduccionyDemandaES']['IMPORTACION_PORTUGAL'][i]
# #                             ins_study.IMPORTACION_MARRUECOS = ins_raw.dic['ProduccionyDemandaES']['IMPORTACION_MARRUECOS'][i]
# #                             ins_study.IMPORTACION_ANDORRA = ins_raw.dic['ProduccionyDemandaES']['IMPORTACION_ANDORRA'][i]
# #
# #                             if iterDate not in listDT:
# #                                 ins_study.ENERGIA_GESTIONADA = ins_raw.dic['ProduccionyDemandaES']['TOTAL_DEMANDA'][i]
# #                                 ins_study.REGIMEN_ESPECIAL = ins_raw.dic['ProduccionyDemandaES']['REGIMEN_ESPECIAL_A_DISTRIBUCION'][i]
# #                                 ins_study.FUEL_GAS = ins_raw.dic['ProduccionyDemandaES']['FUEL_+_GAS_REGIMEN_ORDINARIO_(SIN_PRIMA)'][i]
# #                                 ins_study.UNIDADES_GENERICAS = ins_raw.dic['ProduccionyDemandaES']['UNIDADES_GENERICAS_SUBASTAS_DISTRIBUCION'][i]
# # 
# #                                 ins_study.TOTAL_DEMANDA_NACIONAL_CLIENTES = ins_raw.dic['ProduccionyDemandaES']['TOTAL_DEMANDA_NACIONAL_CLIENTES_(21+22+23)'][i]
# #                                 ins_study.TOTAL_CONSUMO_BOMBEO = ins_raw.dic['ProduccionyDemandaES']['TOTAL_CONSUMO_BOMBEO_(24)'][i]
# #                                 ins_study.TOTAL_EXPORTACIONES = ins_raw.dic['ProduccionyDemandaES']['TOTAL_EXPORTACIONES_(25+26+27+28+29)'][i]
# #                                 ins_study.TOTAL_GENERICAS = ins_raw.dic['ProduccionyDemandaES']['TOTAL_GENERICAS_(30+31)'][i]
# #                         else:
# #                             pass
# 
#                 else:
#                     ins_study.Precios = ins_raw.PreciosES[i]
#                     ins_study.PrevisionEolica = ins_raw.PrevisionEolicaES[i]
#                     ins_study.PrevisionDemanda = ins_raw.PrevisionDemandaES[i]
# 
#                 ins_study.connectiondetails['host'] = None
#                 ins_study.insertorupdatedataintodb()
# 
#             if currentDate == iterDate + timedelta(3):
#                 raise Exception('En la web del OMIE no hay datos de hoy, ayer y antes de ayer')
# 
#             iterDate += ONEDAY

# # from sys import path
# # path.append('libs')
# # from omelinfosys.dbstudydatamanager import findLastStudyDocumentLocal
# # findLastStudyDocumentLocal()
# def findLastStudyDocumentLocal():
#     '''
#     Extraemos de la base de datos el ultimo documento (en funcion de la fecha interna del propio documento)
#     '''
#     ins_study = DBStudyData()
# 
#     ''' BASE DE DATOS LOCAL '''
#     ins_study.connectiondetails['host'] = None
#     ins_study.setCollection()
# 
#     collection = ins_study.getCollection()
# 
#     currentDT = datetime.now()
#     cursor = collection.find({"fecha": {"$lte": currentDT}})
#     for element in cursor:
#         lastelement = element
#     return lastelement['fecha']

class DBStudyData():
    '''
    Esta clase es solo para gestionar la informacion a la hora de meter datos en la base de datos.
    Las consultas que nos interesa hacer las podemos filtrar con queries directas a la base de datos de registros.
    Asi es más facil consultar la importacion haciendo filtros de los datos y ordenar los datos a nuestro antojo.
    Creo que tambien sera más rapido.

    "fecha":,
    "hora":,
    "Precios":,
    "PrevisionDemanda":,
    "PrevisionEolica":,
    "ENERGIA_GESTIONADA":,

    -> Produccion
    "NUCLEAR":,
    "REGIMEN_ESPECIAL":,
    "HIDRAULICA_CONVENCIONAL":,
    "HIDRAULICA_BOMBEO":,
    "CARBON":,
    "CICLO_COMBINADO":,
    "FUEL_GAS":,
    "TERMICO_CON_PRIMA":,
    "UNIDADES_GENERICAS":,
    "IMPORTACION_PORTUGAL":,
    "IMPORTACION_FRANCIA":,
    "IMPORTACION_ANDORRA":,
    "IMPORTACION_MARRUECOS":,

    "REGIMEN_ESPECIAL_A_DISTRIBUCION:"

    -> Demanda
    La demanda tambien es importante ya que una demanda fuera del comun puede hacer subir los precios un monton
    Las centrales de bombeo pueden demandar energia y ademas con precio alto y asi inflacionar los precios de mercado
    Esto es una supocion
    '''

# from sys import path
# path.append('libs')
# from omelinfosys.dbstudydatamanager import DBStudyData
# hostOpenShift = 'mongodb://hmarrao:hmarrao@ds031117.mongolab.com:31117/mercadodiario'
# DBStudyData.connectiondetails['host'] = hostOpenShift
# from datetime import datetime
# startDate = datetime(2014,10,1)
# from omelinfosys.dbstudydatamanager import populateStudyData
# populateStudyData(startDate)

    connectiondetails = dict(host=None)
#     connectiondetails = dict()

    def __init__(self):
        '''
        if no hour is given get it from the fecha
        in data base hour in fecha datetime is set to zero in order to be able to perform queries of a full day
        '''
        try:
            ''' LOCAL '''
#             self.connectiondetails['host'] = None
            ''' SERVIDOR '''
#             self.connectiondetails['host'] = 'mongodb://hmarrao:hmarrao@ds031117.mongolab.com:31117/mercadodiario'

            self.connectiondetails['host'] = self.connectiondetails['host']
            self.connectiondetails['db_name'] = 'mercadodiario'
            self.connectiondetails['coll_name'] = 'tecnologiases'
            self.setCollection()

        except:
            raise
        else:
            # instance attributes definitions
            self.Precios = 0
            self.PrevisionDemanda = 0
            self.PrevisionEolica = 0
            self.ENERGIA_GESTIONADA = 0
            self.NUCLEAR = 0
            self.REGIMEN_ESPECIAL = 0
            self.HIDRAULICA_CONVENCIONAL = 0
            self.HIDRAULICA_BOMBEO = 0
            self.CARBON = 0
            self.CICLO_COMBINADO = 0
            self.FUEL_GAS = 0
            self.TERMICO_CON_PRIMA = 0
            self.UNIDADES_GENERICAS = 0
            self.IMPORTACION_PORTUGAL = 0
            self.IMPORTACION_FRANCIA = 0
            self.IMPORTACION_ANDORRA = 0
            self.IMPORTACION_MARRUECOS = 0

            self.TOTAL_DEMANDA_NACIONAL_CLIENTES = 0
            self.TOTAL_CONSUMO_BOMBEO = 0
            self.TOTAL_EXPORTACIONES = 0
            self.TOTAL_GENERICAS = 0

            self.REGIMEN_ESPECIAL_A_DISTRIBUCION = 0

    def getCollection(self):
        '''
        Get mongo collection cursor
        '''
        return self._collection

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

    # from sys import path
    # path.append('libs')
    # from datetime import datetime
    # fecha = datetime(2012,1,1)
    # from omelinfosys.DBStudyData import DBStudyData
    # ins = DBStudyData()
    # ins.getStudyDataFromDB(fecha)
    # hora = 6
    # ins.getStudyDataFromDB(fecha,hora)
    def getStudyDataFromDB(self,fecha,hora=None):
        '''
        '''
        try:
            # collection = db[self.collectionName]
            # results = collection.find({"fecha": {"$in" : [self.fecha]}})
            if hora is None:
                results = self.collection.find({ "fecha": {"$in" : [fecha]} })
            else:
                results = self.collection.find({ "fecha": {"$in" : [fecha]}, "hora": {"$in": [hora]} })
            # if results.count() == 0:
            #     raise Exception('No hay datos en la base de datos.')
            # if results.count() > 1:
            #     raise Exception('La base de datos tiene mas de un registro para la dada fecha.')
            for result in results:
                # print result
                self.fecha = result["fecha"]
                self.hora = result["hora"]

                ''' PRODUCCION '''
                self.Precios = result["Precios"]
                self.PrevisionDemanda = result["PrevisionDemanda"]
                self.PrevisionEolica = result["PrevisionEolica"]
                self.ENERGIA_GESTIONADA = result["ENERGIA_GESTIONADA"]
                self.NUCLEAR = result["NUCLEAR"]
                self.REGIMEN_ESPECIAL = result["REGIMEN_ESPECIAL"]
                self.HIDRAULICA_CONVENCIONAL = result["HIDRAULICA_CONVENCIONAL"]
                self.HIDRAULICA_BOMBEO = result["HIDRAULICA_BOMBEO"]
                self.CARBON = result["CARBON"]
                self.CICLO_COMBINADO = result["CICLO_COMBINADO"]
                self.FUEL_GAS = result["FUEL_GAS"]
                self.TERMICO_CON_PRIMA = result["TERMICO_CON_PRIMA"]
                self.UNIDADES_GENERICAS = result["UNIDADES_GENERICAS"]
                self.IMPORTACION_PORTUGAL = result["IMPORTACION_PORTUGAL"]
                self.IMPORTACION_FRANCIA = result["IMPORTACION_FRANCIA"]
                self.IMPORTACION_ANDORRA = result["IMPORTACION_ANDORRA"]
                self.IMPORTACION_MARRUECOS = result["IMPORTACION_MARRUECOS"]

                ''' DEMANDA '''
                self.TOTAL_DEMANDA_NACIONAL_CLIENTES = result['TOTAL_DEMANDA_NACIONAL_CLIENTES']
                self.TOTAL_CONSUMO_BOMBEO = result['TOTAL_CONSUMO_BOMBEO']
                self.TOTAL_EXPORTACIONES = result['TOTAL_EXPORTACIONES']
                self.TOTAL_GENERICAS = result['TOTAL_GENERICAS']

                self.REGIMEN_ESPECIAL_A_DISTRIBUCION = result["REGIMEN_ESPECIAL_A_DISTRIBUCION"]

        except:
            raise
        else:
            self.connection.close()

    def insertorupdatedataintodb(self):
        '''
        '''
        try:

            self.setCollection()
            collection = self.getCollection()

            # collection = db[self.collectionName]
            results = collection.find({"fecha" : {"$in": [self.fecha]}, "hora": {"$in": [self.hora]}})
            jsontoinsert = dict()
            jsontoinsert["fecha"] = self.fecha
            jsontoinsert["hora"] = self.hora

            ''' PRODUCCION '''
            jsontoinsert["Precios"] = self.Precios
            jsontoinsert["PrevisionDemanda"] = self.PrevisionDemanda
            jsontoinsert["PrevisionEolica"] = self.PrevisionEolica
            jsontoinsert["ENERGIA_GESTIONADA"] = self.ENERGIA_GESTIONADA
            jsontoinsert["NUCLEAR"] = self.NUCLEAR
            jsontoinsert["REGIMEN_ESPECIAL"] = self.REGIMEN_ESPECIAL
            jsontoinsert["HIDRAULICA_CONVENCIONAL"] = self.HIDRAULICA_CONVENCIONAL
            jsontoinsert["HIDRAULICA_BOMBEO"] = self.HIDRAULICA_BOMBEO
            jsontoinsert["CARBON"] = self.CARBON
            jsontoinsert["CICLO_COMBINADO"] = self.CICLO_COMBINADO
            jsontoinsert["FUEL_GAS"] = self.FUEL_GAS
            jsontoinsert["TERMICO_CON_PRIMA"] = self.TERMICO_CON_PRIMA
            jsontoinsert["UNIDADES_GENERICAS"] = self.UNIDADES_GENERICAS
            jsontoinsert["IMPORTACION_PORTUGAL"] = self.IMPORTACION_PORTUGAL
            jsontoinsert["IMPORTACION_FRANCIA"] = self.IMPORTACION_FRANCIA
            jsontoinsert["IMPORTACION_ANDORRA"] = self.IMPORTACION_ANDORRA
            jsontoinsert["IMPORTACION_MARRUECOS"] = self.IMPORTACION_MARRUECOS

            ''' DEMANDA '''
            jsontoinsert["TOTAL_DEMANDA_NACIONAL_CLIENTES"] = self.TOTAL_DEMANDA_NACIONAL_CLIENTES
            jsontoinsert["TOTAL_CONSUMO_BOMBEO"] = self.TOTAL_CONSUMO_BOMBEO
            jsontoinsert["TOTAL_EXPORTACIONES"] = self.TOTAL_EXPORTACIONES
            jsontoinsert["TOTAL_GENERICAS"] = self.TOTAL_GENERICAS

            jsontoinsert["REGIMEN_ESPECIAL_A_DISTRIBUCION"] = self.REGIMEN_ESPECIAL_A_DISTRIBUCION

            if results.count() == 0:
                # construct the json to insert
                collection.insert(jsontoinsert)
            if results.count() == 1:
                collection.update({"fecha" : {"$in" : [self.fecha]},
                                        "hora" : {"$in" : [self.hora]}},
                                       {"$set" : jsontoinsert })
            if results.count() > 1:
                raise Exception('La base de datos tiene mas de un registro para la dada fecha')
        except:
            raise
        else:
            self.setCollection(), jsontoinsert

class DBManagerStudyDataES(DBStudyData):
    '''
    '''
    def __init__(self,fecha,hour = None):
        #DBStudyData.__init__(self)
        super(DBManagerStudyDataES,self).__init__(fecha,hour,'StudyDataES')

class DBManagerStudyDataPT(DBStudyData):
    '''
    '''
    def __init__(self,fecha,hour = None):
        #DBStudyData.__init__(self)
        super(DBManagerStudyDataPT,self).__init__(fecha,hour,'StudyDataPT')

class DBManagerStudyDataMIBEL(DBStudyData):
    '''
    '''
    def __init__(self,fecha,hour = None):
        #DBStudyData.__init__(self)
        super(DBManagerStudyDataMIBEL,self).__init__(fecha,hour,'StudyDataMIBEL')

# def populateStudyDataBis(startDate, endDate=None):
#     '''
#     Study data won't take into account the change of hour days with the following logic:
#     23 hours day: hour 3 will be replicated.
#     25 hours day: hour 3 will be removed.
#     Sustituimos el nombre ENERGIA_GESTIONADA por TOTAL_DEMANDA segun se define en la web de
#     Sustituimos el nombre TOTAL_DEMANDA por el de ENERGIA_GESTIONADA segun se define en la web de
#     http://www.esios.ree.es/web-publica/
#     '''
#     ONEDAY = timedelta(1)
#     # listDT = diasEnFalta()
#     iterDate = startDate
#     while (endDate >= iterDate):
#         print iterDate.date()
#         ins_raw = DBRawData(iterDate)
#         ins_raw.getRawDataFromDB()
#         for i in range(24):
#             ins_study = DBStudyData()
# 
#             ins_study.hora = i
#             ins_study.fecha = iterDate
#             # ins_study.fecha = datetime(iterDate.year,iterDate.month,iterDate.day,i)
# 
#             ''' PRODUCCION '''
#             ins_study.Precios = ins_raw.PreciosES[i]
#             ins_study.PrevisionDemanda = ins_raw.PrevisionDemandaES[i]
#             ins_study.PrevisionEolica = ins_raw.PrevisionEolicaES[i]
#             ins_study.FUEL_GAS = ins_raw.ProduccionyDemandaES['FUEL_+_GAS_REGIMEN_ORDINARIO_(SIN_PRIMA)'][i]
#             ins_study.UNIDADES_GENERICAS = ins_raw.ProduccionyDemandaES['UNIDADES_GENERICAS_SUBASTAS_DISTRIBUCION'][i]
# 
#             ''' DEMANDA '''
#             ins_study.TOTAL_DEMANDA_NACIONAL_CLIENTES = ins_raw.ProduccionyDemandaES['TOTAL_DEMANDA_NACIONAL_CLIENTES_(21+22+23)'][i]
#             ins_study.TOTAL_CONSUMO_BOMBEO = ins_raw.ProduccionyDemandaES['TOTAL_CONSUMO_BOMBEO_(24)'][i]
#             ins_study.TOTAL_EXPORTACIONES = ins_raw.ProduccionyDemandaES['TOTAL_EXPORTACIONES_(25+26+27+28+29)'][i]
#             ins_study.TOTAL_GENERICAS = ins_raw.ProduccionyDemandaES['TOTAL_GENERICAS_(30+31)'][i]
# 
#             ins_study.insertorupdatedataintodb()
#         iterDate += ONEDAY

# def updateStudyDataBis(startDate, endDate=None):
#     '''
#     el campo "fecha" va variando el valor de CET o CSET, en vez de el valor real del campo "hora",
#     por lo que la "fecha" esta mal y al seleccionar dias de la base de datos obtenemos otros dias
#     '''
#     ONEDAY = timedelta(1)
#     listDT = diasEnFalta()
#     iterDate = startDate
#     while (endDate >= iterDate):
#         print iterDate
#         ins_raw = DBRawData(iterDate)
#         ins_raw.getRawDataFromDB()
#         for i in range(24):
#             ins_study = DBStudyData()
# 
#             ins_study.hora = i
#             ins_study.fecha = iterDate
#             # ins_study.fecha = datetime(iterDate.year,iterDate.month,iterDate.day,i)
# 
#             ''' PRODUCCION '''
#             ins_study.Precios = ins_raw.PreciosES[i]
#             ins_study.PrevisionDemanda = ins_raw.PrevisionDemandaES[i]
#             ins_study.PrevisionEolica = ins_raw.PrevisionEolicaES[i]
#             ins_study.ENERGIA_GESTIONADA = ins_raw.ProduccionyDemandaES['TOTAL_DEMANDA'][i]
#             ins_study.NUCLEAR = ins_raw.ProduccionyDemandaES['NUCLEAR'][i]
#             ins_study.REGIMEN_ESPECIAL = ins_raw.ProduccionyDemandaES['REGIMEN_ESPECIAL_A_DISTRIBUCION'][i]
#             ins_study.HIDRAULICA_CONVENCIONAL = ins_raw.ProduccionyDemandaES['HIDRAULICA_CONVENCIONAL'][i]
#             ins_study.HIDRAULICA_BOMBEO = ins_raw.ProduccionyDemandaES['CONSUMO_DE_BOMBEO'][i]
#             ins_study.CARBON = ins_raw.ProduccionyDemandaES['CARBON_IMPORTACION'][i]
#             ins_study.CICLO_COMBINADO = ins_raw.ProduccionyDemandaES['CICLO_COMBINADO'][i]
#             ins_study.FUEL_GAS = ins_raw.ProduccionyDemandaES['FUEL_+_GAS_REGIMEN_ORDINARIO_(SIN_PRIMA)'][i]
#             ins_study.HIDRAULICA_BOMBEO = ins_raw.ProduccionyDemandaES['CONSUMO_DE_BOMBEO'][i]
#             ins_study.TERMICO_CON_PRIMA = ins_raw.ProduccionyDemandaES['TOTAL_TERMICA_(3+4+5+6+7+8)'][i]
#             ins_study.UNIDADES_GENERICAS = ins_raw.ProduccionyDemandaES['UNIDADES_GENERICAS_SUBASTAS_DISTRIBUCION'][i]
#             ins_study.IMPORTACION_PORTUGAL = ins_raw.ProduccionyDemandaES['IMPORTACION_PORTUGAL'][i]
#             ins_study.IMPORTACION_FRANCIA = ins_raw.ProduccionyDemandaES['IMPORTACION_FRANCIA'][i]
#             ins_study.IMPORTACION_ANDORRA = ins_raw.ProduccionyDemandaES['IMPORTACION_ANDORRA'][i]
#             ins_study.IMPORTACION_PORTUGAL = ins_raw.ProduccionyDemandaES['IMPORTACION_PORTUGAL'][i]
#             ins_study.IMPORTACION_MARRUECOS = ins_raw.ProduccionyDemandaES['IMPORTACION_MARRUECOS'][i]
#             ins_study.IMPORTACION_ANDORRA = ins_raw.ProduccionyDemandaES['IMPORTACION_ANDORRA'][i]
# 
#             if iterDate not in listDT:
#                 ins_study.ENERGIA_GESTIONADA = ins_raw.ProduccionyDemandaES['TOTAL_DEMANDA'][i]
#                 ins_study.REGIMEN_ESPECIAL = ins_raw.ProduccionyDemandaES['REGIMEN_ESPECIAL_A_DISTRIBUCION'][i]
#                 ins_study.FUEL_GAS = ins_raw.ProduccionyDemandaES['FUEL_+_GAS_REGIMEN_ORDINARIO_(SIN_PRIMA)'][i]
#                 ins_study.UNIDADES_GENERICAS = ins_raw.ProduccionyDemandaES['UNIDADES_GENERICAS_SUBASTAS_DISTRIBUCION'][i]
# 
#                 ''' DEMANDA '''
#                 ins_study.TOTAL_DEMANDA_NACIONAL_CLIENTES = ins_raw.ProduccionyDemandaES['TOTAL_DEMANDA_NACIONAL_CLIENTES_(21+22+23)'][i]
#                 ins_study.TOTAL_CONSUMO_BOMBEO = ins_raw.ProduccionyDemandaES['TOTAL_CONSUMO_BOMBEO_(24)'][i]
#                 ins_study.TOTAL_EXPORTACIONES = ins_raw.ProduccionyDemandaES['TOTAL_EXPORTACIONES_(25+26+27+28+29)'][i]
#                 ins_study.TOTAL_GENERICAS = ins_raw.ProduccionyDemandaES['TOTAL_GENERICAS_(30+31)'][i]
# 
#             ins_study.insertorupdatedataintodb()
#         iterDate += ONEDAY

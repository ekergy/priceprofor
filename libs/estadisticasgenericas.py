# -*- coding: utf-8 -*-
'''
Created on 05/2014
@author: hmarrao & david
'''

from pymongo import MongoClient
from datetime import datetime, timedelta

connectiondetails = dict(host=None)

# ''' LOCAL '''
# CONN_HOST = None
# ''' SERVIDOR '''
# CONN_HOST = 'mongodb://hmarrao:hmarrao@ds031117.mongolab.com:31117/mercadodiario'

# from sys import path
# path.append('libs')
# path.append('wsgi')
# from estadisticasgenericas import estadisticasPrecios
# estadisticasPrecios()
def estadisticasPrecios():
    '''
    '''
#     db = MongoClient().mercadodiario

#     db.precioses.aggregate([{"$group": {"_id": "null", "avg": {"$avg": "$PreciosES"}}}])
#     db.precioses.aggregate([{"$group": {"_id": "null", "avg": {"$avg": "$PreciosES"}}}])["result"][0]["avg"]

#     my_date_str = "2014-04-04T00:00:00Z"
#     fecha = parser.parse(my_date_str)
#     # returns a datetime.datetime(2011, 1, 1, 16, 0, tzinfo=tzutc())
#     db.precioses.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha}}}, {"$group": {"_id": "null", "avg": {"$avg": "$PreciosES"}}}])
#     db.precioses.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha}}}, {"$group": {"_id": "null", "avg": {"$avg": "$PreciosES"}}}])["result"][0]["avg"]
#     # (9+6+5+4.9+2.98+2.99+7.04+12+12+16+10+8.8+8.8+10.35+7.04+7.5+7+7.04+7+9+21.9+25.01+20.5+15)/24

#     # tipo de dato "ISODate"
#     # my_date_str = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
#     my_date_str = datetime.now().strftime("%Y-%m-%dT00:00:00Z")
#     fecha2 = parser.parse(my_date_str)
#     fecha = fecha2
#     # db.precioses.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha}}}, {"$group": {"_id": "null", "avg": {"$avg": "$PreciosES"}}}])
#     db.precioses.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$PreciosES"}}}])["result"][0]["avg"]

    promediosPrecios = list()

    promediosDesde = list()
    promediosHasta = list()

    fecha_aux = datetime.now()

    ''' se deben probar en todos los años los dias finales de cada mes que dan problemas por ser o 30 o 31 '''
#     fecha_aux = datetime(2014,1,31)
#     fecha_aux = datetime(2013,2,28)
#     fecha_aux = datetime(2013,3,31)
#     fecha_aux = datetime(2013,4,30)
#     fecha_aux = datetime(2013,5,31)
#     fecha_aux = datetime(2013,6,30)
#     fecha_aux = datetime(2013,7,31)
#     fecha_aux = datetime(2013,8,31)
#     fecha_aux = datetime(2013,9,30)
#     fecha_aux = datetime(2013,10,31)
#     fecha_aux = datetime(2013,11,30)
#     fecha_aux = datetime(2013,12,31)

    db = MongoClient(host=connectiondetails['host']).mercadodiario

    ''' Precio Promedio dia actual '''
#     db = MongoClient(host=CONN_HOST).mercadodiario
#     my_date_str = datetime.now().strftime("%Y-%m-%dT00:00:00Z")
#     fecha2 = parser.parse(my_date_str)
    fecha2 = fecha_aux.replace(hour=0, minute=0, second=0, microsecond=0)
    fecha = fecha2
    query = db.precioses.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$PreciosES"}}}])["result"][0]["avg"]
    promediosPrecios.insert(0, round(query,2))
    promediosDesde.insert(0, fecha)
    promediosHasta.insert(0, fecha2)

#     print 'dia actual'
#     print fecha2 - fecha
#     print ''

    ''' Precio Promedio dia anterior '''
#     db = MongoClient(host=CONN_HOST).mercadodiario
#     my_date_str = datetime.now().strftime("%Y-%m-%dT00:00:00Z")
#     fecha3 = parser.parse(my_date_str)
    fecha3 = fecha_aux.replace(hour=0, minute=0, second=0, microsecond=0)
    fecha2 = fecha3 - timedelta(days=1)
    fecha = fecha3 - timedelta(days=1)
    query = db.precioses.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$PreciosES"}}}])["result"][0]["avg"]
    promediosPrecios.insert(1, round(query,2))
    promediosDesde.insert(1, fecha)
    promediosHasta.insert(1, fecha2)

#     print 'dia anterior'
#     print fecha3 - fecha
#     print ''

    ''' Precio Promedio ultimos dos dias '''
#     db = MongoClient().mercadodiario
#     my_date_str = datetime.now().strftime("%Y-%m-%dT00:00:00Z")
#     # hoy
#     fecha2 = parser.parse(my_date_str)
#     fecha = fecha2
#     db.precioses.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$PreciosES"}}}])["result"][0]["avg"]
# 
#     db = MongoClient().mercadodiario
#     my_date_str = datetime.now().strftime("%Y-%m-%dT00:00:00Z")
#     # ayer
#     fecha2 = parser.parse(my_date_str)
#     fecha2 = fecha2 - timedelta(1)
#     fecha = fecha2
#     db.precioses.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$PreciosES"}}}])["result"][0]["avg"]
# 
#     db = MongoClient().mercadodiario
#     my_date_str = datetime.now().strftime("%Y-%m-%dT00:00:00Z")
#     # ambos hoy y ayer
#     fecha2 = parser.parse(my_date_str)
#     fecha = fecha2 - timedelta(1)
#     db.precioses.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$PreciosES"}}}])["result"][0]["avg"]
#     # (62.019166666666656 + 61.30625) / 2

    ''' Precio Promedio semana actual '''
#     db = MongoClient(host=CONN_HOST).mercadodiario
#     my_date_str = datetime.now().strftime("%Y-%m-%dT00:00:00Z")
#     fecha2 = parser.parse(my_date_str)
    fecha2 = fecha_aux.replace(hour=0, minute=0, second=0, microsecond=0)
    fecha = fecha2 - timedelta(weeks=1) + timedelta(days=1)
    query = db.precioses.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$PreciosES"}}}])["result"][0]["avg"]
    promediosPrecios.insert(2, round(query,2))
    promediosDesde.insert(2, fecha)
    promediosHasta.insert(2, fecha2)

#     print 'semana actual'
#     print fecha2 - fecha
#     print ''

    ''' Precio Promedio semana anterior '''
#     db = MongoClient(host=CONN_HOST).mercadodiario
#     my_date_str = datetime.now().strftime("%Y-%m-%dT00:00:00Z")
#     fecha3 = parser.parse(my_date_str)
    fecha3 = fecha_aux.replace(hour=0, minute=0, second=0, microsecond=0)
    fecha2 = fecha3 - timedelta(weeks=1)
    fecha = fecha3 - timedelta(weeks=2) + timedelta(days=1)
    query = db.precioses.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$PreciosES"}}}])["result"][0]["avg"]
    promediosPrecios.insert(3, round(query,2))
    promediosDesde.insert(3, fecha)
    promediosHasta.insert(3, fecha2)

#     print 'semana anterior'
#     print fecha3 - fecha
#     print ''

    ''' Precio Promedio mes actual '''
    # db = MongoClient(host=CONN_HOST).mercadodiario
    # my_date_str = datetime.now().strftime("%Y-%m-%dT00:00:00Z")
    # fecha2 = parser.parse(my_date_str)
    fecha2 = fecha_aux.replace(hour=0, minute=0, second=0, microsecond=0)
    # fecha = fecha2.replace(month=fecha2.month - 1)
    # fecha = (fecha2 - timedelta(weeks=4) - timedelta(days=2)).replace(day=fecha2.day) + timedelta(days=1)

    try:
        fecha = (fecha2 - timedelta(weeks=4) - timedelta(days=3)).replace(day=fecha2.day) + timedelta(days=1)
    except ValueError:
        fecha = (fecha2 - timedelta(weeks=4) - timedelta(days=3))

    query = db.precioses.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$PreciosES"}}}])["result"][0]["avg"]
    promediosPrecios.insert(4, round(query,2))
    promediosDesde.insert(4, fecha)
    promediosHasta.insert(4, fecha2)

#     print 'mes actual'
#     print fecha2 - fecha
#     print ''

    ''' Precio Promedio mes anterior '''
#     db = MongoClient(host=CONN_HOST).mercadodiario
#     my_date_str = datetime.now().strftime("%Y-%m-%dT00:00:00Z")
#     fecha3 = parser.parse(my_date_str)
    fecha3 = fecha_aux.replace(hour=0, minute=0, second=0, microsecond=0)
#     fecha2 = fecha3.replace(month=fecha3.month - 1)
    # fecha2 = (fecha3 - timedelta(weeks=4) - timedelta(days=3)).replace(day=fecha3.day)

    try:
        fecha2 = (fecha3 - timedelta(weeks=4) - timedelta(days=3)).replace(day=fecha3.day) + timedelta(days=1)
    except ValueError:
        fecha2 = (fecha3 - timedelta(weeks=4) - timedelta(days=3))

#     fecha = fecha2.replace(month=fecha2.month - 1)
    # fecha = (fecha3 - timedelta(weeks=8) - timedelta(days=4)).replace(day=fecha3.day) + timedelta(days=1)
    # fecha = (fecha3 - timedelta(weeks=8) - timedelta(days=6)).replace(day=fecha3.day) + timedelta(days=1)

    try:
        fecha = (fecha3 - timedelta(weeks=8) - timedelta(days=6)).replace(day=fecha3.day) + timedelta(days=1)
    except ValueError:
        fecha = (fecha3 - timedelta(weeks=8) - timedelta(days=6))

    query = db.precioses.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$PreciosES"}}}])["result"][0]["avg"]
    promediosPrecios.insert(5, round(query,2))
    promediosDesde.insert(5, fecha)
    promediosHasta.insert(5, fecha2)

#     print 'mes anterior'
#     print fecha3 - fecha
#     print ''

    ''' Precio Promedio estacion actual '''
#     db = MongoClient(host=CONN_HOST).mercadodiario
#     my_date_str = datetime.now().strftime("%Y-%m-%dT00:00:00Z")
#     fecha2 = parser.parse(my_date_str)
    fecha2 = fecha_aux.replace(hour=0, minute=0, second=0, microsecond=0)
#     fecha = fecha2.replace(month=fecha2.month - 3)
    # fecha = (fecha2 - timedelta(weeks=13)).replace(day=fecha2.day) + timedelta(days=1)
    fecha = (fecha2 - timedelta(weeks=13)) - timedelta(days=1)

    query = db.precioses.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$PreciosES"}}}])["result"][0]["avg"]
    promediosPrecios.insert(6, round(query,2))
    promediosDesde.insert(6, fecha)
    promediosHasta.insert(6, fecha2)

#     print 'estacion actual'
#     print fecha2 - fecha
#     print ''

    ''' Precio Promedio estacion anterior '''
#     db = MongoClient(host=CONN_HOST).mercadodiario
#     my_date_str = datetime.now().strftime("%Y-%m-%dT00:00:00Z")
#     fecha3 = parser.parse(my_date_str)
    fecha3 = fecha_aux.replace(hour=0, minute=0, second=0, microsecond=0)
#     fecha2 = fecha3.replace(month=fecha3.month - 1)
    # fecha2 = (fecha3 - timedelta(weeks=13)).replace(day=fecha3.day)
    fecha2 = (fecha3 - timedelta(weeks=13)) - timedelta(days=1)
#     fecha = fecha2.replace(month=fecha2.month - 3)
    # fecha = (fecha3 - timedelta(weeks=26)).replace(day=fecha3.day) + timedelta(days=1)
    fecha = (fecha3 - timedelta(weeks=26)) - timedelta(days=2)

    query = db.precioses.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$PreciosES"}}}])["result"][0]["avg"]
    promediosPrecios.insert(7, round(query,2))
    promediosDesde.insert(7, fecha)
    promediosHasta.insert(7, fecha2)

#     print 'estacion anterior'
#     print fecha3 - fecha
#     print ''

    ''' Precio Promedio año actual '''
#     db = MongoClient(host=CONN_HOST).mercadodiario
#     my_date_str = datetime.now().strftime("%Y-%m-%dT00:00:00Z")
#     fecha2 = parser.parse(my_date_str)
    fecha2 = fecha_aux.replace(hour=0, minute=0, second=0, microsecond=0)
#     fecha = fecha2.replace(year=fecha2.year - 1)
    # fecha = (fecha2 - timedelta(weeks=52)).replace(day=fecha2.day) + timedelta(days=1)
    fecha = (fecha2 - timedelta(weeks=52)) - timedelta(days=1)

    query = db.precioses.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$PreciosES"}}}])["result"][0]["avg"]
    promediosPrecios.insert(8, round(query,2))
    promediosDesde.insert(8, fecha)
    promediosHasta.insert(8, fecha2)

#     print 'año actual'
#     print fecha2 - fecha
#     print ''

    ''' Precio Promedio año anterior '''
#     db = MongoClient(host=CONN_HOST).mercadodiario
#     my_date_str = datetime.now().strftime("%Y-%m-%dT00:00:00Z")
#     fecha3 = parser.parse(my_date_str)
    fecha3 = fecha_aux.replace(hour=0, minute=0, second=0, microsecond=0)
#     fecha2 = fecha3.replace(year=fecha3.year - 1)
    # fecha2 = (fecha3 - timedelta(weeks=52)).replace(day=fecha3.day)
    fecha2 = (fecha3 - timedelta(weeks=52)) - timedelta(days=1)
#     fecha = fecha2.replace(year=fecha2.year - 1)
    # fecha = (fecha3 - timedelta(weeks=104)).replace(day=fecha3.day) + timedelta(days=1)
    fecha = (fecha3 - timedelta(weeks=104)) - timedelta(days=2)

    query = db.precioses.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$PreciosES"}}}])["result"][0]["avg"]
    promediosPrecios.insert(9, round(query,2))
    promediosDesde.insert(9, fecha)
    promediosHasta.insert(9, fecha2)

#     print 'año anterior'
#     print fecha3 - fecha
#     print ''

    ''' Intervalo de variacion del precio del ultimo dia '''
#     db = MongoClient().mercadodiario
#     # my_date_str = datetime.now().strftime("%Y-%m-%dT00:00:00Z")
#     my_date_str = datetime(2014,10,8).strftime("%Y-%m-%dT00:00:00Z")
#     fecha2 = parser.parse(my_date_str)
#     fecha = fecha2
#     max = db.precioses.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$max": "$PreciosES"}}}])["result"][0]["avg"]
#     min = db.precioses.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$min": "$PreciosES"}}}])["result"][0]["avg"]
#     inter = max - min

    '''
    Este error ocurre cuando por ej la base de datos en local no esta actualizado y faltan los datos del ultimo dia

    File "wsgi/controllers/priceprofor_estadisticas.py", line 159, in estadisticasPrecios
    query = db.precioses.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$PreciosES"}}}])["result"][0]["avg"]
    IndexError: list index out of range
    '''

    ''' LOCAL '''
#     collection = Connection(host=None).mercadodiario.precioses
    ''' SERVIDOR '''
#     collection = Connection(host='mongodb://hmarrao:hmarrao@ds031117.mongolab.com:31117/mercadodiario').mercadodiario.precioses

#     currentDT = datetime(datetime.now().year, datetime.now().month, datetime.now().day)
#     cursor = collection.find({"fecha": {"$in": [currentDT]}})

#     for element in cursor:
#         lastelement = element

#     mylist = list()
#     for element in cursor:
#         mylist.append(element)
# #     return lastelement['fecha']
#     print mylist
#     return mylist

#     print promediosDesde
#     print ''

    return promediosPrecios, promediosDesde, promediosHasta

# from sys import path
# path.append('libs')
# path.append('wsgi')
# from estadisticasgenericas import estadisticasTecnologias
# estadisticasTecnologias()
def estadisticasTecnologias():
    '''
    '''
    promediosNuclear = list()
    promediosRegimenEspecial = list()
    promediosHidraulicaConvencional = list()
    promediosCarbon = list()
    promediosCicloCombinado = list()
    promediosFuelGas = list()

    promediosDesde = list()
    promediosHasta = list()

    fecha_aux = datetime.now()
    db = MongoClient(host=connectiondetails['host']).mercadodiario

    ''' Promedio dia actual '''
#     db = MongoClient(host=CONN_HOST).mercadodiario
#     my_date_str = datetime.now().strftime("%Y-%m-%dT00:00:00Z")
#     fecha2 = parser.parse(my_date_str) - timedelta(3)
    fecha2 = fecha_aux.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(3)
    fecha = fecha2
    indice = 0
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$NUCLEAR"}}}])["result"][0]["avg"]
    promediosNuclear.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$REGIMEN_ESPECIAL"}}}])["result"][0]["avg"]
    promediosRegimenEspecial.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$HIDRAULICA_CONVENCIONAL"}}}])["result"][0]["avg"]
    promediosHidraulicaConvencional.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$CARBON"}}}])["result"][0]["avg"]
    promediosCarbon.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$CICLO_COMBINADO"}}}])["result"][0]["avg"]
    promediosCicloCombinado.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$FUEL_GAS"}}}])["result"][0]["avg"]
    promediosFuelGas.insert(indice, round(query,2))
    promediosDesde.insert(indice, fecha)
    promediosHasta.insert(indice, fecha2)

    ''' Promedio dia anterior '''
#     db = MongoClient(host=CONN_HOST).mercadodiario
#     my_date_str = datetime.now().strftime("%Y-%m-%dT00:00:00Z")
#     fecha3 = parser.parse(my_date_str) - timedelta(3)
    fecha3 = fecha_aux.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(3)
    fecha2 = fecha3 - timedelta(days=1)
    fecha = fecha3 - timedelta(days=1)
    indice = 1
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$NUCLEAR"}}}])["result"][0]["avg"]
    promediosNuclear.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$REGIMEN_ESPECIAL"}}}])["result"][0]["avg"]
    promediosRegimenEspecial.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$HIDRAULICA_CONVENCIONAL"}}}])["result"][0]["avg"]
    promediosHidraulicaConvencional.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$CARBON"}}}])["result"][0]["avg"]
    promediosCarbon.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$CICLO_COMBINADO"}}}])["result"][0]["avg"]
    promediosCicloCombinado.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$FUEL_GAS"}}}])["result"][0]["avg"]
    promediosFuelGas.insert(indice, round(query,2))
    promediosDesde.insert(indice, fecha)
    promediosHasta.insert(indice, fecha2)

    ''' Promedio semana actual '''
#     db = MongoClient(host=CONN_HOST).mercadodiario
#     my_date_str = datetime.now().strftime("%Y-%m-%dT00:00:00Z")
#     fecha2 = parser.parse(my_date_str) - timedelta(3)
    fecha2 = fecha_aux.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(3)
    fecha = fecha2 - timedelta(weeks=1) + timedelta(days=1)
    indice = 2
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$NUCLEAR"}}}])["result"][0]["avg"]
    promediosNuclear.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$REGIMEN_ESPECIAL"}}}])["result"][0]["avg"]
    promediosRegimenEspecial.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$HIDRAULICA_CONVENCIONAL"}}}])["result"][0]["avg"]
    promediosHidraulicaConvencional.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$CARBON"}}}])["result"][0]["avg"]
    promediosCarbon.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$CICLO_COMBINADO"}}}])["result"][0]["avg"]
    promediosCicloCombinado.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$FUEL_GAS"}}}])["result"][0]["avg"]
    promediosFuelGas.insert(indice, round(query,2))
    promediosDesde.insert(indice, fecha)
    promediosHasta.insert(indice, fecha2)

    ''' Promedio semana anterior '''
#     db = MongoClient(host=CONN_HOST).mercadodiario
#     my_date_str = datetime.now().strftime("%Y-%m-%dT00:00:00Z")
#     fecha3 = parser.parse(my_date_str) - timedelta(3)
    fecha3 = fecha_aux.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(3)
    fecha2 = fecha3 - timedelta(weeks=1)
    fecha = fecha3 - timedelta(weeks=2) + timedelta(days=1)
    indice = 3
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$NUCLEAR"}}}])["result"][0]["avg"]
    promediosNuclear.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$REGIMEN_ESPECIAL"}}}])["result"][0]["avg"]
    promediosRegimenEspecial.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$HIDRAULICA_CONVENCIONAL"}}}])["result"][0]["avg"]
    promediosHidraulicaConvencional.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$CARBON"}}}])["result"][0]["avg"]
    promediosCarbon.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$CICLO_COMBINADO"}}}])["result"][0]["avg"]
    promediosCicloCombinado.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$FUEL_GAS"}}}])["result"][0]["avg"]
    promediosFuelGas.insert(indice, round(query,2))
    promediosDesde.insert(indice, fecha)
    promediosHasta.insert(indice, fecha2)

    ''' Promedio mes actual '''
#     db = MongoClient(host=CONN_HOST).mercadodiario
#     my_date_str = datetime.now().strftime("%Y-%m-%dT00:00:00Z")
#     fecha2 = parser.parse(my_date_str) - timedelta(3)
    fecha2 = fecha_aux.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(3)
#     fecha = fecha2.replace(month=fecha2.month - 1)
    fecha = (fecha2 - timedelta(weeks=4) - timedelta(days=2)).replace(day=fecha2.day) + timedelta(days=1)
    indice = 4
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$NUCLEAR"}}}])["result"][0]["avg"]
    promediosNuclear.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$REGIMEN_ESPECIAL"}}}])["result"][0]["avg"]
    promediosRegimenEspecial.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$HIDRAULICA_CONVENCIONAL"}}}])["result"][0]["avg"]
    promediosHidraulicaConvencional.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$CARBON"}}}])["result"][0]["avg"]
    promediosCarbon.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$CICLO_COMBINADO"}}}])["result"][0]["avg"]
    promediosCicloCombinado.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$FUEL_GAS"}}}])["result"][0]["avg"]
    promediosFuelGas.insert(indice, round(query,2))
    promediosDesde.insert(indice, fecha)
    promediosHasta.insert(indice, fecha2)

    ''' Promedio mes anterior '''
#     db = MongoClient(host=CONN_HOST).mercadodiario
#     my_date_str = datetime.now().strftime("%Y-%m-%dT00:00:00Z")
#     fecha3 = parser.parse(my_date_str) - timedelta(3)
    fecha2 = fecha_aux.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(3)
#     fecha2 = fecha3.replace(month=fecha3.month - 1)
    fecha2 = (fecha3 - timedelta(weeks=4) - timedelta(days=2)).replace(day=fecha3.day)
#     fecha = fecha2.replace(month=fecha2.month - 1)
    fecha = (fecha3 - timedelta(weeks=8) - timedelta(days=4)).replace(day=fecha3.day) + timedelta(days=1)
    indice = 5
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$NUCLEAR"}}}])["result"][0]["avg"]
    promediosNuclear.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$REGIMEN_ESPECIAL"}}}])["result"][0]["avg"]
    promediosRegimenEspecial.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$HIDRAULICA_CONVENCIONAL"}}}])["result"][0]["avg"]
    promediosHidraulicaConvencional.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$CARBON"}}}])["result"][0]["avg"]
    promediosCarbon.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$CICLO_COMBINADO"}}}])["result"][0]["avg"]
    promediosCicloCombinado.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$FUEL_GAS"}}}])["result"][0]["avg"]
    promediosFuelGas.insert(indice, round(query,2))
    promediosDesde.insert(indice, fecha)
    promediosHasta.insert(indice, fecha2)

    ''' Promedio estacion actual '''
#     db = MongoClient(host=CONN_HOST).mercadodiario
#     my_date_str = datetime.now().strftime("%Y-%m-%dT00:00:00Z")
#     fecha2 = parser.parse(my_date_str) - timedelta(3)
    fecha2 = fecha_aux.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(3)
#     fecha = fecha2.replace(month=fecha2.month - 3)
    fecha = (fecha2 - timedelta(weeks=13)).replace(day=fecha2.day) + timedelta(days=1)
    indice = 6
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$NUCLEAR"}}}])["result"][0]["avg"]
    promediosNuclear.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$REGIMEN_ESPECIAL"}}}])["result"][0]["avg"]
    promediosRegimenEspecial.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$HIDRAULICA_CONVENCIONAL"}}}])["result"][0]["avg"]
    promediosHidraulicaConvencional.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$CARBON"}}}])["result"][0]["avg"]
    promediosCarbon.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$CICLO_COMBINADO"}}}])["result"][0]["avg"]
    promediosCicloCombinado.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$FUEL_GAS"}}}])["result"][0]["avg"]
    promediosFuelGas.insert(indice, round(query,2))
    promediosDesde.insert(indice, fecha)
    promediosHasta.insert(indice, fecha2)

    ''' Promedio estacion anterior '''
#     db = MongoClient(host=CONN_HOST).mercadodiario
#     my_date_str = datetime.now().strftime("%Y-%m-%dT00:00:00Z")
#     fecha3 = parser.parse(my_date_str) - timedelta(3)
    fecha3 = fecha_aux.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(3)
#     fecha2 = fecha3.replace(month=fecha3.month - 1)
    fecha2 = (fecha3 - timedelta(weeks=13)).replace(day=fecha3.day)
#     fecha = fecha2.replace(month=fecha2.month - 3)
    fecha = (fecha3 - timedelta(weeks=26)).replace(day=fecha3.day) + timedelta(days=1)
    indice = 7
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$NUCLEAR"}}}])["result"][0]["avg"]
    promediosNuclear.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$REGIMEN_ESPECIAL"}}}])["result"][0]["avg"]
    promediosRegimenEspecial.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$HIDRAULICA_CONVENCIONAL"}}}])["result"][0]["avg"]
    promediosHidraulicaConvencional.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$CARBON"}}}])["result"][0]["avg"]
    promediosCarbon.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$CICLO_COMBINADO"}}}])["result"][0]["avg"]
    promediosCicloCombinado.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$FUEL_GAS"}}}])["result"][0]["avg"]
    promediosFuelGas.insert(indice, round(query,2))
    promediosDesde.insert(indice, fecha)
    promediosHasta.insert(indice, fecha2)

    ''' Promedio año actual '''
#     db = MongoClient(host=CONN_HOST).mercadodiario
#     my_date_str = datetime.now().strftime("%Y-%m-%dT00:00:00Z")
#     fecha2 = parser.parse(my_date_str) - timedelta(3)
    fecha2 = fecha_aux.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(3)
#     fecha = fecha2.replace(year=fecha2.year - 1)
    fecha = (fecha2 - timedelta(weeks=52)).replace(day=fecha2.day) + timedelta(days=1)
    indice = 8
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$NUCLEAR"}}}])["result"][0]["avg"]
    promediosNuclear.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$REGIMEN_ESPECIAL"}}}])["result"][0]["avg"]
    promediosRegimenEspecial.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$HIDRAULICA_CONVENCIONAL"}}}])["result"][0]["avg"]
    promediosHidraulicaConvencional.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$CARBON"}}}])["result"][0]["avg"]
    promediosCarbon.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$CICLO_COMBINADO"}}}])["result"][0]["avg"]
    promediosCicloCombinado.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$FUEL_GAS"}}}])["result"][0]["avg"]
    promediosFuelGas.insert(indice, round(query,2))
    promediosDesde.insert(indice, fecha)
    promediosHasta.insert(indice, fecha2)

    ''' Promedio año anterior '''
#     db = MongoClient(host=CONN_HOST).mercadodiario
#     my_date_str = datetime.now().strftime("%Y-%m-%dT00:00:00Z")
#     fecha3 = parser.parse(my_date_str) - timedelta(3)
    fecha3 = fecha_aux.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(3)
#     fecha2 = fecha3.replace(year=fecha3.year - 1)
    fecha2 = (fecha3 - timedelta(weeks=52)).replace(day=fecha3.day)
#     fecha = fecha2.replace(year=fecha2.year - 1)
    fecha = (fecha3 - timedelta(weeks=104)).replace(day=fecha3.day) + timedelta(days=1)
    indice = 9
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$NUCLEAR"}}}])["result"][0]["avg"]
    promediosNuclear.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$REGIMEN_ESPECIAL"}}}])["result"][0]["avg"]
    promediosRegimenEspecial.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$HIDRAULICA_CONVENCIONAL"}}}])["result"][0]["avg"]
    promediosHidraulicaConvencional.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$CARBON"}}}])["result"][0]["avg"]
    promediosCarbon.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$CICLO_COMBINADO"}}}])["result"][0]["avg"]
    promediosCicloCombinado.insert(indice, round(query,2))
    query = db.tecnologiases.aggregate([{"$match": {"fecha": {"$gte": fecha, "$lte": fecha2}}}, {"$group": {"_id": "null", "avg": {"$avg": "$FUEL_GAS"}}}])["result"][0]["avg"]
    promediosFuelGas.insert(indice, round(query,2))
    promediosDesde.insert(indice, fecha)
    promediosHasta.insert(indice, fecha2)

    return promediosNuclear, promediosRegimenEspecial, promediosHidraulicaConvencional, promediosCarbon, promediosCicloCombinado, promediosFuelGas, promediosDesde, promediosHasta

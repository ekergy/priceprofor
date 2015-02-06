# -*- coding: utf-8 -*-
import omieMercadoDiarioDBManager
import datetime

# Aggregations/Projections and other informacion on for PreciosWeb:

# Aggregations/Projections and other informacion on for TecnologiasWeb:

# Aggregations/Projections and other informacion on for TecnologiasWeb:

# Aggregations/Projections and other informacion on for StudyDataMIBEL:

def volumenesanhoStudyDataMIBEL():
    """Devuelve los volumenes en MWh y en EURs por año:

    {max de cada campo (fecha,valor)}
    {max de cada en Volumen Eurs(fecha,valor)}
    {max de precio cada en Volumen Eurs(fecha,valor)}

    """
    result = omieMercadoDiarioDBManager.StudyDataMIBEL._get_collection().aggregate([
    {"$project": {
       'year': { '$year': "$fecha" },
       'VOLUMEN_HIDRAULICA_MWH': "$P_TOTAL_HIDRAULICA" ,
       'VOLUMEN_HIDRAULICA_EUR': { '$multiply': [ "$precio", "$P_TOTAL_HIDRAULICA" ] } ,
       'VOLUMEN_TERMICA_MWH': "$P_TOTAL_TERMICA" ,
       'VOLUMEN_TERMICA_EUR': { '$multiply': [ "$precio", "$P_TOTAL_TERMICA" ] } ,
       'VOLUMEN_REGIMEN_ESPECIAL_MWH': "$P_TOTAL_REGIMEN_ESPECIAL" ,
       'VOLUMEN_REGIMEN_ESPECIAL_EUR': { '$multiply': [ "$precio", "$P_TOTAL_REGIMEN_ESPECIAL" ] } ,
       'VOLUMEN_IMPORTACION_MWH': "$P_TOTAL_IMPORTACION" ,
       'VOLUMEN_IMPORTACION_EUR': { '$multiply': [ "$precio", "$P_TOTAL_IMPORTACION" ] } ,
       'VOLUMEN_GENERICAS_MWH': "$P_TOTAL_GENERICAS" ,
       'VOLUMEN_GENERICAS_EUR': { '$multiply': [ "$precio", "$P_TOTAL_GENERICAS" ] } ,
    }},
    {'$group': 
    {'_id': '$year', 
        'TOTAL_VOLUMEN_HIDRAULICA_MWH': {'$sum': "$VOLUMEN_HIDRAULICA_MWH"},
        'TOTAL_VOLUMEN_HIDRAULICA_EUR': {'$sum': "$VOLUMEN_HIDRAULICA_EUR"},
        'TOTAL_VOLUMEN_TERMICA_MWH': {'$sum': "$VOLUMEN_TERMICA_MWH"},
        'TOTAL_VOLUMEN_TERMICA_EUR': {'$sum': "$VOLUMEN_TERMICA_EUR"},
        'TOTAL_VOLUMEN_REGIMEN_ESPECIAL_MWH': {'$sum': "$VOLUMEN_REGIMEN_ESPECIAL_MWH"},
        'TOTAL_VOLUMEN_REGIMEN_ESPECIAL_EUR': {'$sum': "$VOLUMEN_REGIMEN_ESPECIAL_EUR"},
        'TOTAL_VOLUMEN_IMPORTACION_MWH': {'$sum': "$VOLUMEN_IMPORTACION_MWH"},
        'TOTAL_VOLUMEN_IMPORTACION_EUR': {'$sum': "$VOLUMEN_IMPORTACION_EUR"},
        'TOTAL_VOLUMEN_GENERICAS_MWH': {'$sum': "$VOLUMEN_GENERICAS_MWH"},
        'TOTAL_VOLUMEN_GENERICAS_EUR': {'$sum': "$VOLUMEN_GENERICAS_EUR"},
    }},
        ])

    return result

def volumenesmesesStudyDataMIBEL(anho):
    """Dado un año Devuelve los volumenes en MWh y en EURs por meses:

    {max de cada campo (fecha,valor)}
    {max de cada en Volumen Eurs(fecha,valor)}
    {max de precio cada en Volumen Eurs(fecha,valor)}

    """
    result = omieMercadoDiarioDBManager.StudyDataMIBEL._get_collection().aggregate([
    {"$project": {
       'year': { '$year': "$fecha" },
       'month': { '$month': "$fecha" },
       'VOLUMEN_HIDRAULICA_MWH': "$P_TOTAL_HIDRAULICA" ,
       'VOLUMEN_HIDRAULICA_EUR': { '$multiply': [ "$precio", "$P_TOTAL_HIDRAULICA" ] } ,
       'VOLUMEN_TERMICA_MWH': "$P_TOTAL_TERMICA" ,
       'VOLUMEN_TERMICA_EUR': { '$multiply': [ "$precio", "$P_TOTAL_TERMICA" ] } ,
       'VOLUMEN_REGIMEN_ESPECIAL_MWH': "$P_TOTAL_REGIMEN_ESPECIAL" ,
       'VOLUMEN_REGIMEN_ESPECIAL_EUR': { '$multiply': [ "$precio", "$P_TOTAL_REGIMEN_ESPECIAL" ] } ,
       'VOLUMEN_IMPORTACION_MWH': "$P_TOTAL_IMPORTACION" ,
       'VOLUMEN_IMPORTACION_EUR': { '$multiply': [ "$precio", "$P_TOTAL_IMPORTACION" ] } ,
       'VOLUMEN_GENERICAS_MWH': "$P_TOTAL_GENERICAS" ,
       'VOLUMEN_GENERICAS_EUR': { '$multiply': [ "$precio", "$P_TOTAL_GENERICAS" ] } ,
    }},
    { "$match" : { "year" : int(anho) } },
    {'$group': 
    {'_id': '$month', 
        'TOTAL_VOLUMEN_HIDRAULICA_MWH': {'$sum': "$VOLUMEN_HIDRAULICA_MWH"},
        'TOTAL_VOLUMEN_HIDRAULICA_EUR': {'$sum': "$VOLUMEN_HIDRAULICA_EUR"},
        'TOTAL_VOLUMEN_TERMICA_MWH': {'$sum': "$VOLUMEN_TERMICA_MWH"},
        'TOTAL_VOLUMEN_TERMICA_EUR': {'$sum': "$VOLUMEN_TERMICA_EUR"},
        'TOTAL_VOLUMEN_REGIMEN_ESPECIAL_MWH': {'$sum': "$VOLUMEN_REGIMEN_ESPECIAL_MWH"},
        'TOTAL_VOLUMEN_REGIMEN_ESPECIAL_EUR': {'$sum': "$VOLUMEN_REGIMEN_ESPECIAL_EUR"},
        'TOTAL_VOLUMEN_IMPORTACION_MWH': {'$sum': "$VOLUMEN_IMPORTACION_MWH"},
        'TOTAL_VOLUMEN_IMPORTACION_EUR': {'$sum': "$VOLUMEN_IMPORTACION_EUR"},
        'TOTAL_VOLUMEN_GENERICAS_MWH': {'$sum': "$VOLUMEN_GENERICAS_MWH"},
        'TOTAL_VOLUMEN_GENERICAS_EUR': {'$sum': "$VOLUMEN_GENERICAS_EUR"},
    }},
        ])

    
    return result

def volumenessemanasStudyDataMIBEL(anho):
    """Dado un año Devuelve los volumenes en MWh y en EURs por semanas:

    {max de cada campo (fecha,valor)}
    {max de cada en Volumen Eurs(fecha,valor)}
    {max de precio cada en Volumen Eurs(fecha,valor)}

    """
    result = omieMercadoDiarioDBManager.StudyDataMIBEL._get_collection().aggregate([
    {"$project": {
       'year': { '$year': "$fecha" },
       'week': { '$week': "$fecha" },
       'VOLUMEN_HIDRAULICA_MWH': "$P_TOTAL_HIDRAULICA" ,
       'VOLUMEN_HIDRAULICA_EUR': { '$multiply': [ "$precio", "$P_TOTAL_HIDRAULICA" ] } ,
       'VOLUMEN_TERMICA_MWH': "$P_TOTAL_TERMICA" ,
       'VOLUMEN_TERMICA_EUR': { '$multiply': [ "$precio", "$P_TOTAL_TERMICA" ] } ,
       'VOLUMEN_REGIMEN_ESPECIAL_MWH': "$P_TOTAL_REGIMEN_ESPECIAL" ,
       'VOLUMEN_REGIMEN_ESPECIAL_EUR': { '$multiply': [ "$precio", "$P_TOTAL_REGIMEN_ESPECIAL" ] } ,
       'VOLUMEN_IMPORTACION_MWH': "$P_TOTAL_IMPORTACION" ,
       'VOLUMEN_IMPORTACION_EUR': { '$multiply': [ "$precio", "$P_TOTAL_IMPORTACION" ] } ,
       'VOLUMEN_GENERICAS_MWH': "$P_TOTAL_GENERICAS" ,
       'VOLUMEN_GENERICAS_EUR': { '$multiply': [ "$precio", "$P_TOTAL_GENERICAS" ] } ,
    }},
    { "$match" : { "year" : int(anho) } },
    {'$group': 
    {'_id': '$week', 
        'TOTAL_VOLUMEN_HIDRAULICA_MWH': {'$sum': "$VOLUMEN_HIDRAULICA_MWH"},
        'TOTAL_VOLUMEN_HIDRAULICA_EUR': {'$sum': "$VOLUMEN_HIDRAULICA_EUR"},
        'TOTAL_VOLUMEN_TERMICA_MWH': {'$sum': "$VOLUMEN_TERMICA_MWH"},
        'TOTAL_VOLUMEN_TERMICA_EUR': {'$sum': "$VOLUMEN_TERMICA_EUR"},
        'TOTAL_VOLUMEN_REGIMEN_ESPECIAL_MWH': {'$sum': "$VOLUMEN_REGIMEN_ESPECIAL_MWH"},
        'TOTAL_VOLUMEN_REGIMEN_ESPECIAL_EUR': {'$sum': "$VOLUMEN_REGIMEN_ESPECIAL_EUR"},
        'TOTAL_VOLUMEN_IMPORTACION_MWH': {'$sum': "$VOLUMEN_IMPORTACION_MWH"},
        'TOTAL_VOLUMEN_IMPORTACION_EUR': {'$sum': "$VOLUMEN_IMPORTACION_EUR"},
        'TOTAL_VOLUMEN_GENERICAS_MWH': {'$sum': "$VOLUMEN_GENERICAS_MWH"},
        'TOTAL_VOLUMEN_GENERICAS_EUR': {'$sum': "$VOLUMEN_GENERICAS_EUR"},
    }},
        ])

    
    return result

def volumenediassemanaStudyDataMIBEL(anho):
    """Dado un año Devuelve los volumenes en MWh y en EURs por los dias de las semanas:

    {max de cada campo (fecha,valor)}
    {max de cada en Volumen Eurs(fecha,valor)}
    {max de precio cada en Volumen Eurs(fecha,valor)}

    """
    result = omieMercadoDiarioDBManager.StudyDataMIBEL._get_collection().aggregate([
    {"$project": {
       'year': { '$year': "$fecha" },
       'dayOfWeek': { '$dayOfWeek': "$fecha" },
       'VOLUMEN_HIDRAULICA_MWH': "$P_TOTAL_HIDRAULICA" ,
       'VOLUMEN_HIDRAULICA_EUR': { '$multiply': [ "$precio", "$P_TOTAL_HIDRAULICA" ] } ,
       'VOLUMEN_TERMICA_MWH': "$P_TOTAL_TERMICA" ,
       'VOLUMEN_TERMICA_EUR': { '$multiply': [ "$precio", "$P_TOTAL_TERMICA" ] } ,
       'VOLUMEN_REGIMEN_ESPECIAL_MWH': "$P_TOTAL_REGIMEN_ESPECIAL" ,
       'VOLUMEN_REGIMEN_ESPECIAL_EUR': { '$multiply': [ "$precio", "$P_TOTAL_REGIMEN_ESPECIAL" ] } ,
       'VOLUMEN_IMPORTACION_MWH': "$P_TOTAL_IMPORTACION" ,
       'VOLUMEN_IMPORTACION_EUR': { '$multiply': [ "$precio", "$P_TOTAL_IMPORTACION" ] } ,
       'VOLUMEN_GENERICAS_MWH': "$P_TOTAL_GENERICAS" ,
       'VOLUMEN_GENERICAS_EUR': { '$multiply': [ "$precio", "$P_TOTAL_GENERICAS" ] } ,
    }},
    { "$match" : { "year" : int(anho) } },
    {'$group': 
    {'_id': '$dayOfWeek', 
        'TOTAL_VOLUMEN_HIDRAULICA_MWH': {'$sum': "$VOLUMEN_HIDRAULICA_MWH"},
        'TOTAL_VOLUMEN_HIDRAULICA_EUR': {'$sum': "$VOLUMEN_HIDRAULICA_EUR"},
        'TOTAL_VOLUMEN_TERMICA_MWH': {'$sum': "$VOLUMEN_TERMICA_MWH"},
        'TOTAL_VOLUMEN_TERMICA_EUR': {'$sum': "$VOLUMEN_TERMICA_EUR"},
        'TOTAL_VOLUMEN_REGIMEN_ESPECIAL_MWH': {'$sum': "$VOLUMEN_REGIMEN_ESPECIAL_MWH"},
        'TOTAL_VOLUMEN_REGIMEN_ESPECIAL_EUR': {'$sum': "$VOLUMEN_REGIMEN_ESPECIAL_EUR"},
        'TOTAL_VOLUMEN_IMPORTACION_MWH': {'$sum': "$VOLUMEN_IMPORTACION_MWH"},
        'TOTAL_VOLUMEN_IMPORTACION_EUR': {'$sum': "$VOLUMEN_IMPORTACION_EUR"},
        'TOTAL_VOLUMEN_GENERICAS_MWH': {'$sum': "$VOLUMEN_GENERICAS_MWH"},
        'TOTAL_VOLUMEN_GENERICAS_EUR': {'$sum': "$VOLUMEN_GENERICAS_EUR"},
    }},
        ])

    
    return result

def volumeneshorasStudyDataMIBEL(anho):
    """Dado un año Devuelve los volumenes en MWh y en EURs por horas del dia:

    {max de cada campo (fecha,valor)}
    {max de cada en Volumen Eurs(fecha,valor)}
    {max de precio cada en Volumen Eurs(fecha,valor)}

    """
    result = omieMercadoDiarioDBManager.StudyDataMIBEL._get_collection().aggregate([
    {"$project": {
       'year': { '$year': "$fecha" },
       'hour': { '$hour': "$fecha" },
       'VOLUMEN_HIDRAULICA_MWH': "$P_TOTAL_HIDRAULICA" ,
       'VOLUMEN_HIDRAULICA_EUR': { '$multiply': [ "$precio", "$P_TOTAL_HIDRAULICA" ] } ,
       'VOLUMEN_TERMICA_MWH': "$P_TOTAL_TERMICA" ,
       'VOLUMEN_TERMICA_EUR': { '$multiply': [ "$precio", "$P_TOTAL_TERMICA" ] } ,
       'VOLUMEN_REGIMEN_ESPECIAL_MWH': "$P_TOTAL_REGIMEN_ESPECIAL" ,
       'VOLUMEN_REGIMEN_ESPECIAL_EUR': { '$multiply': [ "$precio", "$P_TOTAL_REGIMEN_ESPECIAL" ] } ,
       'VOLUMEN_IMPORTACION_MWH': "$P_TOTAL_IMPORTACION" ,
       'VOLUMEN_IMPORTACION_EUR': { '$multiply': [ "$precio", "$P_TOTAL_IMPORTACION" ] } ,
       'VOLUMEN_GENERICAS_MWH': "$P_TOTAL_GENERICAS" ,
       'VOLUMEN_GENERICAS_EUR': { '$multiply': [ "$precio", "$P_TOTAL_GENERICAS" ] } ,
    }},
    { "$match" : { "year" : int(anho) } },
    {'$group': 
    {'_id': '$hour', 
        'TOTAL_VOLUMEN_HIDRAULICA_MWH': {'$sum': "$VOLUMEN_HIDRAULICA_MWH"},
        'TOTAL_VOLUMEN_HIDRAULICA_EUR': {'$sum': "$VOLUMEN_HIDRAULICA_EUR"},
        'TOTAL_VOLUMEN_TERMICA_MWH': {'$sum': "$VOLUMEN_TERMICA_MWH"},
        'TOTAL_VOLUMEN_TERMICA_EUR': {'$sum': "$VOLUMEN_TERMICA_EUR"},
        'TOTAL_VOLUMEN_REGIMEN_ESPECIAL_MWH': {'$sum': "$VOLUMEN_REGIMEN_ESPECIAL_MWH"},
        'TOTAL_VOLUMEN_REGIMEN_ESPECIAL_EUR': {'$sum': "$VOLUMEN_REGIMEN_ESPECIAL_EUR"},
        'TOTAL_VOLUMEN_IMPORTACION_MWH': {'$sum': "$VOLUMEN_IMPORTACION_MWH"},
        'TOTAL_VOLUMEN_IMPORTACION_EUR': {'$sum': "$VOLUMEN_IMPORTACION_EUR"},
        'TOTAL_VOLUMEN_GENERICAS_MWH': {'$sum': "$VOLUMEN_GENERICAS_MWH"},
        'TOTAL_VOLUMEN_GENERICAS_EUR': {'$sum': "$VOLUMEN_GENERICAS_EUR"},
    }},
        ])

    
    return result

def volumenesdiaStudyDataMIBEL(anho):
    """Dado un año Devuelve los volumenes en MWh y en EURs por cada del dia:

    {max de cada campo (fecha,valor)}
    {max de cada en Volumen Eurs(fecha,valor)}
    {max de precio cada en Volumen Eurs(fecha,valor)}

    """
    result = omieMercadoDiarioDBManager.StudyDataMIBEL._get_collection().aggregate([
    {"$project": {
       'year': { '$year': "$fecha" },
       'day': { '$dayOfYear': "$fecha" },
       'VOLUMEN_HIDRAULICA_MWH': "$P_TOTAL_HIDRAULICA" ,
       'VOLUMEN_HIDRAULICA_EUR': { '$multiply': [ "$precio", "$P_TOTAL_HIDRAULICA" ] } ,
       'VOLUMEN_TERMICA_MWH': "$P_TOTAL_TERMICA" ,
       'VOLUMEN_TERMICA_EUR': { '$multiply': [ "$precio", "$P_TOTAL_TERMICA" ] } ,
       'VOLUMEN_REGIMEN_ESPECIAL_MWH': "$P_TOTAL_REGIMEN_ESPECIAL" ,
       'VOLUMEN_REGIMEN_ESPECIAL_EUR': { '$multiply': [ "$precio", "$P_TOTAL_REGIMEN_ESPECIAL" ] } ,
       'VOLUMEN_IMPORTACION_MWH': "$P_TOTAL_IMPORTACION" ,
       'VOLUMEN_IMPORTACION_EUR': { '$multiply': [ "$precio", "$P_TOTAL_IMPORTACION" ] } ,
       'VOLUMEN_GENERICAS_MWH': "$P_TOTAL_GENERICAS" ,
       'VOLUMEN_GENERICAS_EUR': { '$multiply': [ "$precio", "$P_TOTAL_GENERICAS" ] } ,
    }},
    { "$match" : { "year" : int(anho) } },
    {'$group': 
    {'_id': '$day', 
        'TOTAL_VOLUMEN_HIDRAULICA_MWH': {'$sum': "$VOLUMEN_HIDRAULICA_MWH"},
        'TOTAL_VOLUMEN_HIDRAULICA_EUR': {'$sum': "$VOLUMEN_HIDRAULICA_EUR"},
        'TOTAL_VOLUMEN_TERMICA_MWH': {'$sum': "$VOLUMEN_TERMICA_MWH"},
        'TOTAL_VOLUMEN_TERMICA_EUR': {'$sum': "$VOLUMEN_TERMICA_EUR"},
        'TOTAL_VOLUMEN_REGIMEN_ESPECIAL_MWH': {'$sum': "$VOLUMEN_REGIMEN_ESPECIAL_MWH"},
        'TOTAL_VOLUMEN_REGIMEN_ESPECIAL_EUR': {'$sum': "$VOLUMEN_REGIMEN_ESPECIAL_EUR"},
        'TOTAL_VOLUMEN_IMPORTACION_MWH': {'$sum': "$VOLUMEN_IMPORTACION_MWH"},
        'TOTAL_VOLUMEN_IMPORTACION_EUR': {'$sum': "$VOLUMEN_IMPORTACION_EUR"},
        'TOTAL_VOLUMEN_GENERICAS_MWH': {'$sum': "$VOLUMEN_GENERICAS_MWH"},
        'TOTAL_VOLUMEN_GENERICAS_EUR': {'$sum': "$VOLUMEN_GENERICAS_EUR"},
    }},
        ])

    
    return result




def MaximosMinimosStudyDataMIBEL(startdate=None,enddate=None,):
    """Devuelve los maximos de cada campo y de sus combinaciones con el precio para cada año:

    Aqui posiblemente hay que añadir otros resultados para que se haga 
    """
    if startdate is None and enddate is None:
        results = omieMercadoDiarioDBManager.StudyDataMIBEL._get_collection().aggregate([
    {"$project": {
       'fecha': "$fecha",
       "precio":"$precio",
       'VOLUMEN_HIDRAULICA_MWH': "$P_TOTAL_HIDRAULICA" ,
       'VOLUMEN_HIDRAULICA_EUR': { '$multiply': [ "$precio", "$P_TOTAL_HIDRAULICA" ] } ,
       'VOLUMEN_TERMICA_MWH': "$P_TOTAL_TERMICA" ,
       'VOLUMEN_TERMICA_EUR': { '$multiply': [ "$precio", "$P_TOTAL_TERMICA" ] } ,
       'VOLUMEN_REGIMEN_ESPECIAL_MWH': "$P_TOTAL_REGIMEN_ESPECIAL" ,
       'VOLUMEN_REGIMEN_ESPECIAL_EUR': { '$multiply': [ "$precio", "$P_TOTAL_REGIMEN_ESPECIAL" ] } ,
       'VOLUMEN_IMPORTACION_MWH': "$P_TOTAL_IMPORTACION" ,
       'VOLUMEN_IMPORTACION_EUR': { '$multiply': [ "$precio", "$P_TOTAL_IMPORTACION" ] } ,
       'VOLUMEN_GENERICAS_MWH': "$P_TOTAL_GENERICAS" ,
       'VOLUMEN_GENERICAS_EUR': { '$multiply': [ "$precio", "$P_TOTAL_GENERICAS" ] } ,
    }}
    ])
    elif startdate is None and enddate is not None:
        results = omieMercadoDiarioDBManager.StudyDataMIBEL._get_collection().aggregate([
    {"$project": {
       'fecha': "$fecha",
       "precio":"$precio",
       'VOLUMEN_HIDRAULICA_MWH': "$P_TOTAL_HIDRAULICA" ,
       'VOLUMEN_HIDRAULICA_EUR': { '$multiply': [ "$precio", "$P_TOTAL_HIDRAULICA" ] } ,
       'VOLUMEN_TERMICA_MWH': "$P_TOTAL_TERMICA" ,
       'VOLUMEN_TERMICA_EUR': { '$multiply': [ "$precio", "$P_TOTAL_TERMICA" ] } ,
       'VOLUMEN_REGIMEN_ESPECIAL_MWH': "$P_TOTAL_REGIMEN_ESPECIAL" ,
       'VOLUMEN_REGIMEN_ESPECIAL_EUR': { '$multiply': [ "$precio", "$P_TOTAL_REGIMEN_ESPECIAL" ] } ,
       'VOLUMEN_IMPORTACION_MWH': "$P_TOTAL_IMPORTACION" ,
       'VOLUMEN_IMPORTACION_EUR': { '$multiply': [ "$precio", "$P_TOTAL_IMPORTACION" ] } ,
       'VOLUMEN_GENERICAS_MWH': "$P_TOTAL_GENERICAS" ,
       'VOLUMEN_GENERICAS_EUR': { '$multiply': [ "$precio", "$P_TOTAL_GENERICAS" ] } ,
    }},
    {'$match': {'fecha' : {'$lt': enddate }}}
    ])
    elif startdate is not None and enddate is None:
            results = omieMercadoDiarioDBManager.StudyDataMIBEL._get_collection().aggregate([
    {"$project": {
       'fecha': "$fecha",
       "precio":"$precio",
       'VOLUMEN_HIDRAULICA_MWH': "$P_TOTAL_HIDRAULICA" ,
       'VOLUMEN_HIDRAULICA_EUR': { '$multiply': [ "$precio", "$P_TOTAL_HIDRAULICA" ] } ,
       'VOLUMEN_TERMICA_MWH': "$P_TOTAL_TERMICA" ,
       'VOLUMEN_TERMICA_EUR': { '$multiply': [ "$precio", "$P_TOTAL_TERMICA" ] } ,
       'VOLUMEN_REGIMEN_ESPECIAL_MWH': "$P_TOTAL_REGIMEN_ESPECIAL" ,
       'VOLUMEN_REGIMEN_ESPECIAL_EUR': { '$multiply': [ "$precio", "$P_TOTAL_REGIMEN_ESPECIAL" ] } ,
       'VOLUMEN_IMPORTACION_MWH': "$P_TOTAL_IMPORTACION" ,
       'VOLUMEN_IMPORTACION_EUR': { '$multiply': [ "$precio", "$P_TOTAL_IMPORTACION" ] } ,
       'VOLUMEN_GENERICAS_MWH': "$P_TOTAL_GENERICAS" ,
       'VOLUMEN_GENERICAS_EUR': { '$multiply': [ "$precio", "$P_TOTAL_GENERICAS" ] } ,
    }},
    {'$match': {'fecha' : {'$gt': startdate }}}
    ])
    else:
            results = omieMercadoDiarioDBManager.StudyDataMIBEL._get_collection().aggregate([
    {"$project": {
       'fecha': "$fecha",
       "precio":"$precio",
       'VOLUMEN_HIDRAULICA_MWH': "$P_TOTAL_HIDRAULICA" ,
       'VOLUMEN_HIDRAULICA_EUR': { '$multiply': [ "$precio", "$P_TOTAL_HIDRAULICA" ] } ,
       'VOLUMEN_TERMICA_MWH': "$P_TOTAL_TERMICA" ,
       'VOLUMEN_TERMICA_EUR': { '$multiply': [ "$precio", "$P_TOTAL_TERMICA" ] } ,
       'VOLUMEN_REGIMEN_ESPECIAL_MWH': "$P_TOTAL_REGIMEN_ESPECIAL" ,
       'VOLUMEN_REGIMEN_ESPECIAL_EUR': { '$multiply': [ "$precio", "$P_TOTAL_REGIMEN_ESPECIAL" ] } ,
       'VOLUMEN_IMPORTACION_MWH': "$P_TOTAL_IMPORTACION" ,
       'VOLUMEN_IMPORTACION_EUR': { '$multiply': [ "$precio", "$P_TOTAL_IMPORTACION" ] } ,
       'VOLUMEN_GENERICAS_MWH': "$P_TOTAL_GENERICAS" ,
       'VOLUMEN_GENERICAS_EUR': { '$multiply': [ "$precio", "$P_TOTAL_GENERICAS" ] } ,
    }},
    {'$match': {'fecha' : {'$gt': startdate ,'$lt': enddate }}}
    ])
    # {'$sort':{"precio":-1}},
    # {'$limit':1}
    # how to effecitly get each record for each container¿?
    
    MAXIMOS = {
    'MAX_VOLUMEN_HIDRAULICA_MWH' : {'fecha':datetime.datetime(2011,1,1,1),'valor':0.0},
    'MAX_VOLUMEN_HIDRAULICA_EUR' : {'fecha':datetime.datetime(2011,1,1,1),'valor':0.0},
    'MAX_VOLUMEN_TERMICA_MWH' : {'fecha':datetime.datetime(2011,1,1,1),'valor':0.0},
    'MAX_VOLUMEN_TERMICA_EUR' : {'fecha':datetime.datetime(2011,1,1,1),'valor':0.0},
    'MAX_VOLUMEN_REGIMEN_ESPECIAL_MWH' : {'fecha':datetime.datetime(2011,1,1,1),'valor':0.0},
    'MAX_VOLUMEN_REGIMEN_ESPECIAL_EUR' : {'fecha':datetime.datetime(2011,1,1,1),'valor':0.0},
    'MAX_VOLUMEN_IMPORTACION_MWH' : {'fecha':datetime.datetime(2011,1,1,1),'valor':0.0},
    'MAX_VOLUMEN_IMPORTACION_EUR' : {'fecha':datetime.datetime(2011,1,1,1),'valor':0.0},
    'MAX_VOLUMEN_GENERICAS_MWH' : {'fecha':datetime.datetime(2011,1,1,1),'valor':0.0},
    'MAX_VOLUMEN_GENERICAS_EUR' : {'fecha':datetime.datetime(2011,1,1,1),'valor':0.0},
    }
    MINIMOS = {
    'MIN_VOLUMEN_HIDRAULICA_MWH' : {'fecha':datetime.datetime(2011,1,1,1),'valor':2.0**100},
    'MIN_VOLUMEN_HIDRAULICA_EUR' : {'fecha':datetime.datetime(2011,1,1,1),'valor':2.0**100},
    'MIN_VOLUMEN_TERMICA_MWH' : {'fecha':datetime.datetime(2011,1,1,1),'valor':2.0**100},
    'MIN_VOLUMEN_TERMICA_EUR' : {'fecha':datetime.datetime(2011,1,1,1),'valor':2.0**100},
    'MIN_VOLUMEN_REGIMEN_ESPECIAL_MWH' : {'fecha':datetime.datetime(2011,1,1,1),'valor':2.0**100},
    'MIN_VOLUMEN_REGIMEN_ESPECIAL_EUR' : {'fecha':datetime.datetime(2011,1,1,1),'valor':2.0**100},
    'MIN_VOLUMEN_IMPORTACION_MWH' : {'fecha':datetime.datetime(2011,1,1,1),'valor':2.0**100},
    'MIN_VOLUMEN_IMPORTACION_EUR' : {'fecha':datetime.datetime(2011,1,1,1),'valor':2.0**100},
    'MIN_VOLUMEN_GENERICAS_MWH' : {'fecha':datetime.datetime(2011,1,1,1),'valor':2.0**100},
    'MIN_VOLUMEN_GENERICAS_EUR' : {'fecha':datetime.datetime(2011,1,1,1),'valor':2.0**100},
    }

    for result in results['result']:
        fecha = result['fecha']
        # Process Maximos
        if result['VOLUMEN_HIDRAULICA_MWH'] >= MAXIMOS['MAX_VOLUMEN_HIDRAULICA_MWH']['valor']:
            MAXIMOS['MAX_VOLUMEN_HIDRAULICA_MWH']['fecha'] = fecha
            MAXIMOS['MAX_VOLUMEN_HIDRAULICA_MWH']['valor'] = result['VOLUMEN_HIDRAULICA_MWH']
        if result['VOLUMEN_HIDRAULICA_EUR'] >= MAXIMOS['MAX_VOLUMEN_HIDRAULICA_EUR']['valor']:
            MAXIMOS['MAX_VOLUMEN_HIDRAULICA_EUR']['fecha'] = fecha
            MAXIMOS['MAX_VOLUMEN_HIDRAULICA_EUR']['valor'] = result['VOLUMEN_HIDRAULICA_EUR']
        if result['VOLUMEN_TERMICA_MWH'] >= MAXIMOS['MAX_VOLUMEN_TERMICA_MWH']['valor']:
            MAXIMOS['MAX_VOLUMEN_TERMICA_MWH']['fecha'] = fecha
            MAXIMOS['MAX_VOLUMEN_TERMICA_MWH']['valor'] = result['VOLUMEN_TERMICA_MWH']
        if result['VOLUMEN_TERMICA_EUR'] >= MAXIMOS['MAX_VOLUMEN_TERMICA_EUR']['valor']:
            MAXIMOS['MAX_VOLUMEN_TERMICA_EUR']['fecha'] = fecha
            MAXIMOS['MAX_VOLUMEN_TERMICA_EUR']['valor'] = result['VOLUMEN_TERMICA_EUR']
        if result['VOLUMEN_REGIMEN_ESPECIAL_MWH'] >= MAXIMOS['MAX_VOLUMEN_REGIMEN_ESPECIAL_MWH']['valor']:
            MAXIMOS['MAX_VOLUMEN_REGIMEN_ESPECIAL_MWH']['fecha'] = fecha
            MAXIMOS['MAX_VOLUMEN_REGIMEN_ESPECIAL_MWH']['valor'] = result['VOLUMEN_REGIMEN_ESPECIAL_MWH']
        if result['VOLUMEN_REGIMEN_ESPECIAL_EUR'] >= MAXIMOS['MAX_VOLUMEN_REGIMEN_ESPECIAL_EUR']['valor']:
            MAXIMOS['MAX_VOLUMEN_REGIMEN_ESPECIAL_EUR']['fecha'] = fecha
            MAXIMOS['MAX_VOLUMEN_REGIMEN_ESPECIAL_EUR']['valor'] = result['VOLUMEN_REGIMEN_ESPECIAL_EUR']
        if result['VOLUMEN_IMPORTACION_MWH'] >= MAXIMOS['MAX_VOLUMEN_IMPORTACION_MWH']['valor']:
            MAXIMOS['MAX_VOLUMEN_IMPORTACION_MWH']['fecha'] = fecha
            MAXIMOS['MAX_VOLUMEN_IMPORTACION_MWH']['valor'] = result['VOLUMEN_IMPORTACION_MWH']
        if result['VOLUMEN_IMPORTACION_EUR'] >= MAXIMOS['MAX_VOLUMEN_IMPORTACION_EUR']['valor']:
            MAXIMOS['MAX_VOLUMEN_IMPORTACION_EUR']['fecha'] = fecha
            MAXIMOS['MAX_VOLUMEN_IMPORTACION_EUR']['valor'] = result['VOLUMEN_IMPORTACION_EUR']
        if result['VOLUMEN_GENERICAS_MWH'] >= MAXIMOS['MAX_VOLUMEN_GENERICAS_MWH']['valor']:
            MAXIMOS['MAX_VOLUMEN_GENERICAS_MWH']['fecha'] = fecha
            MAXIMOS['MAX_VOLUMEN_GENERICAS_MWH']['valor'] = result['VOLUMEN_GENERICAS_MWH']
        if result['VOLUMEN_GENERICAS_EUR'] >= MAXIMOS['MAX_VOLUMEN_GENERICAS_EUR']['valor']:
            MAXIMOS['MAX_VOLUMEN_GENERICAS_EUR']['fecha'] = fecha
            MAXIMOS['MAX_VOLUMEN_GENERICAS_EUR']['valor'] = result['VOLUMEN_GENERICAS_EUR']
        # Process Minimos
        if result['VOLUMEN_HIDRAULICA_MWH'] <= MINIMOS['MIN_VOLUMEN_HIDRAULICA_MWH']['valor']:
            MINIMOS['MIN_VOLUMEN_HIDRAULICA_MWH']['fecha'] = fecha
            MINIMOS['MIN_VOLUMEN_HIDRAULICA_MWH']['valor'] = result['VOLUMEN_HIDRAULICA_MWH']
        if result['VOLUMEN_HIDRAULICA_EUR'] <= MINIMOS['MIN_VOLUMEN_HIDRAULICA_EUR']['valor']:
            MINIMOS['MIN_VOLUMEN_HIDRAULICA_EUR']['fecha'] = fecha
            MINIMOS['MIN_VOLUMEN_HIDRAULICA_EUR']['valor'] = result['VOLUMEN_HIDRAULICA_EUR']
        if result['VOLUMEN_TERMICA_MWH'] <= MINIMOS['MIN_VOLUMEN_TERMICA_MWH']['valor']:
            MINIMOS['MIN_VOLUMEN_TERMICA_MWH']['fecha'] = fecha
            MINIMOS['MIN_VOLUMEN_TERMICA_MWH']['valor'] = result['VOLUMEN_TERMICA_MWH']
        if result['VOLUMEN_TERMICA_EUR'] <= MINIMOS['MIN_VOLUMEN_TERMICA_EUR']['valor']:
            MINIMOS['MIN_VOLUMEN_TERMICA_EUR']['fecha'] = fecha
            MINIMOS['MIN_VOLUMEN_TERMICA_EUR']['valor'] = result['VOLUMEN_TERMICA_EUR']
        if result['VOLUMEN_REGIMEN_ESPECIAL_MWH'] <= MINIMOS['MIN_VOLUMEN_REGIMEN_ESPECIAL_MWH']['valor']:
            MINIMOS['MIN_VOLUMEN_REGIMEN_ESPECIAL_MWH']['fecha'] = fecha
            MINIMOS['MIN_VOLUMEN_REGIMEN_ESPECIAL_MWH']['valor'] = result['VOLUMEN_REGIMEN_ESPECIAL_MWH']
        if result['VOLUMEN_REGIMEN_ESPECIAL_EUR'] <= MINIMOS['MIN_VOLUMEN_REGIMEN_ESPECIAL_EUR']['valor']:
            MINIMOS['MIN_VOLUMEN_REGIMEN_ESPECIAL_EUR']['fecha'] = fecha
            MINIMOS['MIN_VOLUMEN_REGIMEN_ESPECIAL_EUR']['valor'] = result['VOLUMEN_REGIMEN_ESPECIAL_EUR']
        if result['VOLUMEN_IMPORTACION_MWH'] <= MINIMOS['MIN_VOLUMEN_IMPORTACION_MWH']['valor']:
            MINIMOS['MIN_VOLUMEN_IMPORTACION_MWH']['fecha'] = fecha
            MINIMOS['MIN_VOLUMEN_IMPORTACION_MWH']['valor'] = result['VOLUMEN_IMPORTACION_MWH']
        if result['VOLUMEN_IMPORTACION_EUR'] <= MINIMOS['MIN_VOLUMEN_IMPORTACION_EUR']['valor']:
            MINIMOS['MIN_VOLUMEN_IMPORTACION_EUR']['fecha'] = fecha
            MINIMOS['MIN_VOLUMEN_IMPORTACION_EUR']['valor'] = result['VOLUMEN_IMPORTACION_EUR']
        if result['VOLUMEN_GENERICAS_MWH'] <= MINIMOS['MIN_VOLUMEN_GENERICAS_MWH']['valor']:
            MINIMOS['MIN_VOLUMEN_GENERICAS_MWH']['fecha'] = fecha
            MINIMOS['MIN_VOLUMEN_GENERICAS_MWH']['valor'] = result['VOLUMEN_GENERICAS_MWH']
        if result['VOLUMEN_GENERICAS_EUR'] <= MINIMOS['MIN_VOLUMEN_GENERICAS_EUR']['valor']:
            MINIMOS['MIN_VOLUMEN_GENERICAS_EUR']['fecha'] = fecha
            MINIMOS['MIN_VOLUMEN_GENERICAS_EUR']['valor'] = result['VOLUMEN_GENERICAS_EUR']

    return MAXIMOS,MINIMOS
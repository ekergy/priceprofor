 # -*- coding: utf-8 -*-
import omieMercadoDiarioDBManager

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




def MaximosStudyDataMIBEL():
    """Devuelve los maximos de cada campo y de sus combinaciones con el precio para cada año:

    Aqui posiblemente hay que añadir otros resultados para que se haga 
    """
    
    result = omieMercadoDiarioDBManager.StudyDataMIBEL._get_collection().aggregate([
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
    {'$group': 
    {'_id': None, 
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
    {'$sort':precio}
        ])

    return result
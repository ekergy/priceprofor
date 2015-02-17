# -*- coding: utf-8 -*-




def ultimodiaprecios(Mercado):
    """Report for prices in the last day available in precios:

    Arguments:
        Mercado     Can be 'MI','ES','PT' depending in the results that you want to report.

    Result:dict(
        PrecioMedio = "Valor Medio del MWh/EURs"
        PreciosPromedio = "Promedio de los resultos"
        PreciosHorario = "lista de la tupla (i,Precio_i)"
        PrecioMaximo = "lista de la tupla (i,Precio_i) de precio maximo"
        PrecioMinimo = "lista de la tupla (i,Precio_i) de precio maximo"
        )
    """
    # Data needed: 'PreciosHorario':float(), and the date.
    # the other data is deduced by this one.

    result = {
    'PreciosHorario':list(),
    'PreciosPromedio':float(),
    'PreciosHorario':float(),
    'PrecioMaximo':list(),
    'PrecioMinimo':list(),
    }
    return "the results"

def ultimodiafullreport(Mercado):
    """Report for prices in the last day available in precios:

    Arguments:
        Mercado     Can be 'MI','ES','PT' depending in the results that you want to report.

    Result:dict(
        PrecioMedio = "Valor Medio del MWh/EURs"
        PreciosPromedio = "Promedio de los resultos"
        PreciosHorario = "lista de la tupla (i,Precio_i)"
        PrecioMaximo = "lista de la tupla (i,Precio_i) de precio maximo"
        PrecioMinimo = "lista de la tupla (i,Precio_i) de precio maximo"
        )
    """
    if Mercado is not 'ES':
        raise Exception("Other values aren't implemented")

    # Inputs needed:
    
    # The date     datetime.datetime
    
    # Data needed: 'PreciosHorario':list()
    #              'TecnologiasHorarias':list()
    #              'EnergiaGestionadaHoraria':list()

    #


    result = {
    'PreciosHorario':list(),
    'PreciosPromedio':float(),
    'PreciosHorario':float(),
    'PrecioMaximo':list(),
    'PrecioMinimo':list(),
    'VolumenesMWh': {},
    'VolumenesEURs':{}
    }

    return "the results"
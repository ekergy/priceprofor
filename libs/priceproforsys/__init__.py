# -*- coding: utf-8 -*-
#!/usr/bin/env python
# TODO: Add parsers prior to 2014.
# TODO: Fiz saldos in Programa.
# TODO: Add reeHandlersParsers.py to merge all ree*Parser.
# TODO: Add correct unittest to the last specified values.

__author__ = ("Hugo M. Marrao Rodrigues")
__version__ = "0.0.1"
__revision__ = "dev"

# CONN_DETAILS = {'db':'reeMercadoDiario'}

import datetime

def status():
    """This is the status in the database used collection in this Module.
    omie and ree info sys status are not included. Only the managed Collections
    are given in status.
    """
    return "status"

def update():
    """update priceprofor collections
    """
    return "update"


def populateMercadoDiarioMixEs(initfecha=None,endfecha=None):
    """Mercado Diario Mix Es greping data:

    first needs to get data from all databases for a given day.

    Notes to developers:

    """
    try:
        import sys
        sys.path.append('libs/')
        # from omieinfosys import omieMercadoDiarioDBManager
        from reeinfosys import reeMercadoDiarioBDManager
        from .priceproforDBManager import MercadoDiarioMixEs
    except:
        raise Exception("can't import /^(ree|omie)infosys modules.")
    else:
        # TODO: set the proper casuistic for this.
        listadedias = [datetime.datetime(2014,1,1)]

    for dia in listadedias:
        # Get data for precios:
        dia.replace(hour = 0, minute = 0,second = 0,microsecond = 0)
        precios = reeMercadoDiarioBDManager.PreciosWeb.objects(fecha=dia)
        for p in precios:
            precios = p
        TecnologiasCBLdb = reeMercadoDiarioBDManager.TecnologiasCBLWeb.objects(fecha=dia)
        print TecnologiasCBLdb.count()
        for p in TecnologiasCBLdb:
            TecnologiasCBL = p
        TecnologiasPBFdb = reeMercadoDiarioBDManager.TecnologiasPBFWeb.objects(fecha=dia)
        print TecnologiasPBFdb.count()
        for p in TecnologiasPBFdb:
            TecnologiasPBF = p
        
        print precios,TecnologiasCBL,TecnologiasPBF
        

        # Get data for tecnogolias:
        # Get data for energiagestionada:
        # Get or create data in the collection:
        for h in range(24):
            dateandtime = verver
            datainstudy = MercadoDiarioMixEs(dia)
            # En los datos de la REE solamente hay dataos de Hidraulica total.
            # Para el desglose hay que mirar los datos de OMIE:
            datainstudy.HIDRAULICA = {'TOTAL':0.0,'CONVENCIONAL':0.0,'BOMBEO':0.0}
            datainstudy.TERMICA = {'TOTAL':0.0,
                                   'NUCLEAR':0.0,
                                   'CARBON': {'TOTAL':0.0,'NACIONAL':0.0,'IMPORTACION':0.0},
                                   'FUELGAS': {'TOTAL':0.0,'CON_PRIMA':0.0,'SIN_PRIMA':0.0},
                                   'CICLOCOMBINADO':0.0,
                                   }
            datainstudy.REGIMEN_ESPECIAL = {'TOTAL':0.0,
                                            'EOLICA':0.0,
                                            'SOLAR_FOTOVOLTAICO':0.0,
                                            'SOLAR_TERMICO':0.0,
                                            'TERMICA_RENOVABLE':0.0,
                                            'COGENERANCION_OTROS':0.0,
                                            }
            # P_TOTAL_IMPORTACION = FloatField()
            # P_TOTAL_GENERICAS = FloatField()
            # P_TOTAL_PRODUCCION_MIBEL = FloatField()
            datainstudy.IMPORTANCION = {'TOTAL':0.0,}



    
        

    return "populateMercadoDiarioMixEs"

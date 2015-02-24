# -*- coding: utf-8 -*-
import datetime
from collections import OrderedDict


def ReportDay(market=None,day=None):
    """ReportDay
    Volumenes de EURs y MWh
    Tecnologias
    Precios Promedios de las tecnologias
    
    Precios Promedios de las tecnologias
    """
    try:
        import omieMercadoDiarioDBManager
        if day is None:
            day = min(omieMercadoDiarioDBManager.PreciosWeb.lastdateindb,
                        omieMercadoDiarioDBManager.EnergiaGestionadaWeb.lastdateindb)
        day = day.replace(hour = 0, minute = 0,second = 0,microsecond = 0)
        if market is None:
            market = 'MI'
        if market not in ['ES','PT','MI']:
            raise Exception("Variable mercado no es valida")
        precios = omieMercadoDiarioDBManager.PreciosWeb.objects(fecha=day)
        volumenes = omieMercadoDiarioDBManager.EnergiaGestionadaWeb.objects(fecha=day)
    except:
        raise

    if market == 'MI':
        pre = precios[0].PreciosMI
        volmwh = volumenes[0].EnergiaMI['TOTAL_VENTAS']
        voleurs = [float("{0:.2f}".format(p*v)) for p,v in zip(pre,volmwh)]
    elif market == 'ES':
        pre = precios[0].PreciosES
        volmwh = volumenes[0].EnergiaES['TOTAL_VENTAS']
        voleurs = [float("{0:.2f}".format(p*v)) for p,v in zip(pre,volmwh)]
    elif market == 'PT':
        pre = precios[0].PreciosPT
        volmwh = volumenes[0].EnergiaPT['TOTAL_VENTAS']
        voleurs = [float("{0:.2f}".format(p*v)) for p,v in zip(pre,volmwh)]

    result = OrderedDict()
    result['Fecha']=day
    result['Mercado']=market
    result['Precios']=pre
    result['VolumenesMWh']=volmwh
    result['VolumenesEUR']=voleurs
    result['TotalVolumenMWh']=float("{0:.2f}".format(sum(volmwh)))
    result['TotalVolumenEURs']=float("{0:.2f}".format(sum(voleurs)))
    result['PrecioMedio']=float("{0:.2f}".format(sum(voleurs)/sum(volmwh)))
    result['MediaAritmetica']=float("{0:.2f}".format(sum(pre)/len(pre)))

    return result
    

def ReportDayTecnologies(market=None,day=None):
    """ReportDayTecnologies
    Volumenes de EURs y MWh
    Tecnologias
    Precios Promedios de las tecnologias
    
    Precios Promedios de las tecnologias
    """
    def onlyproduction(tecnologias):
        """onlyproduction

        Returns a dictionary with only production values from the tecnology web.
        TOTAL_REGIMEN_ORDINARIO_CON_PRIMA is added since it looks like it is the FUEL GAS.
        """
        keysProduction = [
        'HIDRAULICA_CONVENCIONAL',
        'HIDRAULICA_BOMBEO_PURO',
        'NUCLEAR',
        'CARBON_NACIONAL',
        'CARBON_IMPORTACION',
        'CICLO_COMBINADO',
        'FUEL_+_GAS_REGIMEN_ORDINARIO_(SIN_PRIMA)',
        'FUEL_+_GAS_REGIMEN_ORDINARIO_(CON_PRIMA)',
        'FUEL_+_GAS',
        'REGIMEN_ESPECIAL_A_MERCADO',
        'TOTAL_PRODUCCION_MIBEL',
        'TOTAL_REGIMEN_ORDINARIO_CON_PRIMA',
        ]
        result = {}
        for key,value in tecnologias.iteritems():
            if key in keysProduction:
                result[key] = value
        return result

    # Must Validate Date 
    # since this isn't possible when for the last 3/2 days from now.
    try:
        import omieMercadoDiarioDBManager
        dayindb = min(omieMercadoDiarioDBManager.PreciosWeb.lastdateindb,
                    omieMercadoDiarioDBManager.EnergiaGestionadaWeb.lastdateindb,
                    omieMercadoDiarioDBManager.TecnologiasWeb.lastdateindb)
        if day is None or day > dayindb:
            day = dayindb
        day = day.replace(hour = 0, minute = 0,second = 0,microsecond = 0)
        precios = omieMercadoDiarioDBManager.PreciosWeb.objects(fecha=day)
        volumenes = omieMercadoDiarioDBManager.EnergiaGestionadaWeb.objects(fecha=day)
        tecnologias = omieMercadoDiarioDBManager.TecnologiasWeb.objects(fecha=day)
        if market is None:
            market = 'MI'
        if market not in ['ES','PT','MI']:
            raise Exception("Variable mercado no es valida")
    except:
        raise

    if market == 'MI':
        pre = precios[0].PreciosMI
        volmwh = volumenes[0].EnergiaMI['TOTAL_VENTAS']
        voltec = onlyproduction(tecnologias[0]['ProduccionyDemandaMIBEL'])
    if market == 'ES':
        pre = precios[0].PreciosES
        volmwh = volumenes[0].EnergiaES['TOTAL_VENTAS']
        voltec = onlyproduction(tecnologias[0]['ProduccionyDemandaES'])
    if market == 'PT':
        pre = precios[0].PreciosPT
        volmwh = volumenes[0].EnergiaPT['TOTAL_VENTAS']
        voltec = onlyproduction(tecnologias[0]['ProduccionyDemandaPT'])
    
    voleurs = [float("{0:.2f}".format(p*v)) for p,v in zip(pre,volmwh)]
    volteceurs = dict()
    for key,values in voltec.iteritems():
        volteceurs[key] = [float("{0:.2f}".format(p*v)) for p,v in zip(pre,values)]

    # volteceurs = {}
    
    result = OrderedDict()
    result['Fecha']=day
    result['Mercado']=market
    result['Precios']=pre
    result['VolumenMWh']=volmwh
    result['VolumenEUR']=voleurs
    result['TotalVolumenMWh']=float("{0:.2f}".format(sum(volmwh)))
    result['TotalVolumenEUR']=float("{0:.2f}".format(sum(voleurs)))
    result['MediaAritmetica']=float("{0:.2f}".format(sum(pre)/len(pre)))
    result['PrecioMedio']=float("{0:.2f}".format(sum(voleurs)/sum(volmwh)))
    for k,values in voltec.iteritems():
        result[k] = {'Volumen':values,'TotalVolumen':float("{0:.2f}".format(sum(values))),
                     'VolumenEUR':[float("{0:.2f}".format(p*v)) for p,v in zip(pre,values)]}
        result[k]['TotalVolumenEUR'] = float("{0:.2f}".format(sum(result[k]['VolumenEUR'])))
        if result[k]['TotalVolumen'] == 0:
            result[k]['PrecioMedio'] = 0
        else:
            result[k]['PrecioMedio'] = result[k]['TotalVolumenEUR']/result[k]['TotalVolumen']
    # for k,v in voltec.iteritems():
    #     result['Volumenes'+k] = v
    # for k,v in voltec.iteritems():
    #     result['TotalVolumenes'+k] = float("{0:.2f}".format(sum(v)))
    # for k,v in volteceurs.iteritems():
    #     result['Volumenes'+k+'EUR'] = v
    # for k,v in volteceurs.iteritems():
    #     result['TotalVolumenes'+k+'EUR'] = float("{0:.2f}".format(sum(v)))
    # result['TotalVolumenMWh']=float("{0:.2f}".format(sum(volmwh)))
    # result['TotalVolumenEURs']=float("{0:.2f}".format(sum(voleurs)))
    # result['PrecioMedio']=float("{0:.2f}".format(sum(voleurs)/sum(volmwh)))
    # for k in voltec.keys():
    #     if result['TotalVolumenes'+k] !=0:
    #         result['PrecioMedio'+k] = result['TotalVolumenes'+k+'EUR']/result['TotalVolumenes'+k]
    #     else:
    #         result['PrecioMedio'+k] = 0

    return result

    


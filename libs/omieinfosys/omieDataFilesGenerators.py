# -*- coding: utf-8 -*
"""Omie Data Files Generator:

This module generates data files for users to download and perform studies on
the Market Results.

Data is generated into the data folder.

"""

# needed imports base python:
import os
import sys
import csv
import datetime
try:
    path = os.environ['OPENSHIFT_HOMEDIR']
    # openshift file path!
except:
    path = os.path.join('..','data')
# else:
#     pass
#     # set filepath
# finally:
    #
    

def generateOMIEwebdata(fechaini=None,fechafin=None,market='MI',headerstoprocess=dict(),rewritetemp=False):
    """Generate OMIE 2011
    market
    result
    omie"market"2011

    The collections processed here are: PreciosWeb, EnergiaGestionadaWeb and
    TecnologiasWeb.
    """
    # Validate input data:
    try:
        from omieMercadoDiarioDBManager import PreciosWeb
        from omieMercadoDiarioDBManager import TecnologiasWeb
        from omieMercadoDiarioDBManager import EnergiaGestionadaWeb

        if fechaini is None:
            fechaini = datetime.datetime(2011,1,1)
        if fechafin is None:
            fechafin = min(datetime.datetime.now()
                       ,PreciosWeb.lastdateindb
                       ,EnergiaGestionadaWeb.lastdateindb
                       ,TecnologiasWeb.lastdateindb)
        if not isinstance(fechafin,datetime.datetime):
            raise Exception("fechafin not valid")
        if not isinstance(fechaini,datetime.datetime):
            raise Exception("fechaini not valid")
        if market not in ['ES','MI','PT']:
            raise Exception("marketnotvalid not valid")
            # build the filename as omie_MI_YYYYMMDD_YYYYMMDD.csv
        filename = 'omie'+'_'+str(market)\
                     +'_'+fechaini.strftime('%Y-%m-%d')\
                     +'_'+fechafin.strftime('%Y-%m-%d')\
                     +'.csv'
        filepath = os.path.join(path,filename)
        if os.path.exists(filepath) and not rewritetemp:
            print "file already generated"
            print "set rewritetemp to True to generate a new one"
            raise Exception("File already exists")
        if market == 'ES':
            fieldnames = ['Fecha','Hora','Precio',
                # 'PRODUCCION_ESPAÑA',
                'HIDRAULICA_CONVENCIONAL',
                'HIDRAULICA_BOMBEO_PURO',
                'NUCLEAR',
                'CARBON_NACIONAL',
                'CARBON_IMPORTACION',
                'CICLO_COMBINADO',
                'FUEL_+_GAS_REGIMEN_ORDINARIO_(SIN_PRIMA)',
                'FUEL_+_GAS_REGIMEN_ORDINARIO_(CON_PRIMA)',
                'REGIMEN_ESPECIAL_A_MERCADO',
                'REGIMEN_ESPECIAL_A_DISTRIBUCION',
                'IMPORTACION_CONTRATO_LARGO_PLAZO',
                'IMPORTACION_FRANCIA',
                'IMPORTACION_PORTUGAL',
                'IMPORTACION_MARRUECOS',
                'IMPORTACION_ANDORRA',
                'UNIDADES_GENERICAS',
                'UNIDADES_AJUSTE_DE_DISTRIBUIDORAS_A_PREVISION_DEMANDA',
                #'DEMANDA_ESPAÑA',
                'COMERCIALIZACION_NACIONAL',
                'COMERCIALIZACION_ULTIMO_RECURSO',
                'CONSUMIDOR_DIRECTO',
                'CONSUMO_DE_BOMBEO',
                'EXPORTACION_CONTRATO_A_LARGO_PLAZO',
                'EXPORTACION_A_FRANCIA',
                'EXPORTACION_A_PORTUGAL',
                'EXPORTACION_A_MARRUECOS',
                'EXPORTACION_A_ANDORRA',
                'UNIDADES_GENERICAS',
                'UNIDADES_GENERICAS_SUBASTAS_DISTRIBUCION',
                # 'RESUMEN_DE_PRODUCCION_ESPAÑA',
                'TOTAL_HIDRAULICA_(1+2)',
                'TOTAL_TERMICA_(3+4+5+6+7+8)',
                'TOTAL_REGIMEN_ESPECIAL_(9+10)',
                'TOTAL_IMPORTACION_(11+12+13+14+15)',
                'TOTAL_GENERICAS_(16+17)',
                'TOTAL_PRODUCCION',
                # 'RESUMEN_DE_DEMANDA_ESPAÑA',
                'TOTAL_DEMANDA_NACIONAL_CLIENTES_(21+22+23)',
                'TOTAL_CONSUMO_BOMBEO_(24)',
                'TOTAL_EXPORTACIONES_(25+26+27+28+29)',
                'TOTAL_GENERICAS_(30+31)',
                'TOTAL_DEMANDA',
                # 'OTROS_TOTALES_ESPAÑA',
                'TOTAL_VENTAS_NACIONALES_COMERCIALIZACION_A_MERCADO',
                'TOTAL_VENTAS_INTERNACIONALES_COMERCIALIZACION_A_MERCADO',
                'TOTAL_REGIMEN_ORDINARIO_CON_PRIMA',
                'TOTAL_POTENCIA_INDISPONIBLE',
                ]
        elif market == 'PT':
            fieldnames = ['Fecha','Hora','Precio',
                # 'PRODUCCION_PORTUGAL',
                'HIDRAULICA_CONVENCIONAL',
                'HIDRAULICA_BOMBEO_PURO',
                'NUCLEAR',
                'CARBON_NACIONAL',
                'CARBON_IMPORTACION',
                'CICLO_COMBINADO',
                'FUEL_+_GAS',
                'NO_UTILIZADO',
                'REGIMEN_ESPECIAL_A_MERCADO',
                'NO_UTILIZADO',
                'NO_UTILIZADO',
                'NO_UTILIZADO',
                'IMPORTACION_DE_ESPAÑA',
                'NO_UTILIZADO',
                'NO_UTILIZADO',
                'UNIDADES_GENERICAS',
                #'DEMANDA_PORTUGAL',
                'COMERCIALIZACION_NACIONAL',
                'COMERCIALIZACION_DE_ULTIMO_RECURSO',
                'CONSUMIDOR_DIRECTO',
                'CONSUMO_DE_BOMBEO',
                'NO_UTILIZADO',
                'NO_UTILIZADO',
                'EXPORTACION_A_ESPAÑA',
                'NO_UTILIZADO',
                'NO_UTILIZADO',
                'UNIDADES_GENERICAS',
                # 'RESUMEN_DE_PRODUCCION_PORTUGAL',
                'TOTAL_HIDRAULICA_(201+202)',
                'TOTAL_TERMICA_(203+204+205+206+207)',
                'NO_UTILIZADO',
                'TOTAL_IMPORTACION_(213)',
                'TOTAL_GENERICAS_(216)',
                'TOTAL_PRODUCCION',
                # 'RESUMEN_DE_DEMANDA_PORTUGAL',
                'TOTAL_DEMANDA_PORTUGAL_CLIENTES_(221+222+223)',
                'TOTAL_CONSUMO_BOMBEO_(224)',
                'TOTAL_EXPORTACIONES_(227)',
                'TOTAL_GENERICAS_(230)',
                'TOTAL_DEMANDA',
                #'OTROS_TOTALES_PORTUGAL',
                'TOTAL_VENTAS_NACIONALES_COMERCIALIZACION_A_MERCADO',
                'NO_UTILIZADO',
                'NO_UTILIZADO',
                'TOTAL_POTENCIA_INDISPONIBLE',
                ]
        elif market == 'MI':
            fieldnames = ['Fecha','Hora','Precio',
                #'PRODUCCION_MIBEL',
                'HIDRAULICA_CONVENCIONAL',
                'HIDRAULICA_BOMBEO_PURO',
                'NUCLEAR',
                'CARBON_NACIONAL',
                'CARBON_IMPORTACION',
                'CICLO_COMBINADO',
                'FUEL_+_GAS_REGIMEN_ORDINARIO_(SIN_PRIMA)',
                'FUEL_+_GAS_REGIMEN_ORDINARIO_(CON_PRIMA)',
                'REGIMEN_ESPECIAL_A_MERCADO',
                'REGIMEN_ESPECIAL_A_DISTRIBUCION',
                'IMPORTACION_CONTRATO_LARGO_PLAZO',
                'IMPORTACION_FRANCIA',
                'NO_UTILIZADO',
                'IMPORTACION_MARRUECOS',
                'IMPORTACION_ANDORRA',
                'UNIDADES_GENERICAS',
                'UNIDADES_SUBASTAS_DISTRIBUCION_AJUSTE_A_PREVISION_DEMANDA',
                #'DEMANDA_MIBEL',
                'COMERCIALIZACION_MIBEL',
                'COMERCIALIZACION_ULTIMO_RECURSO',
                'CONSUMIDOR_DIRECTO',
                'CONSUMO_DE_BOMBEO',
                'EXPORTACION_CONTRATO_A_LARGO_PLAZO',
                'EXPORTACION_A_FRANCIA',
                'NO_UTILIZADO',
                'EXPORTACION_A_MARRUECOS',
                'EXPORTACION_A_ANDORRA',
                'UNIDADES_GENERICAS',
                'UNIDADES_GENERICAS_DE_DISTRIBUCION',
                #'RESUMEN_DE_PRODUCCION_MIBEL',
                'TOTAL_HIDRAULICA_(901+902)',
                'TOTAL_TERMICA_(903+904+905+906+907+908)',
                'TOTAL_REGIMEN_ESPECIAL_(909+910)',
                'TOTAL_IMPORTACION_(911+912+914+915)',
                'TOTAL_GENERICAS_(916+917)',
                'TOTAL_PRODUCCION_MIBEL',
                #'RESUMEN_DE_DEMANDA_MIBEL',
                'TOTAL_DEMANDA_NACIONAL_CLIENTES_(921+922+923)',
                'TOTAL_CONSUMO_BOMBEO_(924)',
                'TOTAL_EXPORTACIONES_(925+926+928+929)',
                'TOTAL_GENERICAS_(930+931)',
                'TOTAL_DEMANDA_MIBEL',
                #'OTROS_TOTALES_MIBEL',
                'TOTAL_VENTAS_NACIONALES_COMERCIALIZACION_A_MERCADO',
                'TOTAL_VENTAS_INTERNACIONALES_COMERCIALIZACION_A_MERCADO',
                'TOTAL_REGIMEN_ORDINARIO_CON_PRIMA',
                'TOTAL_POTENCIA_INDISPONIBLE',
                ]

        # now must validate headerstoprocess:

    except:
        raise
        sys.exit()


    # Check if the file exists. if yes return file path.
    # if rewrite==True remove existing file and generate the file again.
    # Get OPENSHIFT_DATA_DIR if it doesn't exists the it is a local run and
    # you can find data at the location ../../data

    numofdays = min(PreciosWeb.objects(fecha__gte=fechaini,fecha__lte=fechafin).count(),
                    TecnologiasWeb.objects(fecha__gte=fechaini,fecha__lte=fechafin).count(),
                    EnergiaGestionadaWeb.objects(fecha__gte=fechaini,fecha__lte=fechafin).count(),
            )

    with open(filepath, 'w') as f:
        # query lastday = 
        days = [fechaini + datetime.timedelta(days=i) for i in range(numofdays)]
        # if you want to handle exceptional day do it here!
        writer = csv.DictWriter(f, fieldnames=fieldnames,delimiter=';')
        writer.writeheader()
        for day in days:
            precios = PreciosWeb.objects.get(fecha=day)
            tecnologias = TecnologiasWeb.objects.get(fecha=day)
            energia = EnergiaGestionadaWeb.objects.get(fecha=day)
            # select market:
            if market=='ES':
                precios = precios['PreciosES']
                energia = energia['EnergiaES']['TOTAL_VENTAS']
                tecnologias = tecnologias['ProduccionyDemandaES']
            elif market=='PT':
                precios = precios['PreciosPT']
                energia = energia['EnergiaPT']['TOTAL_VENTAS']
                tecnologias = tecnologias['ProduccionyDemandaPT']
            else:
                precios = precios['PreciosMI']
                energia = energia['EnergiaMI']['TOTAL_VENTAS']
                tecnologias = tecnologias['ProduccionyDemandaMIBEL']
            for h in range(len(precios)):
                row = dict()
                for key in fieldnames:
                    if key == 'Fecha':
                        row['Fecha'] = day.strftime('%Y-%m-%d')
                    elif key == 'Hora':
                        row['Hora'] = h
                    elif key == 'Precio':
                        row['Precio'] = precios[h]
                    elif key == 'Ventas':
                        row['Ventas'] = energia[h]
                    else:
                        row[key]=tecnologias[key.decode('utf8')][h]
                writer.writerow(row)

            # writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
            # writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})
            
            # f.write('file contents')
            # f.write('other contents')

    return "done"


def generateAllOMIEwebdatafiles():
    """Generates all data file given at ckan repository.

    

    """
    # year 2011 Market MI
    generateOMIEwebdata(fechaini=datetime.datetime(2011,1,1),fechafin=datetime.datetime(2011,12,31),market='MI')
    # year 2011 Market ES
    generateOMIEwebdata(fechaini=datetime.datetime(2011,1,1),fechafin=datetime.datetime(2011,12,31),market='ES')
    # year 2011 Market PT
    generateOMIEwebdata(fechaini=datetime.datetime(2011,1,1),fechafin=datetime.datetime(2011,12,31),market='PT')
    # year 2012 Market MI
    generateOMIEwebdata(fechaini=datetime.datetime(2012,1,1),fechafin=datetime.datetime(2012,12,31),market='MI')
    # year 2012 Market ES
    generateOMIEwebdata(fechaini=datetime.datetime(2012,1,1),fechafin=datetime.datetime(2012,12,31),market='ES')
    # year 2012 Market PT
    generateOMIEwebdata(fechaini=datetime.datetime(2012,1,1),fechafin=datetime.datetime(2012,12,31),market='PT')
    # year 2013 Market MI
    generateOMIEwebdata(fechaini=datetime.datetime(2013,1,1),fechafin=datetime.datetime(2013,12,31),market='MI')
    # year 2013 Market ES
    generateOMIEwebdata(fechaini=datetime.datetime(2013,1,1),fechafin=datetime.datetime(2013,12,31),market='ES')
    # year 2013 Market PT
    generateOMIEwebdata(fechaini=datetime.datetime(2013,1,1),fechafin=datetime.datetime(2013,12,31),market='PT')
    # year 2014 Market MI
    generateOMIEwebdata(fechaini=datetime.datetime(2014,1,1),fechafin=datetime.datetime(2014,12,31),market='MI')
    # year 2014 Market ES
    generateOMIEwebdata(fechaini=datetime.datetime(2014,1,1),fechafin=datetime.datetime(2014,12,31),market='ES')
    # year 2014 Market PT
    generateOMIEwebdata(fechaini=datetime.datetime(2014,1,1),fechafin=datetime.datetime(2014,12,31),market='PT')
    # year 2015 Market MI
    generateOMIEwebdata(fechaini=datetime.datetime(2015,1,1),fechafin=datetime.datetime(2015,12,31),market='MI')
    # year 2015 Market ES
    generateOMIEwebdata(fechaini=datetime.datetime(2015,1,1),fechafin=datetime.datetime(2015,12,31),market='ES')
    # year 2015 Market PT
    generateOMIEwebdata(fechaini=datetime.datetime(2015,1,1),fechafin=datetime.datetime(2015,12,31),market='PT')

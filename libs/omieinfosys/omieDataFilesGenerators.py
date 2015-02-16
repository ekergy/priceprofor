# -*- coding: utf-8 -*
"""Omie Data Files Generator:

This module generates data files for users to download and perform studies on
the Market Results.

Data is generated into the data folder.

"""

# needed imports base python:
import os
import csv
import datetime


def generateOMIEwebdata(year=2011,market='MI',rewrite=False):
    """Generate OMIE 2011
    market
    result
    omie"market"2011

    The collections processed here are:

    """
    # Check if the file exists. if yes return file path.
    # if rewrite==True remove existing file and generate the file again.
    # Get OPENSHIFT_DATA_DIR if it doesn't exists the it is a local run and
    # you can find data at the location ../../data
    filename = 'omie'+str(market)+str(year)+'.csv'
    filepath = os.path.join('..','data',filename)
    print "Fileexists¿?",filepath,os.path.exists(filepath)

    # Lets gather information to write into file:
    try:
        from omieMercadoDiarioDBManager import PreciosWeb
        from omieMercadoDiarioDBManager import TecnologiasWeb
        from omieMercadoDiarioDBManager import EnergiaGestionadaWeb
    except:
        raise
    else:
        # Opening file:
        # first process year:
        fechaINI=datetime.datetime(year,1,1)
        fechaFIN=datetime.datetime(year,12,31)
        value = min(PreciosWeb.objects(fecha__gte=fechaINI,fecha__lte=fechaFIN).count(),
                    TecnologiasWeb.objects(fecha__gte=fechaINI,fecha__lte=fechaFIN).count(),
                    EnergiaGestionadaWeb.objects(fecha__gte=fechaINI,fecha__lte=fechaFIN).count(),
            )
        print value
        with open(filepath, 'w') as f:
            # query lastday = 

            days = [datetime.datetime(year,1,1) + datetime.timedelta(days=i) for i in range(value)]
            for day in days:
                precios = PreciosWeb.objects.get(fecha=day)
                tecnologias = TecnologiasWeb.objects.get(fecha=day)
                energia = EnergiaGestionadaWeb.objects.get(fecha=day)
                # select market:
                if market=='ES':
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
                    'OTROS_TOTALES_ESPAÑA',
                    'TOTAL_VENTAS_NACIONALES_COMERCIALIZACION_A_MERCADO',
                    'TOTAL_VENTAS_INTERNACIONALES_COMERCIALIZACION_A_MERCADO',
                    'TOTAL_REGIMEN_ORDINARIO_CON_PRIMA',
                    'TOTAL_POTENCIA_INDISPONIBLE',
                    ]
                    writer = csv.DictWriter(f, fieldnames=fieldnames,delimiter=';')
                    writer.writeheader()
                    precios = precios['PreciosES']
                    energia = energia['EnergiaES']['TOTAL_VENTAS']
                    tecnologias = tecnologias['ProduccionyDemandaES']
                elif market=='PT':
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
                    writer = csv.DictWriter(f, fieldnames=fieldnames,delimiter=';')
                    writer.writeheader()
                    precios = precios['PreciosPT']
                    energia = energia['EnergiaPT']['TOTAL_VENTAS']
                    tecnologias = tecnologias['ProduccionyDemandaPT']
                else:
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
                    writer = csv.DictWriter(f, fieldnames=fieldnames,delimiter=';')
                    writer.writeheader()
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
                            row[key]=tecnologias[key][h]
                    writer.writerow(row)

            # writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
            # writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})
            
            # f.write('file contents')
            # f.write('other contents')

    

    return "done"






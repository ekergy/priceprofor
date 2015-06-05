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
from collections import OrderedDict
try:
    path = os.environ['OPENSHIFT_HOMEDIR']
    # openshift file path!
except:
    # path = os.path.join('..','..','data')
    path = os.path.join('data')
# else:
#     pass
#     # set filepath
# finally:
    #
    

def generateOMIEwebdata(fechaini=None,fechafin=None,market='MI',headerstoprocess=None,rewritetemp=False,filename=None):
    """Generate OMIE 2011
    market
    result
    omie"market"2011

    The collections processed here are: PreciosWeb, EnergiaGestionadaWeb and
    TecnologiasWeb.
    """
    def generatefieldnames(market,headerstoprocess=None):
        """processheaders
            return a list of the of the filenames:
        """
        OrderedDict([('pear', 1), ('orange', 2), ('banana', 3), ('apple', 4)])
        marketsfieldnames = {
        'MI': OrderedDict([
            ('Fecha',True),
            ('Anho',False),
            ('Mes',False),
            ('Dia',False),
            ('Semana',False),
            ('DiaSemana',False),
            ('Hora',True),
            ('Precio',True),
            ('TOTAL_VENTAS',True),
            #('PRODUCCION_MIBEL',True),
            ('HIDRAULICA_CONVENCIONAL',True),
            ('HIDRAULICA_BOMBEO_PURO',True),
            ('NUCLEAR',True),
            ('CARBON_NACIONAL',True),
            ('CARBON_IMPORTACION',True),
            ('CICLO_COMBINADO',True),
            ('FUEL_+_GAS_REGIMEN_ORDINARIO_(SIN_PRIMA)',True),
            ('FUEL_+_GAS_REGIMEN_ORDINARIO_(CON_PRIMA)',True),
            ('REGIMEN_ESPECIAL_A_MERCADO',True),
            ('REGIMEN_ESPECIAL_A_DISTRIBUCION',True),
            ('IMPORTACION_CONTRATO_LARGO_PLAZO',True),
            ('IMPORTACION_FRANCIA',True),
            ('NO_UTILIZADO',True),
            ('IMPORTACION_MARRUECOS',True),
            ('IMPORTACION_ANDORRA',True),
            ('UNIDADES_GENERICAS',True),
            ('UNIDADES_SUBASTAS_DISTRIBUCION_AJUSTE_A_PREVISION_DEMANDA',True),
            #('DEMANDA_MIBEL',True),
            ('COMERCIALIZACION_MIBEL',True),
            ('COMERCIALIZACION_ULTIMO_RECURSO',True),
            ('CONSUMIDOR_DIRECTO',True),
            ('CONSUMO_DE_BOMBEO',True),
            ('EXPORTACION_CONTRATO_A_LARGO_PLAZO',True),
            ('EXPORTACION_A_FRANCIA',True),
            ('NO_UTILIZADO',True),
            ('EXPORTACION_A_MARRUECOS',True),
            ('EXPORTACION_A_ANDORRA',True),
            ('UNIDADES_GENERICAS',True),
            ('UNIDADES_GENERICAS_DE_DISTRIBUCION',True),
            #('RESUMEN_DE_PRODUCCION_MIBEL',True),
            ('TOTAL_HIDRAULICA_(901+902)',True),
            ('TOTAL_TERMICA_(903+904+905+906+907+908)',True),
            ('TOTAL_REGIMEN_ESPECIAL_(909+910)',True),
            ('TOTAL_IMPORTACION_(911+912+914+915)',True),
            ('TOTAL_GENERICAS_(916+917)',True),
            ('TOTAL_PRODUCCION_MIBEL',True),
            #('RESUMEN_DE_DEMANDA_MIBEL',True),
            ('TOTAL_DEMANDA_NACIONAL_CLIENTES_(921+922+923)',True),
            ('TOTAL_CONSUMO_BOMBEO_(924)',True),
            ('TOTAL_EXPORTACIONES_(925+926+928+929)',True),
            ('TOTAL_GENERICAS_(930+931)',True),
            ('TOTAL_DEMANDA_MIBEL',True),
            #('OTROS_TOTALES_MIBEL',True),
            ('TOTAL_VENTAS_NACIONALES_COMERCIALIZACION_A_MERCADO',True),
            ('TOTAL_VENTAS_INTERNACIONALES_COMERCIALIZACION_A_MERCADO',True),
            ('TOTAL_REGIMEN_ORDINARIO_CON_PRIMA',True),
            ('TOTAL_POTENCIA_INDISPONIBLE',True),
            ]),
        'ES': OrderedDict([
            ('Fecha',True),
            ('Anho',False),
            ('Mes',False),
            ('Dia',False),
            ('Semana',False),
            ('DiaSemana',False),
            ('Hora',True),
            ('Precio',True),
            ('TOTAL_VENTAS',True),
            # ('PRODUCCION_ESPAÑA',True),
            ('HIDRAULICA_CONVENCIONAL',True),
            ('HIDRAULICA_BOMBEO_PURO',True),
            ('NUCLEAR',True),
            ('CARBON_NACIONAL',True),
            ('CARBON_IMPORTACION',True),
            ('CICLO_COMBINADO',True),
            ('FUEL_+_GAS_REGIMEN_ORDINARIO_(SIN_PRIMA)',True),
            ('FUEL_+_GAS_REGIMEN_ORDINARIO_(CON_PRIMA)',True),
            ('REGIMEN_ESPECIAL_A_MERCADO',True),
            ('REGIMEN_ESPECIAL_A_DISTRIBUCION',True),
            ('IMPORTACION_CONTRATO_LARGO_PLAZO',True),
            ('IMPORTACION_FRANCIA',True),
            ('IMPORTACION_PORTUGAL',True),
            ('IMPORTACION_MARRUECOS',True),
            ('IMPORTACION_ANDORRA',True),
            ('UNIDADES_GENERICAS',True),
            ('UNIDADES_AJUSTE_DE_DISTRIBUIDORAS_A_PREVISION_DEMANDA',True),
            # ('DEMANDA_ESPAÑA',True),
            ('COMERCIALIZACION_NACIONAL',True),
            ('COMERCIALIZACION_ULTIMO_RECURSO',True),
            ('CONSUMIDOR_DIRECTO',True),
            ('CONSUMO_DE_BOMBEO',True),
            ('EXPORTACION_CONTRATO_A_LARGO_PLAZO',True),
            ('EXPORTACION_A_FRANCIA',True),
            ('EXPORTACION_A_PORTUGAL',True),
            ('EXPORTACION_A_MARRUECOS',True),
            ('EXPORTACION_A_ANDORRA',True),
            ('UNIDADES_GENERICAS',True),
            ('UNIDADES_GENERICAS_SUBASTAS_DISTRIBUCION',True),
            # ('RESUMEN_DE_PRODUCCION_ESPAÑA',True),
            ('TOTAL_HIDRAULICA_(1+2)',True),
            ('TOTAL_TERMICA_(3+4+5+6+7+8)',True),
            ('TOTAL_REGIMEN_ESPECIAL_(9+10)',True),
            ('TOTAL_IMPORTACION_(11+12+13+14+15)',True),
            ('TOTAL_GENERICAS_(16+17)',True),
            ('TOTAL_PRODUCCION',True),
            # ('RESUMEN_DE_DEMANDA_ESPAÑA',True),
            ('TOTAL_DEMANDA_NACIONAL_CLIENTES_(21+22+23)',True),
            ('TOTAL_CONSUMO_BOMBEO_(24)',True),
            ('TOTAL_EXPORTACIONES_(25+26+27+28+29)',True),
            ('TOTAL_GENERICAS_(30+31)',True),
            ('TOTAL_DEMANDA',True),
            # ('OTROS_TOTALES_ESPAÑA',True),
            ('TOTAL_VENTAS_NACIONALES_COMERCIALIZACION_A_MERCADO',True),
            ('TOTAL_VENTAS_INTERNACIONALES_COMERCIALIZACION_A_MERCADO',True),
            ('TOTAL_REGIMEN_ORDINARIO_CON_PRIMA',True),
            ('TOTAL_POTENCIA_INDISPONIBLE',True),
            ]),
        'PT': OrderedDict([
            ('Fecha',True),
            ('Anho',False),
            ('Mes',False),
            ('Dia',False),
            ('Semana',False),
            ('DiaSemana',False),
            ('Hora',True),
            ('Precio',True),
            ('TOTAL_VENTAS',True),
            # ('PRODUCCION_PORTUGAL',True),
            ('HIDRAULICA_CONVENCIONAL',True),
            ('HIDRAULICA_BOMBEO_PURO',True),
            ('NUCLEAR',True),
            ('CARBON_NACIONAL',True),
            ('CARBON_IMPORTACION',True),
            ('CICLO_COMBINADO',True),
            ('FUEL_+_GAS',True),
            ('NO_UTILIZADO',True),
            ('REGIMEN_ESPECIAL_A_MERCADO',True),
            ('NO_UTILIZADO',True),
            ('NO_UTILIZADO',True),
            ('NO_UTILIZADO',True),
            ('IMPORTACION_DE_ESPAÑA',True),
            ('NO_UTILIZADO',True),
            ('NO_UTILIZADO',True),
            ('UNIDADES_GENERICAS',True),
            # ('DEMANDA_PORTUGAL',True),
            ('COMERCIALIZACION_NACIONAL',True),
            ('COMERCIALIZACION_DE_ULTIMO_RECURSO',True),
            ('CONSUMIDOR_DIRECTO',True),
            ('CONSUMO_DE_BOMBEO',True),
            ('NO_UTILIZADO',True),
            ('NO_UTILIZADO',True),
            ('EXPORTACION_A_ESPAÑA',True),
            ('NO_UTILIZADO',True),
            ('NO_UTILIZADO',True),
            ('UNIDADES_GENERICAS',True),
            # ('RESUMEN_DE_PRODUCCION_PORTUGAL',True),
            ('TOTAL_HIDRAULICA_(201+202)',True),
            ('TOTAL_TERMICA_(203+204+205+206+207)',True),
            ('NO_UTILIZADO',True),
            ('TOTAL_IMPORTACION_(213)',True),
            ('TOTAL_GENERICAS_(216)',True),
            ('TOTAL_PRODUCCION',True),
            # ('RESUMEN_DE_DEMANDA_PORTUGAL',True),
            ('TOTAL_DEMANDA_PORTUGAL_CLIENTES_(221+222+223)',True),
            ('TOTAL_CONSUMO_BOMBEO_(224)',True),
            ('TOTAL_EXPORTACIONES_(227)',True),
            ('TOTAL_GENERICAS_(230)',True),
            ('TOTAL_DEMANDA',True),
            # ('OTROS_TOTALES_PORTUGAL',True),
            ('TOTAL_VENTAS_NACIONALES_COMERCIALIZACION_A_MERCADO',True),
            ('NO_UTILIZADO',True),
            ('NO_UTILIZADO',True),
            ('TOTAL_POTENCIA_INDISPONIBLE',True),
            ])
        }
        if headerstoprocess is not None:
            marketsfieldnames[market].update(headerstoprocess)
        result = list()
        for k,v in marketsfieldnames[market].iteritems():
            if v:
                # NOT CLEAR THAT IS NEEDED decoding here or not.
                # result.append(k.decode('utf8'))
                result.append(k)
        return result


        


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
        # build the filename as omie_MI_YYYYMMDD_YYYYMMDD_NN.csv
        # with NN as number og fields processed!
        fieldnames = generatefieldnames(market,headerstoprocess=headerstoprocess)
        if filename is None:
            filename = 'omie'+'_'+str(market)\
                             +'_'+fechaini.strftime('%Y-%m-%d')\
                             +'_'+fechafin.strftime('%Y-%m-%d')\
                             +'_'+str(len(fieldnames))\
                             +'.csv'
        filepath = os.path.join(path,filename)
        if os.path.exists(filepath) and not rewritetemp:
            print "file already generated"
            print "set rewritetemp to True to generate a new one"
            raise Exception("File already exists")
        

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
        print 'fieldnames'
        print fieldnames
        print 'fieldnames'
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
                    elif key == 'Anho':
                        row['Anho'] = day.year
                    elif key == 'Mes':
                        row['Mes'] = day.month
                    elif key == 'Dia':
                        row['Dia'] = day.day
                    elif key == 'Semana':
                        row['Semana'] = day.isocalendar()[1]
                    elif key == 'DiaSemana':
                        row['DiaSemana'] = day.weekday[1]
                    elif key == 'Hora':
                        row['Hora'] = h
                    elif key == 'Precio':
                        row['Precio'] = precios[h]
                    elif key == 'TOTAL_VENTAS':
                        row['TOTAL_VENTAS'] = energia[h]
                    else:
                        row[key]=tecnologias[key.decode('utf8')][h]
                writer.writerow(row)

            # writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
            # writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})
            
            # f.write('file contents')
            # f.write('other contents')

    return os.path.abspath(filepath)


def generateAllOMIEwebdatafiles():
    """Generates all data file given at ckan repository.

    This is a Helper and easy to use function.

    

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

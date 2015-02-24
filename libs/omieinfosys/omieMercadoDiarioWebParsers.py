# -*- coding: utf-8 -*-

from csv import reader
from utilities import stringtofloat, unicodetodecimal, cambiohoraverano, cambiohorainvierno
from urllib2 import urlopen
from datetime import datetime
from collections import OrderedDict

class PreciosMercadoDiarioHandler(object):
    """
    Class to parse the Spanish and Portguese Electric Market Prices.
    http://www.omie.es/aplicaciones/datosftp/datosftp.jsp?path=/marginalpdbc/
    Introduced the concept of Mibel Price as the market price set before market split operation.
    Note:
        What is used here for the mibel price is not the concept only an aproximation. Because the split can occur in both markets and not only one.
    But it is a good aproximation to assume that the mibel price is the lower price from the Spanish and Portguese Electric Market Prices
    """
    PARSEABLETOMIBEL = {}
    PARSEABLETOES = {}
    PARSEABLETOPT = {}
    def __init__(self,thefile = None):
        try:
            self.toparsePRECIOS = reader(thefile,delimiter=';')
            self.precioses = list()
            self.preciospt = list()
            self.preciosmibel = list()
        except:
            raise
        else:
            for row in self.toparsePRECIOS:
                # condition to be a row with data
                if row.__len__()!=0 and row.__len__()>3 :
                    # Changed to the unicode to decimal function since is better implemented (or I think!)
                    # precioes = stringtofloat(row[5],decimalsep='.',groupsep='')
                    # preciopt = stringtofloat(row[4],decimalsep='.',groupsep='')
                    precioes = unicodetodecimal(row[5])
                    preciopt = unicodetodecimal(row[4])
                    self.precioses.append(precioes)
                    self.preciospt.append(preciopt)
                    self.preciosmibel.append(min(precioes,preciopt))
                    
class EnergiaGestionadaMercadoDiarioHandler(object):
    """Class to parse Spanish, Portuguese and Mibel Electric Market Volumen managed in
    the Daily Market.
    Data is parsed directly from OMIE web and can be found at:
    http://www.omie.es/aplicaciones/datosftp/datosftp.jsp?path=/pdbc_tot/
    The data source contains the information for all three markets.
    """
    def __init__(self,thefile = None):
        try:
            self.toparseENERGIA = reader(thefile,delimiter=';')
            self.energiaes = {'TOTAL_COMPRAS':list(),'TOTAL_VENTAS':list()}
            self.energiapt = {'TOTAL_COMPRAS':list(),'TOTAL_VENTAS':list()}
            self.energiami = {'TOTAL_COMPRAS':list(),'TOTAL_VENTAS':list()}
        except:
            raise
        else:
            for row in self.toparseENERGIA:
                # condition to be a row with data:
                if row.__len__() == 9:
                    # This is the first row. Let get date from it.
                    self.fecha = datetime.strptime(row[3],'%d/%m/%Y')
                if row.__len__()!=0 and row.__len__()>25:
                    if self.fecha == cambiohoraverano(self.fecha.year):
                        len_valores = range(2,25)
                    elif self.fecha == cambiohorainvierno(self.fecha.year):
                        len_valores = range(2,27)
                    else:
                        len_valores = range(2,26)
                    concepto = row[0]
                    mercado = row[1]
                    if concepto == "Total Compras":
                        if mercado == "ES":
                            for i in len_valores:
                                self.energiaes['TOTAL_COMPRAS'].append(stringtofloat(row[i]))
                        elif mercado == "PT":
                            for i in len_valores:
                                self.energiapt['TOTAL_COMPRAS'].append(stringtofloat(row[i]))
                        else:
                            for i in len_valores:
                                self.energiami['TOTAL_COMPRAS'].append(stringtofloat(row[i]))
                    elif concepto == "Total Ventas":
                        if mercado == "ES":
                            for i in len_valores:
                                self.energiaes['TOTAL_VENTAS'].append(stringtofloat(row[i]))
                        elif mercado == "PT":
                            for i in len_valores:
                                self.energiapt['TOTAL_VENTAS'].append(stringtofloat(row[i]))
                        else:
                            for i in len_valores:
                                self.energiami['TOTAL_VENTAS'].append(stringtofloat(row[i]))




                    

                    


class TecnologiasMercadoDiarioHandler(object):
    '''
    Class to parse the Spanish, Portuguese and Mibel Electric Market Tecnologies.
    Data is parsed directly from OMIE web and can be found at:
    http://www.omie.es/aplicaciones/datosftp/datosftp.jsp?path=/pdbc_stota/
    TODO: ProduccionYDemanda deberia tener algo como Produccion por un lado y Demanda por otro.
    '''

    PARSEABLETOMIBEL = OrderedDict({
                        '900':'PRODUCCION_MIBEL',
                        '901':'HIDRAULICA_CONVENCIONAL',
                        '902':'HIDRAULICA_BOMBEO_PURO',
                        '903':'NUCLEAR',
                        '904':'CARBON_NACIONAL',
                        '905':'CARBON_IMPORTACION',
                        '906':'CICLO_COMBINADO',
                        '907':'FUEL_+_GAS_REGIMEN_ORDINARIO_(SIN_PRIMA)',
                        '908':'FUEL_+_GAS_REGIMEN_ORDINARIO_(CON_PRIMA)',
                        '909':'REGIMEN_ESPECIAL_A_MERCADO',
                        '910':'REGIMEN_ESPECIAL_A_DISTRIBUCION',
                        '911':'IMPORTACION_CONTRATO_LARGO_PLAZO',
                        '912':'IMPORTACION_FRANCIA',
                        '913':'NO_UTILIZADO',
                        '914':'IMPORTACION_MARRUECOS',
                        '915':'IMPORTACION_ANDORRA',
                        '916':'UNIDADES_GENERICAS',
                        '917':'UNIDADES_SUBASTAS_DISTRIBUCION_AJUSTE_A_PREVISION_DEMANDA',
                        '920':'DEMANDA_MIBEL',
                        '921':'COMERCIALIZACION_MIBEL',
                        '922':'COMERCIALIZACION_ULTIMO_RECURSO',
                        '923':'CONSUMIDOR_DIRECTO',
                        '924':'CONSUMO_DE_BOMBEO',
                        '925':'EXPORTACION_CONTRATO_A_LARGO_PLAZO',
                        '926':'EXPORTACION_A_FRANCIA',
                        '927':'NO_UTILIZADO',
                        '928':'EXPORTACION_A_MARRUECOS',
                        '929':'EXPORTACION_A_ANDORRA',
                        '930':'UNIDADES_GENERICAS',
                        '931':'UNIDADES_GENERICAS_DE_DISTRIBUCION',
                        '940':'RESUMEN_DE_PRODUCCION_MIBEL',
                        '941':'TOTAL_HIDRAULICA_(901+902)',
                        '942':'TOTAL_TERMICA_(903+904+905+906+907+908)',
                        '943':'TOTAL_REGIMEN_ESPECIAL_(909+910)',
                        '944':'TOTAL_IMPORTACION_(911+912+914+915)',
                        '945':'TOTAL_GENERICAS_(916+917)',
                        '949':'TOTAL_PRODUCCION_MIBEL',
                        '950':'RESUMEN_DE_DEMANDA_MIBEL',
                        '951':'TOTAL_DEMANDA_NACIONAL_CLIENTES_(921+922+923)',
                        '952':'TOTAL_CONSUMO_BOMBEO_(924)',
                        '953':'TOTAL_EXPORTACIONES_(925+926+928+929)',
                        '954':'TOTAL_GENERICAS_(930+931)',
                        '959':'TOTAL_DEMANDA_MIBEL',
                        '960':'OTROS_TOTALES_MIBEL',
                        '961':'TOTAL_VENTAS_NACIONALES_COMERCIALIZACION_A_MERCADO',
                        '962':'TOTAL_VENTAS_INTERNACIONALES_COMERCIALIZACION_A_MERCADO',
                        '963':'TOTAL_REGIMEN_ORDINARIO_CON_PRIMA',
                        '964':'TOTAL_POTENCIA_INDISPONIBLE',
                       })
    PARSEABLETOES = OrderedDict({
                    '0':'PRODUCCION_ESPAÑA',
                    '1':'HIDRAULICA_CONVENCIONAL',
                    '2':'HIDRAULICA_BOMBEO_PURO',
                    '3':'NUCLEAR',
                    '4':'CARBON_NACIONAL',
                    '5':'CARBON_IMPORTACION',
                    '6':'CICLO_COMBINADO',
                    '7':'FUEL_+_GAS_REGIMEN_ORDINARIO_(SIN_PRIMA)',
                    '8':'FUEL_+_GAS_REGIMEN_ORDINARIO_(CON_PRIMA)',
                    '9':'REGIMEN_ESPECIAL_A_MERCADO',
                    '10':'REGIMEN_ESPECIAL_A_DISTRIBUCION',
                    '11':'IMPORTACION_CONTRATO_LARGO_PLAZO',
                    '12':'IMPORTACION_FRANCIA',
                    '13':'IMPORTACION_PORTUGAL',
                    '14':'IMPORTACION_MARRUECOS',
                    '15':'IMPORTACION_ANDORRA',
                    '16':'UNIDADES_GENERICAS',
                    '17':'UNIDADES_AJUSTE_DE_DISTRIBUIDORAS_A_PREVISION_DEMANDA',
                    '20':'DEMANDA_ESPAÑA',
                    '21':'COMERCIALIZACION_NACIONAL',
                    '22':'COMERCIALIZACION_ULTIMO_RECURSO',
                    '23':'CONSUMIDOR_DIRECTO',
                    '24':'CONSUMO_DE_BOMBEO',
                    '25':'EXPORTACION_CONTRATO_A_LARGO_PLAZO',
                    '26':'EXPORTACION_A_FRANCIA',
                    '27':'EXPORTACION_A_PORTUGAL',
                    '28':'EXPORTACION_A_MARRUECOS',
                    '29':'EXPORTACION_A_ANDORRA',
                    '30':'UNIDADES_GENERICAS',
                    '31':'UNIDADES_GENERICAS_SUBASTAS_DISTRIBUCION',
                    '40':'RESUMEN_DE_PRODUCCION_ESPAÑA',
                    '41':'TOTAL_HIDRAULICA_(1+2)',
                    '42':'TOTAL_TERMICA_(3+4+5+6+7+8)',
                    '43':'TOTAL_REGIMEN_ESPECIAL_(9+10)',
                    '44':'TOTAL_IMPORTACION_(11+12+13+14+15)',
                    '45':'TOTAL_GENERICAS_(16+17)',
                    '49':'TOTAL_PRODUCCION',
                    '50':'RESUMEN_DE_DEMANDA_ESPAÑA',
                    '51':'TOTAL_DEMANDA_NACIONAL_CLIENTES_(21+22+23)',
                    '52':'TOTAL_CONSUMO_BOMBEO_(24)',
                    '53':'TOTAL_EXPORTACIONES_(25+26+27+28+29)',
                    '54':'TOTAL_GENERICAS_(30+31)',
                    '59':'TOTAL_DEMANDA',
                    '60':'OTROS_TOTALES_ESPAÑA',
                    '61':'TOTAL_VENTAS_NACIONALES_COMERCIALIZACION_A_MERCADO',
                    '62':'TOTAL_VENTAS_INTERNACIONALES_COMERCIALIZACION_A_MERCADO',
                    '63':'TOTAL_REGIMEN_ORDINARIO_CON_PRIMA',
                    '64':'TOTAL_POTENCIA_INDISPONIBLE',
    
                    })

    PARSEABLETOPT = OrderedDict({
                    '200':'PRODUCCION_PORTUGAL',
                    '201':'HIDRAULICA_CONVENCIONAL',
                    '202':'HIDRAULICA_BOMBEO_PURO',
                    '203':'NUCLEAR',
                    '204':'CARBON_NACIONAL',
                    '205':'CARBON_IMPORTACION',
                    '206':'CICLO_COMBINADO',
                    '207':'FUEL_+_GAS',
                    '208':'NO_UTILIZADO',
                    '209':'REGIMEN_ESPECIAL_A_MERCADO',
                    '210':'NO_UTILIZADO',
                    '211':'NO_UTILIZADO',
                    '212':'NO_UTILIZADO',
                    '213':'IMPORTACION_DE_ESPAÑA',
                    '214':'NO_UTILIZADO',
                    '215':'NO_UTILIZADO',
                    '216':'UNIDADES_GENERICAS',
                    '220':'DEMANDA_PORTUGAL',
                    '221':'COMERCIALIZACION_NACIONAL',
                    '222':'COMERCIALIZACION_DE_ULTIMO_RECURSO',
                    '223':'CONSUMIDOR_DIRECTO',
                    '224':'CONSUMO_DE_BOMBEO',
                    '225':'NO_UTILIZADO',
                    '226':'NO_UTILIZADO',
                    '227':'EXPORTACION_A_ESPAÑA',
                    '228':'NO_UTILIZADO',
                    '229':'NO_UTILIZADO',
                    '230':'UNIDADES_GENERICAS',
                    '240':'RESUMEN_DE_PRODUCCION_PORTUGAL',
                    '241':'TOTAL_HIDRAULICA_(201+202)',
                    '242':'TOTAL_TERMICA_(203+204+205+206+207)',
                    '243':'NO_UTILIZADO',
                    '244':'TOTAL_IMPORTACION_(213)',
                    '245':'TOTAL_GENERICAS_(216)',
                    '249':'TOTAL_PRODUCCION',
                    '250':'RESUMEN_DE_DEMANDA_PORTUGAL',
                    '251':'TOTAL_DEMANDA_PORTUGAL_CLIENTES_(221+222+223)',
                    '252':'TOTAL_CONSUMO_BOMBEO_(224)',
                    '253':'TOTAL_EXPORTACIONES_(227)',
                    '254':'TOTAL_GENERICAS_(230)',
                    '259':'TOTAL_DEMANDA',
                    '260':'OTROS_TOTALES_PORTUGAL',
                    '261':'TOTAL_VENTAS_NACIONALES_COMERCIALIZACION_A_MERCADO',
                    '262':'NO_UTILIZADO',
                    '263':'NO_UTILIZADO',
                    '264':'TOTAL_POTENCIA_INDISPONIBLE',
                    })

    def __init__(self,thefile = None):
        self.toparseTECNOLOGIAS = reader(thefile,delimiter=';')
        self.ProduccionyDemandaMIBEL = dict()
        self.ProduccionyDemandaES = dict()
        self.ProduccionyDemandaPT = dict()
        # get date from thefile instead of passing it:
        for row in self.toparseTECNOLOGIAS:
            if row.__len__() == 9:
                # This is the first row. Let get date from it.
                self.fecha = datetime.strptime(row[3],'%d/%m/%Y')
                #self.fecha = datetime(self.fecha.year,self.fecha.month,self.fecha.day)
            if row.__len__()!=0 and row.__len__()>26:
                tomibel = self.PARSEABLETOMIBEL.get(row[0],False)
                toes = self.PARSEABLETOES.get(row[0],False)
                topt = self.PARSEABLETOPT.get(row[0],False)
                if tomibel:
                    # Add demanda and producion casuistic
                    if self.fecha == cambiohoraverano(self.fecha.year):
                        self.ProduccionyDemandaMIBEL[tomibel] = [stringtofloat(row[i]) for i in range(3,26)]
                    elif self.fecha == cambiohorainvierno(self.fecha.year):
                        self.ProduccionyDemandaMIBEL[tomibel] = [stringtofloat(row[i]) for i in range(3,28)]
                    else:
                        self.ProduccionyDemandaMIBEL[tomibel] = [stringtofloat(row[i]) for i in range(3,27)]
                if toes:
                    # Add demanda and producion casuistic
                    if self.fecha == cambiohoraverano(self.fecha.year):
                        self.ProduccionyDemandaES[toes] = [stringtofloat(row[i]) for i in range(3,26)]
                    elif self.fecha == cambiohorainvierno(self.fecha.year):
                        self.ProduccionyDemandaES[toes] = [stringtofloat(row[i]) for i in range(3,28)]
                    else:
                        self.ProduccionyDemandaES[toes] = [stringtofloat(row[i]) for i in range(3,27)]
                if topt:
                    # Add demanda and producion casuistic
                    if self.fecha == cambiohoraverano(self.fecha.year):
                        self.ProduccionyDemandaPT[topt] = [stringtofloat(row[i]) for i in range(3,26)]
                    elif self.fecha == cambiohorainvierno(self.fecha.year):
                        self.ProduccionyDemandaPT[topt] = [stringtofloat(row[i]) for i in range(3,28)]
                    else:
                        self.ProduccionyDemandaPT[topt] = [stringtofloat(row[i]) for i in range(3,27)]
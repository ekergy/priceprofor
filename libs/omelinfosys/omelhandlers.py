# -*- coding: utf-8 -*-
'''
Created on 27/02/2013
@author: hmarrao
'''
from csv import reader
from utilities import stringtofloat, cambiohoraverano, cambiohorainvierno, validafecha, omiepreciosurl, omieproduccionurl
from urllib2 import urlopen
from datetime import datetime

# # from sys import path
# # path.append('libs/')
# # from omelinfosys.omelhandlers import getpreciosmibelfromweb
# # from datetime import datetime
# # fecha = datetime(2014,5,19)
# # getpreciosmibelfromweb(fecha)['PreciosES']
# def getpreciosmibelfromweb(fecha):
#         '''
#         This is the main method so the usage of PreciosMibelHandler is more strainfoward.
#         '''
#         try:
#             validafecha(fecha)
#             # The marginalpdbc data have the Spanish and the Portuguese prices.
#             toparsePRECIOS = urlopen(omiepreciosurl(fecha))
#         except:
#             raise
#         else:
#             Precios = PreciosMibelHandler(toparsePRECIOS)
#             return {"PreciosMibel":Precios.preciospt,"PreciosES":Precios.precioses,"PreciosPT":Precios.preciosmibel}
#         #finally:
#         #    del toparsePRECIOS,Precios

# from sys import path
# path.append('libs/')
# from omelinfosys.omelhandlers import getpreciosmibelfromweb
# from datetime import datetime
# fecha = datetime(2014,5,19)
# getpreciosmibelfromweb(fecha)['PreciosES']
def getpreciosmibelfromweb(fecha,numero=None):
        '''
        This is the main method so the usage of PreciosMibelHandler is more strainfoward.
        '''
        try:
#             currentDate = datetime.datetime(datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day)
#             if fecha == currentDate + datetime.timedelta(1):
#                 validafecha(fecha - datetime.timedelta(1))
#             else:
#                 validafecha(fecha)
            URL = omiepreciosurl(fecha)
            # print URL
            toparsePRECIOS = urlopen(URL)
        except:
            raise
#             req = Request(omiepreciosurl(fecha))
#             urlopen(req)
#         except URLError, e:
#             print e.reason
        else:
            Precios = PreciosMibelHandler(toparsePRECIOS)
            # print Precios.precioses
            if Precios.precioses == []:
#                 print ''
#                 print 'ERROR'
#                 print 'la fecha',fecha.date(),'no tiene precios horarios'
#                 print ''
                numero = '2'
                print fecha.date()
                URL = omiepreciosurl(fecha)[:len(omiepreciosurl(fecha))-1]+str(numero)
                print URL
                toparsePRECIOS = urlopen(URL)
                Precios = PreciosMibelHandler(toparsePRECIOS)
                print Precios.precioses
                return {"PreciosMibel":Precios.preciospt,"PreciosES":Precios.precioses,"PreciosPT":Precios.preciosmibel}
#                 return {"PreciosES": Precios.precioses}
            else:
                return {"PreciosMibel":Precios.preciospt,"PreciosES":Precios.precioses,"PreciosPT":Precios.preciosmibel}
#                 return {"PreciosES": Precios.precioses}
        #finally:
        #    del toparsePRECIOS,Precios

class PreciosMibelHandler(object):
    '''
    Class to parse the Spanish and Portguese Electric Market Prices.
    Introduced the concept of Mibel Price as the market price set before market split operation.
    What is used here is not the concept only an aproximation. Because the split can occur in both markets and not only one.
    But it is a good aproximation to assume that the mibel price is the lower price from the Spanish and Portguese Electric Market Prices
    '''
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
                if row.__len__()!=0 and row.__len__()>3 :
                    precioes = stringtofloat(row[5],decimalsep='.',groupsep='')
                    preciopt = stringtofloat(row[4],decimalsep='.',groupsep='')
                    self.precioses.append(precioes)
                    self.preciospt.append(preciopt)
                    self.preciosmibel.append(min(precioes,preciopt))

def getproduccionmibelfromweb(fecha):
        '''
        This is the main method so the usage of PreciosMibelHandler is more strainfoward.
        '''
        try:
            validafecha(fecha)
            # The marginalpdbc data have the Spanish and the Portuguese prices.
            toparsePRODUCCION = urlopen(omieproduccionurl(fecha))
        except:
            raise
        else:
            Produccion = ProduccionMibelHandler(toparsePRODUCCION)
            return {"ProduccionyDemandaMIBEL":Produccion.ProduccionyDemandaMIBEL,"ProduccionyDemandaES":Produccion.ProduccionyDemandaES,"ProduccionyDemandaPT":Produccion.ProduccionyDemandaPT}
        #finally:
        #    del toparsePRECIOS,Precios

class ProduccionMibelHandler(object):
    '''
    Class to parse the Spanish, Portguese and Mibel Electric Market Prices.
    TODO: esta funcion talvez este mejor fuera de la clase y asi la podemos usar con otros metodos y classes
    como esta echo con las Previsiones.
    TODO: ProduccionYDemanda se deberian de separan en Produccion por un lado y Demanda por otro lado
    class ProduccionYDemandaHandler
    '''
    # def getproducionanddemandafromweb(fecha):
    PARSEABLETOMIBEL = {
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
                        '914':'IMPORTACION_MARRUECOS',
                        '915':'IMPORTACION_ANDORRA',
                        '916':'UNIDADES_GENERICAS_PRODUCCION',
                        '917':'UNIDADES_SUBASTAS_DISTRIBUCION_AJUSTE_A_PREVISION_DEMANDA',
                        '921':'COMERCIALIZACION_MIBEL',
                        '922':'COMERCIALIZACION_ULTIMO_RECURSO',
                        '923':'CONSUMIDOR_DIRECTO',
                        '924':'CONSUMO_DE_BOMBEO',
                        '925':'EXPORTACION_CONTRATO_A_LARGO_PLAZO',
                        '926':'EXPORTACION_A_FRANCIA',
                        '928':'EXPORTACION_A_MARRUECOS',
                        '929':'EXPORTACION_A_ANDORRA',
                        '930':'UNIDADES_GENERICAS_DEMANDA',
                        '931':'UNIDADES_GENERICAS_DE_DISTRIBUCION',
                        '941':'TOTAL_HIDRAULICA_(901+902)',
                        '942':'TOTAL_TERMICA_(903+904+905+906+907+908)',
                        '943':'TOTAL_REGIMEN_ESPECIAL_(909+910)',
                        '944':'TOTAL_IMPORTACION_(911+912+914+915)',
                        '945':'TOTAL_GENERICAS_(916+917)',
                        '949':'TOTAL_PRODUCCION_MIBEL',
                        '951':'TOTAL_DEMANDA_NACIONAL_CLIENTES_(921+922+923)',
                        '952':'TOTAL_CONSUMO_BOMBEO_(924)',
                        '953':'TOTAL_EXPORTACIONES_(925+926+928+929)',
                        '954':'TOTAL_GENERICAS_(930+931)',
                        '959':'TOTAL_DEMANDA_MIBEL',
                        '961':'TOTAL_VENTAS_NACIONALES_COMERCIALIZACION_A_MERCADO',
                        '962':'TOTAL_VENTAS_INTERNACIONALES_COMERCIALIZACION_A_MERCADO',
                        '963':'TOTAL_REGIMEN_ORDINARIO_CON_PRIMA',
                        '964':'TOTAL_POTENCIA_INDISPONIBLE',
                       }
    PARSEABLETOES = {
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
                    '16':'UNIDADES_GENERICAS_PRODUCCION',
                    '17':'UNIDADES_AJUSTE_DE_DISTRIBUIDORAS_A_PREVISION_DEMANDA',
                    '21':'COMERCIALIZACION_NACIONAL',
                    '22':'COMERCIALIZACION_ULTIMO_RECURSO',
                    '23':'CONSUMIDOR_DIRECTO',
                    '24':'CONSUMO_DE_BOMBEO',
                    '25':'EXPORTACION_CONTRATO_A_LARGO_PLAZO',
                    '26':'EXPORTACION_A_FRANCIA',
                    '27':'EXPORTACION_A_PORTUGAL',
                    '28':'EXPORTACION_A_MARRUECOS',
                    '29':'EXPORTACION_A_ANDORRA',
                    '30':'UNIDADES_GENERICAS_DEMANDA',
                    '31':'UNIDADES_GENERICAS_SUBASTAS_DISTRIBUCION',
                    '41':'TOTAL_HIDRAULICA_(1+2)',
                    '42':'TOTAL_TERMICA_(3+4+5+6+7+8)',
                    '43':'TOTAL_REGIMEN_ESPECIAL_(9+10)',
                    '44':'TOTAL_IMPORTACION_(11+12+13+14+15)',
                    '45':'TOTAL_GENERICAS_(16+17)',
                    '49':'TOTAL_PRODUCCION',
                    '51':'TOTAL_DEMANDA_NACIONAL_CLIENTES_(21+22+23)',
                    '52':'TOTAL_CONSUMO_BOMBEO_(24)',
                    '53':'TOTAL_EXPORTACIONES_(25+26+27+28+29)',
                    '54':'TOTAL_GENERICAS_(30+31)',
                    '59':'TOTAL_DEMANDA',
                    '61':'TOTAL_VENTAS_NACIONALES_COMERCIALIZACION_A_MERCADO',
                    '62':'TOTAL_VENTAS_INTERNACIONALES_COMERCIALIZACION_A_MERCADO',
                    '63':'TOTAL_REGIMEN_ORDINARIO_CON_PRIMA',
                    '64':'TOTAL_POTENCIA_INDISPONIBLE',
                    }

    PARSEABLETOPT = {
                    '201':'HIDRAULICA_CONVENCIONAL',
                    '202':'HIDRAULICA_BOMBEO_PURO',
                    '203':'NUCLEAR',
                    '204':'CARBON_NACIONAL',
                    '205':'CARBON_IMPORTACION',
                    '206':'CICLO_COMBINADO',
                    '207':'FUEL_+_GAS',
                    '209':'REGIMEN_ESPECIAL_A_MERCADO',
                    '213':'IMPORTACION_DE_ESPAÑA',
                    '216':'UNIDADES_GENERICAS_PRODUCCION',
                    '221':'COMERCIALIZACION_NACIONAL',
                    '222':'COMERCIALIZACION_DE_ULTIMO_RECURSO',
                    '223':'CONSUMIDOR_DIRECTO',
                    '224':'CONSUMO_DE_BOMBEO',
                    '227':'EXPORTACION_A_ESPAÑA',
                    '230':'UNIDADES_GENERICAS_DEMANDA',
                    '241':'TOTAL_HIDRAULICA_(201+202)',
                    '242':'TOTAL_TERMICA_(203+204+205+206+207)',
                    '244':'TOTAL_IMPORTACION_(213)',
                    '245':'TOTAL_GENERICAS_(216)',
                    '249':'TOTAL_PRODUCCION',
                    '251':'TOTAL_DEMANDA_PORTUGAL_CLIENTES_(221+222+223)',
                    '252':'TOTAL_CONSUMO_BOMBEO_(224)',
                    '253':'TOTAL_EXPORTACIONES_(227)',
                    '254':'TOTAL_GENERICAS_(230)',
                    '259':'TOTAL_DEMANDA',
                    '261':'TOTAL_VENTAS_NACIONALES_COMERCIALIZACION_A_MERCADO',
                    '264':'TOTAL_POTENCIA_INDISPONIBLE',
                    }

    def __init__(self,thefile = None):
        self.toparseTECNOLOGIAS = reader(thefile,delimiter=';')
        self.ProduccionyDemandaMIBEL = dict()
        self.ProduccionyDemandaES = dict()
        self.ProduccionyDemandaPT = dict()
        # get date from thefile instead of passing it:
        # print self.toparseTECNOLOGIAS
        for row in self.toparseTECNOLOGIAS:
            if row.__len__() == 9:
                # This is the first row. Let get date from it.
                self.fecha = datetime.strptime(row[3],'%d/%m/%Y')
                self.fecha = datetime(self.fecha.year,self.fecha.month,self.fecha.day)
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

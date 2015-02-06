# -*- coding: utf-8 -*-
#
# ESTA CLASE SOLO FUNCIONA PARA EL NUEVO FORMATO DEL XML. para el año de 2014
#

from xml.sax import handler, make_parser
from utilities import unicodetodecimal

class ContratacionBilateralHandler(handler.ContentHandler):
    '''
    valid for year 2014>+
    classdocs
    Handler for XML file:
    Definición
    Es el programa de energía diario, con desglose horario, de las diferentes unidades de programación 
    correspondientes a ventas y adquisiciones de energía en el sistema eléctrico peninsular español 
    (mercado diario + contratación bilateral con entrega física).
    Direct Download for file:
    XML identifier:
    BAL_PBF_DD = PBF program energy generation in Contractación Bilateral in MWh.
    Unidades = MWh
    fuente: http://www.esios.ree.es/web-publica/
    ubicación en la web: Programas y Demanda -> Programas -> PBF
    '''
    # Tags del XML
    TAG_SERIESTEMPORALES = "SeriesTemporales"
    TAG_VALUE = "value"
    TAG_NUMBER = "number"
    TAG_TYPE = "type"
    TAG_CTD = "Ctd"
    TAG_ESPANA = "España"
    TAG_PERIODO = "Periodo"
    TAG_INTERVALO = "Intervalo"
    TAG_CONCEPTO = "Concepto"
    # Valores Posibles del atributo value del tag Concepto estan en el dict del init!

    def __init__(self):
        '''
        Constructor
        '''
        # TODO: add a check on date for this parser.
        handler.ContentHandler.__init__(self)
        self.parsingresults = \
        {'HIDRAULICA': {'TAGS':[u'Hidráulica (UGH + Turb. Bomb.)',u'Hydro (UGH + Pump. Gen.)'],'inConceptoAs':False,'valores':[],},
        'HIDRAULICA_OTROS': {'TAGS':[u'Resto hidráulica',u'Rest hydro'],'inConceptoAs':False,'valores':[],},
        'EOLICA': {'TAGS':[u'Eólica',u'Wind'],'inConceptoAs':False,'valores':[],},
        'SOLAR_FOTOVOLTAICO': {'TAGS':[u'Solar fotovoltaico',u'Solar PV'],'inConceptoAs':False,'valores':[],},
        'SOLAR_TERMICO': {'TAGS':[u'Solar térmico',u'Solar thermal'],'inConceptoAs':False,'valores':[],},
        'TERMICA_RENOVABLE': {'TAGS':[u'Térmica renovable',u'Therm renewable'],'inConceptoAs':False,'valores':[],},
        # Tags correspondientes a generación termica no renovable:
        'CARBON': {'TAGS':[u'Coal', u'Carbón'],'inConceptoAs':False,'valores':[],},
        'NUCLEAR': {'TAGS':[u'Nuclear'],'inConceptoAs':False,'valores':[],},
        'FUEL_GAS': {'TAGS':[u'Fuel + Gas',u'Fuel + Gas'],'inConceptoAs':False,'valores':[],},
        'CICLO_COMBINADO': {'TAGS':[u'Combined cycle GT', u'Ciclo Combinado'],'inConceptoAs':False,'valores':[],},
        'COGENERACION_Y_RESTO': {'TAGS':[u'Cogeneración y resto',u'Cogeneration and rest'],'inConceptoAs':False,'valores':[],},
        # Tags correspondientes a importacion:
        'CONSUMO_DE_BOMBEO': {'TAGS':[u'Consumo Bombeo'],'inConceptoAs':False,'valores':[],},
        #
        'IMPORTACION_PORTUGAL': {'TAGS':["Prog. Imp. Portugal"],'inConceptoAs':False,'valores':[],},
        'IMPORTACION_FRANCIA': {'TAGS':["Prog. Imp. Francia"],'inConceptoAs':False,'valores':[],},
        'IMPORTACION_ANDORRA': {'TAGS':["Prog. Imp. Andorra"],'inConceptoAs':False,'valores':[],},
        'IMPORTACION_MARRUECOS': {'TAGS':["Prog. Imp. Marruecos"],'inConceptoAs':False,'valores':[],},
        # Tags correspondientes a exportacion:
        'EXPORTACION_A_PORTUGAL': {'TAGS':["Prog. Exp. Portugal"],'inConceptoAs':False,'valores':[],},
        'EXPORTACION_A_FRANCIA': {'TAGS':["Prog. Exp. Francia"],'inConceptoAs':False,'valores':[],},
        'EXPORTACION_A_ANDORRA': {'TAGS':["Prog. Exp. Andorra"],'inConceptoAs':False,'valores':[],},
        'EXPORTACION_A_MARRUECOS': {'TAGS':["Prog. Exp. Marruecos"],'inConceptoAs':False,'valores':[],},
        }
        # Navigation tags while walking in the XML.
        self.__inSeriesTemporales = False
        self.__inPeriodo = False
        self.__inIntervalo = False
        
    def startElement(self, tag, attrib):
        if tag == self.TAG_SERIESTEMPORALES:
            self.__inSeriesTemporales = True
        if tag == self.TAG_CONCEPTO and self.__inSeriesTemporales == True:
            concepto = attrib.get("value")
            # Process Generacion:
            for key,value in self.parsingresults.iteritems():
                if concepto in value['TAGS']:
                    value['inConceptoAs'] = True
            
        if tag == self.TAG_PERIODO and self.__inSeriesTemporales:
            self.__inPeriodo = True
        if tag == self.TAG_INTERVALO and self.__inPeriodo and self.__inSeriesTemporales:
            self.__inIntervalo = True
        # Now this defines where are we so:
        if tag == "Ctd" and attrib.get("type") == "number" and  self.__inIntervalo and self.__inPeriodo and self.__inSeriesTemporales:
            for key,value in self.parsingresults.iteritems():
                if value['inConceptoAs']:
                    cantidad = attrib.get("value")
                    if str(cantidad) == "-":
                        cantidad = 0
                    else:
                        cantidad = unicodetodecimal(cantidad)
                    value['valores'].append(cantidad)

    def endElement(self, tag):
        '''
        '''
        if tag == self.TAG_SERIESTEMPORALES:
            self.__inSeriesTemporales = False
            for key,value in self.parsingresults.iteritems():
                value['inConceptoAs'] = False

        if tag == self.TAG_PERIODO:
            self.__inPeriodo = False
        if tag == self.TAG_INTERVALO:
            self.__inIntervalo = False

class ContratacionBilateralOLDERHandler(handler.ContentHandler):
    '''
    valid for year 2014>+
    classdocs
    Handler for XML file:
    Definición
    Es el programa de energía diario, con desglose horario, de las diferentes unidades de programación 
    correspondientes a ventas y adquisiciones de energía en el sistema eléctrico peninsular español 
    (mercado diario + contratación bilateral con entrega física).
    Direct Download for file:
    XML identifier:
    BAL_PBF_DD = PBF program energy generation in Contractación Bilateral in MWh.
    Unidades = MWh
    fuente: http://www.esios.ree.es/web-publica/
    ubicación en la web: Programas y Demanda -> Programas -> PBF
    '''
    # Tags del XML
    TAG_SERIESTEMPORALES = "SeriesTemporales"
    TAG_VALUE = "value"
    TAG_NUMBER = "number"
    TAG_TYPE = "type"
    TAG_CTD = "Ctd"
    TAG_ESPANA = "España"
    TAG_PERIODO = "Periodo"
    TAG_INTERVALO = "Intervalo"
    TAG_CONCEPTO = "Concepto"
    # Valores Posibles del atributo value del tag Concepto estan en el dict del init!

    def __init__(self):
        '''
        Constructor
        '''
        # TODO: add a check on date for this parser.
        handler.ContentHandler.__init__(self)
        self.parsingresults = \
        {'HIDRAULICA': {'TAGS':[u'Hidráulica Convencional'],'inConceptoAs':False,'valores':[],},
        'HIDRAULICA_OTROS': {'TAGS':[u'Rég. Esp. Hidráulico'],'inConceptoAs':False,'valores':[],},
        'HIDRAULICA_BOMBEO': {'TAGS':[u'Turbinación bombeo'],'inConceptoAs':False,'valores':[],},
        'EOLICA': {'TAGS':[u'Rég. Esp. Eólico'],'inConceptoAs':False,'valores':[],},
        'SOLAR_FOTOVOLTAICO': {'TAGS':[u'Rég. Esp. Solar Fotovoltaico'],'inConceptoAs':False,'valores':[],},
        'SOLAR_TERMICO': {'TAGS':[u'Rég. Esp. Solar Térmico'],'inConceptoAs':False,'valores':[],},
        'TERMICA_RENOVABLE': {'TAGS':[u'Rég. Esp. Térmico Renovable'],'inConceptoAs':False,'valores':[],},
        'TERMICA_NORENOVABLE': {'TAGS':[u'Rég. Esp. Térmico no Renov.'],'inConceptoAs':False,'valores':[],},
        'OTRAS_RENOVABLE': {'TAGS':[u'Rég. Esp. Otras Renovables'],'inConceptoAs':False,'valores':[],},
        # Tags correspondientes a generación termica no renovable:
        'CARBON': {'TAGS':[u'Coal', u'Carbón'],'inConceptoAs':False,'valores':[],},
        'NUCLEAR': {'TAGS':[u'Nuclear'],'inConceptoAs':False,'valores':[],},
        'FUEL_GAS': {'TAGS':[u'Fuel-Gas'],'inConceptoAs':False,'valores':[],},
        'REGIMEN_ORDINARIO_CON_PRIMA': {'TAGS':[u'Régimen ordinario con prima'],'inConceptoAs':False,'valores':[],},
        'CICLO_COMBINADO': {'TAGS':[u'Combined cycle GT', u'Ciclo Combinado'],'inConceptoAs':False,'valores':[],},
        'COGENERACION_Y_RESTO': {'TAGS':[u'Cogeneración y resto',u'Cogeneration and rest'],'inConceptoAs':False,'valores':[],},
        # Tags correspondientes a importacion:
        'CONSUMO_DE_BOMBEO': {'TAGS':[u'Consumo Bombeo'],'inConceptoAs':False,'valores':[],},
        #
        'IMPORTACION_PORTUGAL': {'TAGS':["Prog. Imp. Portugal"],'inConceptoAs':False,'valores':[],},
        'IMPORTACION_FRANCIA': {'TAGS':["Prog. Imp. Francia"],'inConceptoAs':False,'valores':[],},
        'IMPORTACION_ANDORRA': {'TAGS':["Prog. Imp. Andorra"],'inConceptoAs':False,'valores':[],},
        'IMPORTACION_MARRUECOS': {'TAGS':["Prog. Imp. Marruecos"],'inConceptoAs':False,'valores':[],},
        # Tags correspondientes a exportacion:
        'EXPORTACION_A_PORTUGAL': {'TAGS':["Prog. Exp. Portugal"],'inConceptoAs':False,'valores':[],},
        'EXPORTACION_A_FRANCIA': {'TAGS':["Prog. Exp. Francia"],'inConceptoAs':False,'valores':[],},
        'EXPORTACION_A_ANDORRA': {'TAGS':["Prog. Exp. Andorra"],'inConceptoAs':False,'valores':[],},
        'EXPORTACION_A_MARRUECOS': {'TAGS':["Prog. Exp. Marruecos"],'inConceptoAs':False,'valores':[],},
        }
        # Navigation tags while walking in the XML.
        self.__inSeriesTemporales = False
        self.__inPeriodo = False
        self.__inIntervalo = False
        
    def startElement(self, tag, attrib):
        if tag == self.TAG_SERIESTEMPORALES:
            self.__inSeriesTemporales = True
        if tag == self.TAG_CONCEPTO and self.__inSeriesTemporales == True:
            concepto = attrib.get("value")
            # Process Generacion:
            for key,value in self.parsingresults.iteritems():
                if concepto in value['TAGS']:
                    value['inConceptoAs'] = True
            
        if tag == self.TAG_PERIODO and self.__inSeriesTemporales:
            self.__inPeriodo = True
        if tag == self.TAG_INTERVALO and self.__inPeriodo and self.__inSeriesTemporales:
            self.__inIntervalo = True
        # Now this defines where are we so:
        if tag == "Ctd" and attrib.get("type") == "number" and  self.__inIntervalo and self.__inPeriodo and self.__inSeriesTemporales:
            for key,value in self.parsingresults.iteritems():
                if value['inConceptoAs']:
                    cantidad = attrib.get("value")
                    if str(cantidad) == "-":
                        cantidad = 0
                    else:
                        cantidad = unicodetodecimal(cantidad)
                    value['valores'].append(cantidad)

    def endElement(self, tag):
        '''
        '''
        if tag == self.TAG_SERIESTEMPORALES:
            self.__inSeriesTemporales = False
            for key,value in self.parsingresults.iteritems():
                value['inConceptoAs'] = False

        if tag == self.TAG_PERIODO:
            self.__inPeriodo = False
        if tag == self.TAG_INTERVALO:
            self.__inIntervalo = False

class ProgramaBaseFuncHandler(handler.ContentHandler):
    '''
    valid for year 2014>+
    classdocs
    Handler for XML file:
    Definición
    Es el programa de energía diario, con desglose horario, de las diferentes unidades de programación 
    correspondientes a ventas y adquisiciones de energía en el sistema eléctrico peninsular español 
    (mercado diario + contratación bilateral con entrega física).
    Direct Download for file:
    XML identifier:
    BAL_PBF_DD = PBF program energy generation in Contractación Bilateral in MWh.
    Unidades = MWh
    fuente: http://www.esios.ree.es/web-publica/
    ubicación en la web: Programas y Demanda -> Programas -> PBF
    '''
    # Tags del XML
    TAG_SERIESTEMPORALES = "SeriesTemporales"
    TAG_VALUE = "value"
    TAG_NUMBER = "number"
    TAG_TYPE = "type"
    TAG_CTD = "Ctd"
    TAG_ESPANA = "España"
    TAG_PERIODO = "Periodo"
    TAG_INTERVALO = "Intervalo"
    TAG_CONCEPTO = "Concepto"
    # Valores Posibles del atributo value del tag Concepto.
    
    def __init__(self):
        '''
        Constructor
        '''
        # TODO: add a check on date for this parser.
        handler.ContentHandler.__init__(self)
        self.parsingresults = \
        {'HIDRAULICA': {'TAGS':[u'Hidráulica (UGH + Turb. Bomb.)',u'Hydro (UGH + Pump. Gen.)'],'inConceptoAs':False,'valores':[],},
        'HIDRAULICA_OTROS': {'TAGS':[u'Resto hidráulica',u'Rest hydro'],'inConceptoAs':False,'valores':[],},
        'EOLICA': {'TAGS':[u'Eólica',u'Wind'],'inConceptoAs':False,'valores':[],},
        'SOLAR_FOTOVOLTAICO': {'TAGS':[u'Solar fotovoltaico',u'Solar PV'],'inConceptoAs':False,'valores':[],},
        'SOLAR_TERMICO': {'TAGS':[u'Solar térmico',u'Solar thermal'],'inConceptoAs':False,'valores':[],},
        'TERMICA_RENOVABLE': {'TAGS':[u'Térmica renovable',u'Therm renewable'],'inConceptoAs':False,'valores':[],},
        # Tags correspondientes a generación termica no renovable:
        'CARBON': {'TAGS':[u'Coal', u'Carbón'],'inConceptoAs':False,'valores':[],},
        'NUCLEAR': {'TAGS':[u'Nuclear'],'inConceptoAs':False,'valores':[],},
        'FUEL_GAS': {'TAGS':[u'Fuel + Gas',u'Fuel + Gas'],'inConceptoAs':False,'valores':[],},
        'CICLO_COMBINADO': {'TAGS':[u'Combined cycle GT', u'Ciclo Combinado'],'inConceptoAs':False,'valores':[],},
        'COGENERACION_Y_RESTO': {'TAGS':[u'Cogeneración y resto',u'Cogeneration and rest'],'inConceptoAs':False,'valores':[],},
        # Tags correspondientes a importacion:
        'CONSUMO_DE_BOMBEO': {'TAGS':[u'Consumo Bombeo'],'inConceptoAs':False,'valores':[],},
        #
        'SALDO_PORTUGAL': {'TAGS':["Saldo Portugal"],'inConceptoAs':False,'valores':[],},
        'SALDO_FRANCIA': {'TAGS':["Saldo Francia"],'inConceptoAs':False,'valores':[],},
        'SALDO_ANDORRA': {'TAGS':["Saldo Andorra"],'inConceptoAs':False,'valores':[],},
        'SALDO_MARRUECOS': {'TAGS':["Saldo Marruecos"],'inConceptoAs':False,'valores':[],},
        # Tags correspondientes a exportacion:
        }
        # Navigation tags while walking in the XML.
        self.__inSeriesTemporales = False
        self.__inPeriodo = False
        self.__inIntervalo = False
        
    def startElement(self, tag, attrib):
        if tag == self.TAG_SERIESTEMPORALES:
            self.__inSeriesTemporales = True
        if tag == self.TAG_CONCEPTO and self.__inSeriesTemporales == True:
            concepto = attrib.get("value")
            # Process Generacion:
            for key,value in self.parsingresults.iteritems():
                if concepto in value['TAGS']:
                    value['inConceptoAs'] = True
            
        if tag == self.TAG_PERIODO and self.__inSeriesTemporales:
            self.__inPeriodo = True
        if tag == self.TAG_INTERVALO and self.__inPeriodo and self.__inSeriesTemporales:
            self.__inIntervalo = True
        # Now this defines where are we so:
        if tag == "Ctd" and attrib.get("type") == "number" and  self.__inIntervalo and self.__inPeriodo and self.__inSeriesTemporales:
            for key,value in self.parsingresults.iteritems():
                if value['inConceptoAs']:
                    cantidad = attrib.get("value")
                    if str(cantidad) == "-":
                        cantidad = 0
                    else:
                        cantidad = unicodetodecimal(cantidad)
                    value['valores'].append(cantidad)

    def endElement(self, tag):
        '''
        '''
        if tag == self.TAG_SERIESTEMPORALES:
            self.__inSeriesTemporales = False
            for key,value in self.parsingresults.iteritems():
                value['inConceptoAs'] = False

        if tag == self.TAG_PERIODO:
            self.__inPeriodo = False
        if tag == self.TAG_INTERVALO:
            self.__inIntervalo = False

class ProgramaBaseFuncOLDERHandler(handler.ContentHandler):
    '''
    valid for year 2014< y >2012
    2011 is out of scope because info change from day to day without any logic.
    classdocs
    Handler for XML file:
    Definición
    Es el programa de energía diario, con desglose horario, de las diferentes unidades de programación 
    correspondientes a ventas y adquisiciones de energía en el sistema eléctrico peninsular español 
    (mercado diario + contratación bilateral con entrega física).
    Direct Download for file:
    XML identifier:
    BAL_PBF_DD = PBF program energy generation in Contractación Bilateral in MWh.
    Unidades = MWh
    fuente: http://www.esios.ree.es/web-publica/
    ubicación en la web: Programas y Demanda -> Programas -> PBF
    '''
    # Tags del XML
    TAG_SERIESTEMPORALES = "SeriesTemporales"
    TAG_VALUE = "value"
    TAG_NUMBER = "number"
    TAG_TYPE = "type"
    TAG_CTD = "Ctd"
    TAG_ESPANA = "España"
    TAG_PERIODO = "Periodo"
    TAG_INTERVALO = "Intervalo"
    TAG_CONCEPTO = "Concepto"
    # Valores Posibles del atributo value del tag Concepto.
    
    def __init__(self):
        '''
        Constructor
        '''
        # TODO: add a check on date for this parser.
        handler.ContentHandler.__init__(self)
        self.parsingresults = \
        {'HIDRAULICA': {'TAGS':[u'Hidráulica Convencional'],'inConceptoAs':False,'valores':[],},
        'HIDRAULICA_OTROS': {'TAGS':[u'Rég. Esp. Hidráulico'],'inConceptoAs':False,'valores':[],},
        'HIDRAULICA_BOMBEO': {'TAGS':[u'Turbinación bombeo'],'inConceptoAs':False,'valores':[],},
        'EOLICA': {'TAGS':[u'Rég. Esp. Eólico'],'inConceptoAs':False,'valores':[],},
        'SOLAR_FOTOVOLTAICO': {'TAGS':[u'Rég. Esp. Solar Fotovoltaico'],'inConceptoAs':False,'valores':[],},
        'SOLAR_TERMICO': {'TAGS':[u'Rég. Esp. Solar Térmico'],'inConceptoAs':False,'valores':[],},
        'TERMICA_RENOVABLE': {'TAGS':[u'Rég. Esp. Térmico Renovable'],'inConceptoAs':False,'valores':[],},
        'TERMICA_NORENOVABLE': {'TAGS':[u'Rég. Esp. Térmico no Renov.'],'inConceptoAs':False,'valores':[],},
        'OTRAS_RENOVABLE': {'TAGS':[u'Rég. Esp. Otras Renovables'],'inConceptoAs':False,'valores':[],},
        # Tags correspondientes a generación termica no renovable:
        'CARBON': {'TAGS':[u'Coal', u'Carbón'],'inConceptoAs':False,'valores':[],},
        'NUCLEAR': {'TAGS':[u'Nuclear'],'inConceptoAs':False,'valores':[],},
        'FUEL_GAS': {'TAGS':[u'Fuel-Gas'],'inConceptoAs':False,'valores':[],},
        'REGIMEN_ORDINARIO_CON_PRIMA': {'TAGS':[u'Régimen ordinario con prima'],'inConceptoAs':False,'valores':[],},
        'CICLO_COMBINADO': {'TAGS':[u'Combined cycle GT', u'Ciclo Combinado'],'inConceptoAs':False,'valores':[],},
        'COGENERACION_Y_RESTO': {'TAGS':[u'Cogeneración y resto',u'Cogeneration and rest'],'inConceptoAs':False,'valores':[],},
        # Tags correspondientes a importacion:
        'CONSUMO_DE_BOMBEO': {'TAGS':[u'Consumo Bombeo'],'inConceptoAs':False,'valores':[],},
        #
        'SALDO_PORTUGAL': {'TAGS':["Saldo Portugal"],'inConceptoAs':False,'valores':[],},
        'SALDO_FRANCIA': {'TAGS':["Saldo Francia"],'inConceptoAs':False,'valores':[],},
        'SALDO_ANDORRA': {'TAGS':["Saldo Andorra"],'inConceptoAs':False,'valores':[],},
        'SALDO_MARRUECOS': {'TAGS':["Saldo Marruecos"],'inConceptoAs':False,'valores':[],},
        # Tags correspondientes a exportacion:
        }
        # Navigation tags while walking in the XML.
        self.__inSeriesTemporales = False
        self.__inPeriodo = False
        self.__inIntervalo = False
        
    def startElement(self, tag, attrib):
        if tag == self.TAG_SERIESTEMPORALES:
            self.__inSeriesTemporales = True
        if tag == self.TAG_CONCEPTO and self.__inSeriesTemporales == True:
            concepto = attrib.get("value")
            # Process Generacion:
            for key,value in self.parsingresults.iteritems():
                if concepto in value['TAGS']:
                    value['inConceptoAs'] = True
            
        if tag == self.TAG_PERIODO and self.__inSeriesTemporales:
            self.__inPeriodo = True
        if tag == self.TAG_INTERVALO and self.__inPeriodo and self.__inSeriesTemporales:
            self.__inIntervalo = True
        # Now this defines where are we so:
        if tag == "Ctd" and attrib.get("type") == "number" and  self.__inIntervalo and self.__inPeriodo and self.__inSeriesTemporales:
            for key,value in self.parsingresults.iteritems():
                if value['inConceptoAs']:
                    cantidad = attrib.get("value")
                    if str(cantidad) == "-":
                        cantidad = 0
                    else:
                        cantidad = unicodetodecimal(cantidad)
                    value['valores'].append(cantidad)

    def endElement(self, tag):
        '''
        '''
        if tag == self.TAG_SERIESTEMPORALES:
            self.__inSeriesTemporales = False
            for key,value in self.parsingresults.iteritems():
                value['inConceptoAs'] = False

        if tag == self.TAG_PERIODO:
            self.__inPeriodo = False
        if tag == self.TAG_INTERVALO:
            self.__inIntervalo = False

class PrevEolHandler(handler.ContentHandler):
    '''
    classdocs

    PREVEOL_DD = La propria prevision de la energia eolica
    generada para la red electrica.
    Solicitar y Nombre del fichero:
    Contenido del fichero:
    fuente: http://www.esios.ree.es/web-publica/
    ubicación en la web: Previsiones > Previsión de la producción eólica nacional peninsular >  Previsión de la producción eólica nacional peninsular
    '''
    SERIESTEMPORALES = "SeriesTemporales"
    PERIODO = "Periodo"
    INTERVALO = "Intervalo"
    CTD = "Ctd"

    def __init__(self):
        '''
        Constructor
        '''
        handler.ContentHandler.__init__(self)
        self.listavalores = []
        self.__inseriestemporales = False
        self.__inperiodo = False
        self.__inintervalo = False

    def startElement(self, tag, attrib):
        '''
        start and end element
        '''
        if tag == self.SERIESTEMPORALES:
            self.__inseriestemporales = True
        if tag == self.PERIODO and self.__inseriestemporales:
            self.__inperiodo = True
        if tag == self.INTERVALO and self.__inperiodo and \
        self.__inseriestemporales:
            self.__inintervalo = True
        if tag == self.CTD and self.__inintervalo and \
        self.__inperiodo and self.__inseriestemporales:
            self.listavalores.append(unicodetodecimal(attrib.get("v")))

        def endElement(self, tag):
            if tag == self.SERIESTEMPORALES:
                self.__inSeriesTemporales = False
                if tag == self.PERIODO:
                    self.__inPeriodo = False
                if tag == self.INTERVALO:
                    self.__inIntervalo = False

class PrevDemandaHandler(handler.ContentHandler):
    '''
    classdocs
    DEMANDEFORCAST = La propria prevision de demanda de la red electrica.
    fuente: http://www.esios.ree.es/web-publica/
    ubicación en la web: Previsiones > Previsión de la demanda eléctrica nacional peninsular > previsión del OS
    '''
    SERIESTEMPORALES = "SeriesTemporales"
    PERIODO = "Periodo"
    INTERVALO = "Intervalo"
    CTD = "Ctd"

    def __init__(self):
        '''
        Constructor
        '''
        handler.ContentHandler.__init__(self)
        self.listavalores = []
        self.__inseriestemporales = False
        self.__inperiodo = False
        self.__inintervalo = False

    def startElement(self, tag, attrib):
        '''
        start and end elements in the parser.
        '''
        if tag == self.SERIESTEMPORALES:
            self.__inseriestemporales = True
        if tag == self.PERIODO and self.__inseriestemporales:
            self.__inperiodo = True
        if tag == self.INTERVALO and self.__inperiodo and \
        self.__inseriestemporales:
            self.__inintervalo = True
        if tag == self.CTD and self.__inintervalo and \
        self.__inperiodo and self.__inseriestemporales:
            self.listavalores.append(unicodetodecimal(attrib.get("v")))

        def endElement(self, tag):
            if tag == self.SERIESTEMPORALES:
                self.__inseriestemporales = False
                if tag == self.PERIODO:
                    self.__inperiodo = False
                if tag == self.INTERVALO:
                    self.__inintervalo = False


class EnergiaGestionadaHandler(handler.ContentHandler):
    '''
    classdocs

    MD_EGEST_DD = La energia gestionada en el mercado diario componente española
    generada para la red electrica.
    Solicitar y Nombre del fichero:
    Contenido del fichero:
    fuente: http://www.esios.ree.es/web-publica/
    ubicación en la web: Mercados - MIBEL > Mercado Diario > Energía gestionada
    '''
    SERIESTEMPORALES = "SeriesTemporales"
    PERIODO = "Periodo"
    INTERVALO = "Intervalo"
    CTD = "Ctd"

    def __init__(self):
        '''
        Constructor
        '''
        handler.ContentHandler.__init__(self)
        self.listavalores = []
        self.__inseriestemporales = False
        self.__inperiodo = False
        self.__inintervalo = False

    def startElement(self, tag, attrib):
        '''
        start and end element
        '''
        if tag == self.SERIESTEMPORALES:
            self.__inseriestemporales = True
        if tag == self.PERIODO and self.__inseriestemporales:
            self.__inperiodo = True
        if tag == self.INTERVALO and self.__inperiodo and \
        self.__inseriestemporales:
            self.__inintervalo = True
        if tag == self.CTD and self.__inintervalo and \
        self.__inperiodo and self.__inseriestemporales:
            self.listavalores.append(unicodetodecimal(attrib.get("value")))

    def endElement(self, tag):
        if tag == self.SERIESTEMPORALES:
            self.__inSeriesTemporales = False
            if tag == self.PERIODO:
                self.__inPeriodo = False
            if tag == self.INTERVALO:
                self.__inIntervalo = False

class PreciosHandler(handler.ContentHandler):
    '''
    classdocs

    MD_PREC_DD = La energia gestionada en el mercado diario componente española
    generada para la red electrica.
    Solicitar y Nombre del fichero:
    Contenido del fichero:
    fuente: http://www.esios.ree.es/web-publica/
    ubicación en la web: Mercados - MIBEL > Mercado Diario > Energía gestionada
    '''
    SERIESTEMPORALES = "SeriesTemporales"
    CONCEPTO = "Concepto"
    PERIODO = "Periodo"
    INTERVALO = "Intervalo"
    CTD = "Ctd"

    def __init__(self):
        '''
        Constructor
        '''
        handler.ContentHandler.__init__(self)
        self.listavalores = []
        self.__inseriestemporales = False
        self.__inEspanha = False
        self.__inperiodo = False
        self.__inintervalo = False

    def startElement(self, tag, attrib):
        '''
        start and end element
        '''
        if tag == self.SERIESTEMPORALES:
            self.__inseriestemporales = True
        if tag == self.CONCEPTO and self.__inseriestemporales:
            if attrib.get("value") == u'España':
                self.__inEspanha = True
        if tag == self.PERIODO and self.__inseriestemporales and self.__inEspanha:
            self.__inperiodo = True
        if tag == self.INTERVALO and self.__inperiodo and \
        self.__inseriestemporales and self.__inEspanha:
            self.__inintervalo = True
        if tag == self.CTD and self.__inintervalo and \
        self.__inperiodo and self.__inseriestemporales and self.__inEspanha:
            self.listavalores.append(unicodetodecimal(attrib.get("value")))

    def endElement(self, tag):
        if tag == self.SERIESTEMPORALES:
            self.__inseriestemporales = False
            self.__inEspanha = False
            if tag == self.PERIODO:
                self.__inPeriodo = False
            if tag == self.INTERVALO:
                self.__inIntervalo = False


# -*- coding: utf-8 -*-
'''
Created on 27/02/2013
@author: hmarrao
'''
# imports:
from xml.sax import handler, make_parser
from utilities import unicodetodecimal,validafecha,esiosreeurl
from urllib2 import urlopen
# Constantes:

def getdemandeforcast(fecha):
    '''
    function to simplify DemandeforcastHandler usage
    '''
    try:
        validafecha(fecha)
        url = esiosreeurl(fecha, xmlid="demanda_aux")
        infile = urlopen(url)
        parser = make_parser()
        handler = DemandeforcastHandler()
        parser.setContentHandler(handler)
        parser.parse(infile)
    except:
        raise
    else:
        return handler.listavalores

# The handlers implementation a handlers by needed xml:
class DemandeforcastHandler(handler.ContentHandler):
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

def getpreveoldd(fecha):
    '''
    function to simplify PreveolddHandler usage
    '''
    try:
        validafecha(fecha)
        url = esiosreeurl(fecha, xmlid="preveol_DD")
        infile = urlopen(url)
        parser = make_parser()
        handler = DemandeforcastHandler()
        parser.setContentHandler(handler)
        parser.parse(infile)
    except:
        raise
    else:
        return handler.listavalores

class PreveolddHandler(handler.ContentHandler):
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

def getmdegestdd(fecha):
    url = esiosreeurl(fecha, xmlid="MD_EGEST_DD")
    infile = urlopen(url, 'r')
    parser = make_parser()
    handler = MDEgestddHandler()
    parser.setContentHandler(handler)
    parser.parse(infile)
    return handler.listavalores

class MDEgestddHandler(handler.ContentHandler):
    '''
    classdocs

    MD_EGEST_DD = La energia gestionada en el mercado diario componente española
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
            self.listavalores.append(unicodetodecimal(attrib.get("value")))

    def endElement(self, tag):
        if tag == self.SERIESTEMPORALES:
            self.__inSeriesTemporales = False
            if tag == self.PERIODO:
                self.__inPeriodo = False
            if tag == self.INTERVALO:
                self.__inIntervalo = False

class BalPBFddHandler(handler.ContentHandler):
    '''
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
    # Tags correspondientes a generación:
    HIDRAULICA_CONVENCIONAL = [u'Hidráulica Convencional']
    HIDRAULICA_BOMBEO_PURO = [u'Turbinación bombeo']
    NUCLEAR = [u'Nuclear']
    CARBON = [u'Coal', u'Carbón']
    FUEL_GAS_SIN_PRIMA = [u'Fuel-Gas']
    FUEL_GAS_CON_PRIMA = [u'Régimen ordinario con prima',u'Régimen Ordinario con Prima']
    CICLO_COMBINADO = ["Combined Cycle", "Ciclo Combinado"]
    REGIMEN_ESPECIAL_A_MERCADO = [u'Total Régimen Especial']
    UNIDADES_GENERICAS = [u'Unid. Prog. Genéricas']
    IMPORTACION_PORTUGAL = ["Prog. Imp. Portugal"]
    IMPORTACION_FRANCIA = ["Prog. Imp. Francia"]
    IMPORTACION_ANDORRA = ["Prog. Imp. Andorra"]
    IMPORTACION_MARRUECOS = ["Prog. Imp. Marruecos"]
    # Tags correspondientes a demanda:
    CONSUMO_DE_BOMBEO = [u'Consumo Bombeo']
    EXPORTACION_A_PORTUGAL = ["Prog. Exp. Portugal"]
    EXPORTACION_A_FRANCIA = ["Prog. Exp. Francia"]
    EXPORTACION_A_ANDORRA = ["Prog. Exp. Andorra"]
    EXPORTACION_A_MARRUECOS = ["Prog. Exp. Marruecos"]

    def __init__(self):
        '''
        Constructor
        '''
        handler.ContentHandler.__init__(self)
        # Valores de produccion:
        self.listavaloresHIDRAULICA_CONVENCIONAL = []
        self.listavaloresHIDRAULICA_BOMBEO_PURO = []
        self.listavaloresNUCLEAR = []
        self.listavaloresCARBON = []
        self.listavaloresFUEL_GAS_SIN_PRIMA = []
        self.listavaloresFUEL_GAS_CON_PRIMA = []
        self.listavaloresCICLO_COMBINADO = []
        self.listavaloresREGIMEN_ESPECIAL_A_MERCADO = []
        self.listavaloresUNIDADES_GENERICAS = []
        self.listavaloresIMPORTACION_FRANCIA = []
        self.listavaloresIMPORTACION_PORTUGAL = []
        self.listavaloresIMPORTACION_MARRUECOS = []
        self.listavaloresIMPORTACION_ANDORRA = []
        # Valores de demanda:
        self.listavaloresCONSUMO_DE_BOMBEO = []
        self.listavaloresEXPORTACION_A_FRANCIA = []
        self.listavaloresEXPORTACION_A_PORTUGAL = []
        self.listavaloresEXPORTACION_A_MARRUECOS = []
        self.listavaloresEXPORTACION_A_ANDORRA = []
        self.listavaloresNuclear = []
        self.listavaloresCoal = []
        self.listavaloresFuelOilGas = []
        self.listavaloresCombinedCycle = []
        self.listavaloresSpecialRegimeGenMarket = []
        # Navigation tags while walking in the XML.
        self.__inSeriesTemporales = False
        self.__inPeriodo = False
        self.__inIntervalo = False
        self.__inConceptoAsHIDRAULICA_CONVENCIONAL = False
        self.__inConceptoAsHIDRAULICA_BOMBEO_PURO = False
        self.__inConceptoAsNUCLEAR = False
        self.__inConceptoAsCARBON = False
        self.__inConceptoAsFUEL_GAS_SIN_PRIMA = False
        self.__inConceptoAsFUEL_GAS_CON_PRIMA = False
        self.__inConceptoAsCICLO_COMBINADO = False
        self.__inConceptoAsREGIMEN_ESPECIAL_A_MERCADO = False
        self.__inConceptoAsUNIDADES_GENERICAS = False
        self.__inConceptoAsIMPORTACION_PORTUGAL = False
        self.__inConceptoAsIMPORTACION_FRANCIA = False
        self.__inConceptoAsIMPORTACION_ANDORRA = False
        self.__inConceptoAsIMPORTACION_MARRUECOS = False
        # Navegacion tags while walking in the XML.
        self.__inConceptoAsCONSUMO_DE_BOMBEO = False
        self.__inConceptoAsEXPORTACION_A_FRANCIA = False
        self.__inConceptoAsEXPORTACION_A_PORTUGAL = False
        self.__inConceptoAsEXPORTACION_A_MARRUECOS = False
        self.__inConceptoAsEXPORTACION_A_ANDORRA = False

    def startElement(self, tag, attrib):
        if tag == self.TAG_SERIESTEMPORALES:
            self.__inSeriesTemporales = True
        if tag == self.TAG_CONCEPTO and self.__inSeriesTemporales == True:
            concepto = attrib.get("value")
            # Process Generacion:
            if concepto in self.HIDRAULICA_CONVENCIONAL:
                self.__inConceptoAsHIDRAULICA_CONVENCIONAL = True
            if concepto in self.HIDRAULICA_BOMBEO_PURO:
                self.__inConceptoAsHIDRAULICA_BOMBEO_PURO = True
            if concepto in self.NUCLEAR:
                self.__inConceptoAsNUCLEAR = True
            if concepto in self.CARBON:
                self.__inConceptoAsCARBON = True
            if concepto in self.FUEL_GAS_SIN_PRIMA:
                self.__inConceptoAsFUEL_GAS_SIN_PRIMA = True
            if concepto in self.FUEL_GAS_CON_PRIMA:
                self.__inConceptoAsFUEL_GAS_CON_PRIMA = True
            if concepto in self.CICLO_COMBINADO:
                self.__inConceptoAsCICLO_COMBINADO = True
            if concepto in self.REGIMEN_ESPECIAL_A_MERCADO:
                self.__inConceptoAsREGIMEN_ESPECIAL_A_MERCADO = True
            if concepto in self.UNIDADES_GENERICAS:
                self.__inConceptoAsUNIDADES_GENERICAS = True
            # imported energy should be like Generacion:
            if concepto in self.IMPORTACION_FRANCIA:
                self.__inConceptoAsIMPORTACION_FRANCIA = True
            if concepto in self.IMPORTACION_PORTUGAL:
                self.__inConceptoAsIMPORTACION_PORTUGAL = True
            if concepto in self.IMPORTACION_MARRUECOS:
                self.__inConceptoAsIMPORTACION_MARRUECOS = True
            if concepto in self.IMPORTACION_ANDORRA:
                self.__inConceptoAsIMPORTACION_ANDORRA = True
            # Process demanda:
            if concepto in self.CONSUMO_DE_BOMBEO:
                self.__inConceptoAsCONSUMO_DE_BOMBEO = True
            if concepto in self.EXPORTACION_A_FRANCIA:
                self.__inConceptoAsEXPORTACION_A_FRANCIA = True
            if concepto in self.EXPORTACION_A_PORTUGAL:
                self.__inConceptoAsEXPORTACION_A_PORTUGAL = True
            if concepto in self.EXPORTACION_A_MARRUECOS:
                self.__inConceptoAsEXPORTACION_A_MARRUECOS = True
            if concepto in self.EXPORTACION_A_ANDORRA:
                self.__inConceptoAsEXPORTACION_A_ANDORRA = True
        if tag == self.TAG_PERIODO and self.__inSeriesTemporales:
            self.__inPeriodo = True
        if tag == self.TAG_INTERVALO and self.__inPeriodo and self.__inSeriesTemporales:
            self.__inIntervalo = True
        # Now this defines where are we so:
        if tag == "Ctd" and attrib.get("type") == "number" and  self.__inIntervalo and self.__inPeriodo and self.__inSeriesTemporales:
            if self.__inConceptoAsHIDRAULICA_CONVENCIONAL:
                cantidad = attrib.get("value")
                if str(cantidad) == "-":
                    cantidad = 0
                else:
                    cantidad = unicodetodecimal(cantidad)
                self.listavaloresHIDRAULICA_CONVENCIONAL.append(cantidad)
            if self.__inConceptoAsHIDRAULICA_BOMBEO_PURO:
                cantidad = attrib.get("value")
                if str(cantidad) == "-":
                    cantidad = 0
                else:
                    cantidad = unicodetodecimal(cantidad)
                self.listavaloresHIDRAULICA_BOMBEO_PURO.append(cantidad)
            if self.__inConceptoAsNUCLEAR:
                cantidad = attrib.get("value")
                if str(cantidad) == "-":
                    cantidad = 0
                else:
                    cantidad = unicodetodecimal(cantidad)
                self.listavaloresNUCLEAR.append(cantidad)
            if self.__inConceptoAsCARBON:
                cantidad = attrib.get("value")
                if str(cantidad) == "-":
                    cantidad = 0
                else:
                    cantidad = unicodetodecimal(cantidad)
                self.listavaloresCARBON.append(cantidad)
            if self.__inConceptoAsFUEL_GAS_SIN_PRIMA:
                cantidad = attrib.get("value")
                if str(cantidad) == "-":
                    cantidad = 0
                else:
                    cantidad = unicodetodecimal(cantidad)
                self.listavaloresFUEL_GAS_SIN_PRIMA.append(cantidad)
            if self.__inConceptoAsFUEL_GAS_CON_PRIMA:
                cantidad = attrib.get("value")
                if str(cantidad) == "-":
                    cantidad = 0
                else:
                    cantidad = unicodetodecimal(cantidad)
                self.listavaloresFUEL_GAS_CON_PRIMA.append(cantidad)
            if self.__inConceptoAsCICLO_COMBINADO:
                cantidad = attrib.get("value")
                if str(cantidad) == "-":
                    cantidad = 0
                else:
                    cantidad = unicodetodecimal(cantidad)
                self.listavaloresCICLO_COMBINADO.append(cantidad)
            if self.__inConceptoAsREGIMEN_ESPECIAL_A_MERCADO:
                cantidad = attrib.get("value")
                if str(cantidad) == "-":
                    cantidad = 0
                else:
                    cantidad = unicodetodecimal(cantidad)
                self.listavaloresREGIMEN_ESPECIAL_A_MERCADO.append(cantidad)
            # There are two tags with the same name: only want the first tag so if values reached its maximum
            # do not insert any more values. Because of winter and summer hour change
            # the code will use the Hidraulica values to control this.
            if len(self.listavaloresUNIDADES_GENERICAS) < len(self.listavaloresHIDRAULICA_CONVENCIONAL):
                if self.__inConceptoAsUNIDADES_GENERICAS:
                    cantidad = attrib.get("value")
                    if str(cantidad) == "-":
                        cantidad = 0
                    else:
                        cantidad = unicodetodecimal(cantidad)
                    self.listavaloresUNIDADES_GENERICAS.append(cantidad)
            if self.__inConceptoAsIMPORTACION_FRANCIA:
                cantidad = attrib.get("value")
                if str(cantidad) == "-":
                    cantidad = 0
                else:
                    cantidad = unicodetodecimal(cantidad)
                self.listavaloresIMPORTACION_FRANCIA.append(cantidad)
            if self.__inConceptoAsIMPORTACION_PORTUGAL:
                cantidad = attrib.get("value")
                if str(cantidad) == "-":
                    cantidad = 0
                else:
                    cantidad = unicodetodecimal(cantidad)
                self.listavaloresIMPORTACION_PORTUGAL.append(cantidad)
            if self.__inConceptoAsIMPORTACION_MARRUECOS:
                cantidad = attrib.get("value")
                if str(cantidad) == "-":
                    cantidad = 0
                else:
                    cantidad = unicodetodecimal(cantidad)
                self.listavaloresIMPORTACION_MARRUECOS.append(cantidad)
            if self.__inConceptoAsIMPORTACION_ANDORRA:
                cantidad = attrib.get("value")
                if str(cantidad) == "-":
                    cantidad = 0
                else:
                    cantidad = unicodetodecimal(cantidad)
                self.listavaloresIMPORTACION_ANDORRA.append(cantidad)
            if self.__inConceptoAsCONSUMO_DE_BOMBEO:
                cantidad = attrib.get("value")
                if str(cantidad) == "-":
                    cantidad = 0
                else:
                    cantidad = unicodetodecimal(cantidad)
                self.listavaloresCONSUMO_DE_BOMBEO.append(abs(cantidad))
            if self.__inConceptoAsEXPORTACION_A_FRANCIA:
                cantidad = attrib.get("value")
                if str(cantidad) == "-":
                    cantidad = 0
                else:
                    cantidad = unicodetodecimal(cantidad)
                self.listavaloresEXPORTACION_A_FRANCIA.append(abs(cantidad))
            if self.__inConceptoAsEXPORTACION_A_PORTUGAL:
                cantidad = attrib.get("value")
                if str(cantidad) == "-":
                    cantidad = 0
                else:
                    cantidad = unicodetodecimal(cantidad)
                self.listavaloresEXPORTACION_A_PORTUGAL.append(abs(cantidad))
            if self.__inConceptoAsEXPORTACION_A_MARRUECOS:
                cantidad = attrib.get("value")
                if str(cantidad) == "-":
                    cantidad = 0
                else:
                    cantidad = unicodetodecimal(cantidad)
                self.listavaloresEXPORTACION_A_MARRUECOS.append(abs(cantidad))
            if self.__inConceptoAsEXPORTACION_A_ANDORRA:
                cantidad = attrib.get("value")
                if str(cantidad) == "-":
                    cantidad = 0
                else:
                    cantidad = unicodetodecimal(cantidad)
                self.listavaloresEXPORTACION_A_ANDORRA.append(abs(cantidad))

    def endElement(self, tag):
        '''
        '''
        if tag == self.TAG_SERIESTEMPORALES:
            self.__inSeriesTemporales = False
            self.__inConceptoAsHIDRAULICA_CONVENCIONAL = False
            self.__inConceptoAsHIDRAULICA_BOMBEO_PURO = False
            self.__inConceptoAsNUCLEAR = False
            self.__inConceptoAsCARBON = False
            self.__inConceptoAsFUEL_GAS_SIN_PRIMA = False
            self.__inConceptoAsFUEL_GAS_CON_PRIMA = False
            self.__inConceptoAsCICLO_COMBINADO = False
            self.__inConceptoAsREGIMEN_ESPECIAL_A_MERCADO = False
            self.__inConceptoAsUNIDADES_GENERICAS = False
            self.__inConceptoAsIMPORTACION_FRANCIA = False
            self.__inConceptoAsIMPORTACION_PORTUGAL = False
            self.__inConceptoAsIMPORTACION_MARRUECOS = False
            self.__inConceptoAsIMPORTACION_ANDORRA = False
            self.__inConceptoAsCONSUMO_DE_BOMBEO = False
            self.__inConceptoAsEXPORTACION_A_FRANCIA = False
            self.__inConceptoAsEXPORTACION_A_PORTUGAL = False
            self.__inConceptoAsEXPORTACION_A_MARRUECOS = False
            self.__inConceptoAsEXPORTACION_A_ANDORRA = False
        if tag == self.TAG_PERIODO:
            self.__inPeriodo = False
        if tag == self.TAG_INTERVALO:
            self.__inIntervalo = False

class CBFPBFddHandler(BalPBFddHandler):
    '''
    fuente: http://www.esios.ree.es/web-publica/
    ubicación en la web: Programas y Demanda -> Contractación Bilateral -> PBF
    '''
    def __init__(self):
        BalPBFddHandler.__init__(self)
        #super(CBFPBFddHandler,self).__init__()

class DEMPBFddHandler(handler.ContentHandler):
    '''
    fuente: http://www.esios.ree.es/web-publica/
    ubicación en la web: Programas y Demanda -> Composición de la Demanda -> PBF
    '''
    # tags del XML
    TAG_SERIESTEMPORALES = "SeriesTemporales"
    TAG_CONCEPTO = "Concepto"
    TAG_PERIODO = "Periodo"
    TAG_INTERVALO = "Intervalo"
    TAG_CTD = "Ctd"
    # Valores Posibles del atributo value del tag Concepto.
    # Tags correspondientes a la composición de la Demanda:
    COMER_MERCADO_LIBRE = [u'Comerc. mercado libre']
    COMER_ULTIMO_RECURSO = [u'Comerc. último recurso']
    CONS_DIRECTO_MERCADO = [u'Cons. directo mercado']
    CONSUMO_DE_SERV_AUX = [u'Consumo de Serv. Aux.']
    CORRECCION_EOLICA = [u'Corrección Eólica']
    CORRECCION_SOLAR_FV = [u'Corrección Solar FV']
    CORRECCION_REE = [u'Corrección REE']

    def __init__(self):
        '''
        Constructor
        '''
        handler.ContentHandler.__init__(self)
        self.listavaloresCOMER_MERCADO_LIBRE = []
        self.listavaloresCOMER_ULTIMO_RECURSO = []
        self.listavaloresCONS_DIRECTO_MERCADO = []
        self.listavaloresCONSUMO_DE_SERV_AUX = []
        self.listavaloresCORRECCION_EOLICA = []
        self.listavaloresCORRECCION_SOLAR_FV = []
        self.listavaloresCORRECCION_REE = []
        self.__inConceptoAsCOMER_MERCADO_LIBRE = False
        self.__inConceptoAsCOMER_ULTIMO_RECURSO = False
        self.__inConceptoAsCONS_DIRECTO_MERCADO = False
        self.__inConceptoAsCONSUMO_DE_SERV_AUX = False
        self.__inConceptoAsCORRECCION_EOLICA = False
        self.__inConceptoAsCORRECCION_SOLAR_FV = False
        self.__inConceptoAsCORRECCION_REE = False
        self.__inSeriesTemporales = False
        self.__inPeriodo = False
        self.__inIntervalo = False

    def startElement(self, tag, attrib):
        '''
        start and end elements in the parser.
        '''
        if tag == self.TAG_SERIESTEMPORALES:
            self.__inSeriesTemporales = True
        if tag == self.TAG_CONCEPTO and self.__inSeriesTemporales == True:
            concepto = attrib.get("value")
            # Process Valores comercializacion:
            if concepto in self.COMER_MERCADO_LIBRE:
                self.__inConceptoAsCOMER_MERCADO_LIBRE = True
            if concepto in self.COMER_ULTIMO_RECURSO:
                self.__inConceptoAsCOMER_ULTIMO_RECURSO = True
            if concepto in self.CONS_DIRECTO_MERCADO:
                self.__inConceptoAsCONS_DIRECTO_MERCADO = True
            if concepto in self.CONSUMO_DE_SERV_AUX:
                self.__inConceptoAsCONSUMO_DE_SERV_AUX = True
            if concepto in self.CORRECCION_EOLICA:
                self.__inConceptoAsCORRECCION_EOLICA = True
            if concepto in self.CORRECCION_SOLAR_FV:
                self.__inConceptoAsCORRECCION_SOLAR_FV = True
            if concepto in self.CORRECCION_REE:
                self.__inConceptoAsCORRECCION_REE = True
        if tag == self.TAG_PERIODO and self.__inSeriesTemporales:
            self.__inPeriodo = True
        if tag == self.TAG_INTERVALO and self.__inPeriodo and \
        self.__inSeriesTemporales:
            self.__inIntervalo = True
        if tag == self.TAG_CTD and attrib.get("type") == "number" and  self.__inIntervalo and self.__inPeriodo and self.__inSeriesTemporales:
            #first: prepare data to be inserted.
            cantidad = attrib.get("value")
            if str(cantidad) == "-":
                cantidad = 0
            else:
                cantidad = unicodetodecimal(cantidad)
            #second: Put data in proper list
            if self.__inConceptoAsCOMER_MERCADO_LIBRE:
                self.listavaloresCOMER_MERCADO_LIBRE.append(cantidad)
            if self.__inConceptoAsCOMER_ULTIMO_RECURSO:
                self.listavaloresCOMER_ULTIMO_RECURSO.append(cantidad)
            if self.__inConceptoAsCONS_DIRECTO_MERCADO:
                self.listavaloresCONS_DIRECTO_MERCADO.append(cantidad)
            if self.__inConceptoAsCONSUMO_DE_SERV_AUX:
                self.listavaloresCONSUMO_DE_SERV_AUX.append(cantidad)
            if self.__inConceptoAsCORRECCION_EOLICA:
                self.listavaloresCORRECCION_EOLICA.append(cantidad)
            if self.__inConceptoAsCORRECCION_SOLAR_FV:
                self.listavaloresCORRECCION_SOLAR_FV.append(cantidad)
            if self.__inConceptoAsCORRECCION_REE:
                self.listavaloresCORRECCION_REE.append(cantidad)

    def endElement(self, tag):
        '''
        '''
        if tag == self.TAG_SERIESTEMPORALES:
            self.__inSeriesTemporales = False
            self.__inConceptoAsCOMER_MERCADO_LIBRE = False
            self.__inConceptoAsCOMER_ULTIMO_RECURSO = False
            self.__inConceptoAsCONS_DIRECTO_MERCADO = False
            self.__inConceptoAsCONSUMO_DE_SERV_AUX = False
            self.__inConceptoAsCORRECCION_EOLICA = False
            self.__inConceptoAsCORRECCION_SOLAR_FV = False
            self.__inConceptoAsCORRECCION_REE = False
        if tag == self.TAG_PERIODO:
            self.__inPeriodo = False
        if tag == self.TAG_INTERVALO:
            self.__inIntervalo = False

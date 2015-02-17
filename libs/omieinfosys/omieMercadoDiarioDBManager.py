# -*- coding: utf-8 -*-
#
# This Module to handle db connections!
# omieMercadoDiario TecnologiasWeb
#                   PreciosWeb
#                   omieStudyData
#
# TODO: omieStudyData :: Collection Model:

from mongoengine import *
#from omieMercadoDiarioDBManager import db

class PreciosWeb(Document):
    """
    Manages PreciosWeb as delivered by PreciosMercadoDiarioParser Collection/Table

    > Note to developers and mongo users:
        Check last document available:
        Check last document available:

    """
    fecha = DateTimeField(unique=True)
    PreciosES = ListField()
    PreciosPT = ListField()
    PreciosMI = ListField()

    @queryset_manager
    def lastdateindb(doc_cls, queryset):
        """
        """
        result = queryset.order_by('-fecha')[0].fecha
        return result

    @queryset_manager
    def numofrecords(doc_cls, queryset):
        """
        """
        result = queryset.count()
        return result

    @queryset_manager
    def status(doc_cls, queryset):
        """
        Gives Collection status:
            * Start Date record startrecdate
            * End Date record
            * Num of record
        """

        numofrecord = queryset.count()
        if numofrecord == 0:
            startrecdate = None
            endrecdate = None
        else:
            startrecdate = queryset.order_by('fecha')[0].fecha
            endrecdate = queryset.order_by('-fecha')[0].fecha

        return {'startrecdate':startrecdate,
                'endrecdate':endrecdate,
                'numofrecord':numofrecord,}
    
    
class EnergiaGestionadaWeb(Document):
    """
    Manages EnergiaGestionadaWeb as delivered by EnergiaGestionadaParser Collection/Table

    > Note to developers and mongo users:
        Check last document available:
        Check last document available:

    """
    fecha = DateTimeField(unique=True)
    EnergiaES = DictField()
    EnergiaPT = DictField()
    EnergiaMI = DictField()

    @queryset_manager
    def lastdateindb(doc_cls, queryset):
        """
        """
        result = queryset.order_by('-fecha')[0].fecha
        return result

    @queryset_manager
    def numofrecords(doc_cls, queryset):
        """
        """
        result = queryset.count()
        return result

    @queryset_manager
    def status(doc_cls, queryset):
        """
        Gives Collection status:
            * Start Date record startrecdate
            * End Date record
            * Num of record
        """

        numofrecord = queryset.count()
        if numofrecord == 0:
            startrecdate = None
            endrecdate = None
        else:
            startrecdate = queryset.order_by('fecha')[0].fecha
            endrecdate = queryset.order_by('-fecha')[0].fecha

        return {'startrecdate':startrecdate,
                'endrecdate':endrecdate,
                'numofrecord':numofrecord,}
    # def __init__(self):
    #     """
    #     """
    #     pass


class TecnologiasWeb(Document):
    """
    Manages "Energia Acumulados por tipo de generacion" as delivered by EnergiaMercadoDiarioParser Collection/Table
    """
    fecha = DateTimeField(unique=True)
    ProduccionyDemandaMIBEL = DictField()
    ProduccionyDemandaES = DictField()
    ProduccionyDemandaPT = DictField()

    @queryset_manager
    def lastdateindb(doc_cls, queryset):
        """
        index is automatic!
        """
        result = queryset.order_by('-fecha')[0].fecha
        return result

    @queryset_manager
    def numofrecords(doc_cls, queryset):
        """
        """
        result = queryset.count()
        return result

    @queryset_manager
    def status(doc_cls, queryset):
        """
        Gives Collection status:
            * Start Date record startrecdate
            * End Date record
            * Num of record
        """

        numofrecord = queryset.count()
        if numofrecord == 0:
            startrecdate = None
            endrecdate = None
        else:
            startrecdate = queryset.order_by('fecha')[0].fecha
            endrecdate = queryset.order_by('-fecha')[0].fecha

        return {'startrecdate':startrecdate,
                'endrecdate':endrecdate,
                'numofrecord':numofrecord,}

    # def __init__(self):
    #     """
    #     """
    #     pass

class StudyDataES(Document):
    """
    Manages omieStudyData Collection/Table
    This study data should handle missing data as defined.
    And also records per hour instead of per day

    > Note to developers and mongo users:
        Simple Average of prices:
            
        Weight Average of prices:
            
        Money Manage by NUCLEAR TECNOLOGY by each day:
            db.study_data_e_s.aggregate(
               [
                 { $project: { fecha: '$fecha',total: { $multiply: [ "$NUCLEAR", "$precio" ] } } }
               ]
            )
        Money manage by NUCLEAR TECNOLOGY since ever:
        db.study_data_e_s.aggregate(
           [
             { $project: {total: { $multiply: [ "$NUCLEAR", "$precio" ] } } },
             {
               $group:
                 {
                   _id : null,
                   totalAmount: { $sum: '$total' },
                   count: { $sum: 1 }
                 }
             }
           ]
        )
        Money manage by NUCLEAR TECNOLOGY with matching criteria:
        db.study_data_e_s.aggregate(
           [
             { $match : { hour : 4 } },
             { $project: {total: { $multiply: [ "$NUCLEAR", "$precio" ] } } },
             {
               $group: 
                 {
                   _id : null,
                   totalAmount: { $sum: '$total' },
                   count: { $sum: 1 }
                 }
             }
           ]
        )
        Money samething done grouping hours:
        db.study_data_e_s.aggregate([
            { $project: { hour: '$hour',total: { $multiply: [ "$NUCLEAR", "$precio" ] } } },
            { $group:   {_id : '$hour',totalAmount: { $sum: '$total' },count: { $sum: 1 }}
            }])
        Histogram of int part of all prices:
        db.study_data_e_s.aggregate([{ $project:{'count': { $subtract: ['$precio',{$mod: ['$precio',1] }]}}}, 
                                     { $group : { _id:'$count', count:{$sum:1} }},
                                     { $sort  : { _id: 1 }}])
        Can be combined with the hour to perform specialized Histograms of int part of all prices:

    """
    fecha = DateTimeField(unique=True) # Must at least include Hour!
    year = IntField()
    month = IntField()
    day = IntField()
    hour = IntField()
    # 
    precio = FloatField()
    # Tecnologias en el mercado:
    # RESUMEN_DE_PRODUCCION_ESPAÑA
    # TOTAL_HIDRAULICA
    # TOTAL_TERMICA
    # TOTAL_REGIMEN_ESPECIAL
    # TOTAL_IMPORTACION
    # TOTAL_GENERICAS
    # TOTAL_PRODUCCION
    # '50':'RESUMEN_DE_DEMANDA_ESPAÑA',
    # '51':'TOTAL_DEMANDA_NACIONAL_CLIENTES_(21+22+23)',
    # '52':'TOTAL_CONSUMO_BOMBEO_(24)',
    # '53':'TOTAL_EXPORTACIONES_(25+26+27+28+29)',
    # '54':'TOTAL_GENERICAS_(30+31)',
    # '59':'TOTAL_DEMANDA',
    #
    # HIDRAULICA_CONVENCIONAL = FloatField()
    # HIDRAULICA_BOMBEO_PURO = FloatField()
    # NUCLEAR = FloatField()
    # CARBON_NACIONAL = FloatField()
    # CARBON_IMPORTACION = FloatField()
    # CICLO_COMBINADO = FloatField()
    # FUEL_GAS = FloatField()
    # FUEL_GAS_PRIMA = FloatField()
    # REGIMEN_ESPECIAL_A_MERCADO = FloatField()
    # IMPORTACION_PORTUGAL = FloatField()
    # IMPORTACION_OTROS = FloatField()
    # TOTAL_HIDRAULICA = FloatField()
    # TOTAL_TERMICA = FloatField()
    # TOTAL_REGIMEN_ESPECIAL = FloatField()
    # TOTAL_GENERICAS = FloatField()
    # TOTAL_PRODUCCION = FloatField()
    # TOTAL_DEMANDA_NACIONAL_CLIENTES = FloatField()
    # TOTAL_CONSUMO_BOMBEO = FloatField()
    # TOTAL_EXPORTACIONES = FloatField()
    # TOTAL_GENERICAS = FloatField()
    # TOTAL_DEMANDA = FloatField()


class StudyDataMIBEL(Document):
    """Manages omieStudyDataForMIBEL Collection/Table:

    """
    fecha = DateTimeField(unique=True) # Must at least include Hour!
    # 
    precio = FloatField()
    # Tecnologias en el mercado:
    # '940':'RESUMEN_DE_PRODUCCION_MIBEL',
    P_TOTAL_HIDRAULICA = FloatField()
    P_TOTAL_TERMICA = FloatField()
    P_TOTAL_REGIMEN_ESPECIAL = FloatField()
    P_TOTAL_REGIMEN_ORDINARIO_CON_PRIMA = FloatField()
    P_TOTAL_IMPORTACION = FloatField()
    P_TOTAL_GENERICAS = FloatField()
    P_TOTAL_PRODUCCION_MIBEL = FloatField()
    # '950':'RESUMEN_DE_DEMANDA_MIBEL',
    D_TOTAL_DEMANDA_NACIONAL_CLIENTES = FloatField()
    D_TOTAL_CONSUMO_BOMBEO = FloatField()
    D_TOTAL_EXPORTACIONES = FloatField()
    D_TOTAL_GENERICAS = FloatField()
    D_TOTAL_DEMANDA_MIBEL = FloatField()

    @queryset_manager
    def lastdateindb(doc_cls, queryset):
        """
        index is automatic!
        """
        result = queryset.order_by('-fecha')[0].fecha
        return result

    @queryset_manager
    def numofrecords(doc_cls, queryset):
        """
        """
        result = queryset.count()
        return result


    @queryset_manager
    def status(doc_cls, queryset):
        """
        Gives Collection status:
            * Start Date record startrecdate
            * End Date record
            * Num of record
        """
        numofrecord = queryset.count()
        if numofrecord == 0:
            startrecdate = None
            endrecdate = None
        else:
            startrecdate = queryset.order_by('fecha')[0].fecha
            endrecdate = queryset.order_by('-fecha')[0].fecha

        return {'startrecdate':startrecdate,
                'endrecdate':endrecdate,
                'numofrecord':numofrecord,}
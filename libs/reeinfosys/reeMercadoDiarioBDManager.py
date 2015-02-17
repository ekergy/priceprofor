# -*- coding: utf-8 -*-
#
# This Module to handle db connections!
# reeMercadoDiario TecnologiasCBLWeb
#                  TecnologiasPBFWeb
#                  PreciosWeb
#                  PrevisionesWeb
#                  reeStudyData
#
# TODO: reeStudyData :: Collection Model:

from mongoengine import *


class StudyDataES(Document):
    """
    Manages omieStudyData Collection/Table
    This study data should handle missing data as defined.
    And also records per hour instead of per day.
    """
    fecha = DateTimeField(unique=False) # must include Hour in order to be unique!
    year = IntField()
    month = IntField()
    day = IntField()
    hour = IntField()
    # Tecnologias en el mercado:
    precio = FloatField()
    EnergiaGestionada = FloatField()
    PrevDemanda = FloatField()
    PrevEol = FloatField()
    NUCLEAR = FloatField()



class PrevDemandaWeb(Document):
    """
    Manages PrevDemandaWeb Collection/Table
    """
    fecha = DateTimeField(unique=True)
    PrevDemanda = ListField()

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


class PrevEolWeb(Document):
    """
    Manages PrevEolWeb Collection/Table
    """
    fecha = DateTimeField(unique=True)
    PrevEol = ListField()

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


class EnergiaGestionadaWeb(Document):
    """
    Manages EnergiaGestionadaWeb Collection/Table
    """
    fecha = DateTimeField(unique=True)
    EnergiaGestionada = ListField()

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



class TecnologiasPBFWeb(Document):
    """
    Manages TecnologiasPBFWeb Collection/Table
    """
    fecha = DateTimeField(unique=True)
    TecnologiasPBF = DictField()

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



class TecnologiasCBLWeb(Document):
    """
    Manages TecnologiasCBLWeb Collection/Table
    """
    fecha = DateTimeField(unique=True)
    TecnologiasCBL = DictField()

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

class PreciosWeb(Document):
    """
    Manages PreciosWeb as delivered by PreciosMercadoDiarioParser Collection/Table

    > Note to developers and mongo users:
        Check last document available:
            db.precios_web.find().sort({ fecha: -1 })
            "Comprehensive approach is"
            db.precios_web.find( { $query: {}, $orderby: { fecha : -1 } } )
        Get document by fecha:
            db.precios_web.find({ fecha: ISODate("2012-01-01 00:00:00.000Z") })
        Get documents between fechas:
            db.precios_web.find({fecha: {$gte: ISODate("2011-06-01 00:00:00.000Z"), $lte: ISODate("2012-06-03 00:00:00.000Z")} });

    """
    fecha = DateTimeField(unique=True)
    PreciosES = ListField()

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

    



# -*- coding: utf-8 -*-

from mongoengine import *

class MercadoDiarioMixEs(Document):
    """MercadoDiarioMix
    This class will manage data in the Mercado Diario Mix for Spain.

    It will use data from omie and ree in orther to get the most deaggregated information possible on the Market:
    Olny production is taking into account:

    Also it will try to manage data since the delivery date isn't always the same.

    Note to developers:
    Starting doing this using 2014-1-1 since we have full ree and omie data.

    Status field will determine witch data is available:
    status {ree:True,omie:True}

    Data is taken directly the Web Collections in the ree and omie databases not from study data.

    

    """
    fecha = DateTimeField(unique=True)
    status = DictField()
    precio = FloatField()
    HIDRAULICA = DictField()
    TERMICA = DictField()
    REGIMEN_ESPECIAL = DictField()
    IMPORTACION = DictField()
    GENERICAS = DictField()

    @queryset_manager
    def lastdateindb(doc_cls, queryset):
        """
        index is automatic!
        """
        result = queryset.order_by('-fecha')[0].fecha
        return result

class FullDeaggregatedDataEs(Document):
    """FullDeaggregatedDataEs
    
    """
    fecha = DateTimeField(unique=True)
    status = DictField()
    precio = FloatField()
    predictions = DictField()
    HIDRAULICA = DictField()
    TERMICA = DictField()
    REGIMEN_ESPECIAL = DictField()
    IMPORTACION = DictField()
    GENERICAS = DictField()
    

    @queryset_manager
    def lastdateindb(doc_cls, queryset):
        """
        index is automatic!
        """
        result = queryset.order_by('-fecha')[0].fecha
        return result
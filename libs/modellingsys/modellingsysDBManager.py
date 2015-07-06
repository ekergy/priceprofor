# -*- coding: utf-8 -*-
#
# This Module to handle db connections!
#

from mongoengine import *

class ModellingResults(Document):
    """
    Manages Modellingsys as delivered by ModellingResults Collections

    > Note to developers and mongo users:
        Check last document available:

    """

    meta = {'collection': 'ModellingResults'}
    
    dayahead = DateTimeField()
    baseset = ListField()
    model = DictField()
    errormodel = ListField()
    errorpredictions = ListField()
    predictions = DictField()
    
    @queryset_manager
    def lastdayaheadindb(doc_cls, queryset):
        """
        """
        result = queryset.order_by('-dayahead')[0]
        return result

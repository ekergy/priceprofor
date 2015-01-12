# -*- coding: utf-8 -*-
#!/usr/bin/env python

__author__ = ("Hugo M. Marrao Rodrigues")
__version__ = "0.0.0"
__revision__ = "alpha"

from flask import Blueprint

homepage = Blueprint('home_page', __name__)

@homepage.route('/', defaults={'page': 'index'})
@homepage.route('/<page>')
def homepagefunc(page):
    """
    homepage for homepage!
    """
    page = 'null' if page is None else str(page)
    return "homepage"+page+"end"
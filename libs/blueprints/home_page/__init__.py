# -*- coding: utf-8 -*-
#!/usr/bin/env python

__author__ = ("Hugo M. Marrao Rodrigues")
__version__ = "0.0.0"
__revision__ = "alpha"

from flask import Blueprint, render_template, url_for
from flask.ext.assets import Bundle

homepage = Blueprint('home_page', __name__, template_folder="templates",static_folder="static",url_prefix='/ver2')

# homepage_js = Bundle('static/js/bootstrap.min.js')

#@homepage.route('/', defaults={'page': 'index'})
@homepage.route('/<page>')
def homepagefunc(page):
    """
    homepage for homepage!
    """
    page = 'null' if page is None else str(page)
    return "homepage"+page+"end"+url_for('static', filename='css/bootstrap.min.css')

@homepage.route('/verver/verver')
def index_html():
    """
    homepage for homepage!
    """
    return homepage.send_static_file('index.html')

# -*- coding: utf-8 -*-
"""PriceProfor: MIBEL data explorer and Modelling.

PriceProfor is a project developed to explore MIBEL data and perform Modelling
and reports. This application is build with mongodb and python-flask app 
server with blueprints modular implementation:

"""

__author__ = ("Hugo M. Marrao Rodrigues")
__version__ = "0.0.0"
__revision__ = "alpha"


from flask import Flask, url_for, redirect
# from flask.ext.assets import Environment
app = Flask(__name__, static_folder='static', static_url_path='')
# importing blueprints:
from omieinfosys.omieBlueprintAPI import omieMercadoDiario
app.register_blueprint(omieMercadoDiario)

# import for old controllers:
from json import dumps

def has_no_empty_params(rule):
    """
    Function to help to build site Map and all links.
    """    
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@app.route("/site-map")
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint)
            links.append((url, rule.endpoint))
    return str(links)

@app.route("/all-links")
def all_links():
    links = []
    for rule in app.url_map.iter_rules():
        if has_no_empty_params(rule): #len(rule.defaults) >= len(rule.arguments):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    return str(links)

@app.route("/")
# @app.route("/index")
# @app.route("/index/")
# @app.route("/index.html")
# @app.route("/home")
# @app.route("/home/")
# @app.route("/home.html")
def roothomeindex():
    """
    Default Project presentation page.
    """
    # print url_for('static', filename="index.html")
    return redirect(url_for('static', filename="index.html"))

@app.route("/PreciosHorariosUltimoDia")
def PreciosHorariosUltimoDia():
    """This controller comes from old priceprofor:
    The information is 
    PrecioMedio
    PreciosPromedio
    PreciosHorario
    PrecioMaximo
    PrecioMinimo
    """
    result = {'PrecioMedio':list(),
              'PreciosPromedio':list(),
              'PreciosHorario':list(),
              'PrecioMaximo':list(),
              'PrecioMinimo':list()}

    return dumps(result)
    




if __name__ == "__main__":
    app.run(debug=True)

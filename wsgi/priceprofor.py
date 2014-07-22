# -*- coding: utf-8 -*-
'''
Created on 13/05/2014
@author: david, hector, marrao, mundi
'''

from bottle import route

# framework:
from bottle import default_app

# controllers:
from controllers import resources
from controllers import priceprofor_graficas
from controllers import priceprofor_single_plots
from controllers import sme_mde_viz
from controllers import priceprofor_restfulAPI
# from controllers import priceprofor_precioshorarios

from bottle import TEMPLATE_PATH
#TEMPLATE_PATH.append(os.path.join(os.environ['OPENSHIFT_HOMEDIR'], 
#    'runtime/repo/wsgi/views/'))

# Get APP root in system:
from os import path as ospath
from os import environ as osenviron

# get sys to add proper template paths
import sys

try:
    root_app=ospath.join(osenviron['OPENSHIFT_REPO_DIR'])
except:
    root_app=ospath.join(sys.path[0])
finally:
    TEMPLATE_PATH.append(ospath.join(root_app, 'wsgi', 'views', 'templates'))
    TEMPLATE_PATH.append(ospath.join(root_app, 'wsgi', 'views', 'templates','priceprofor_graficas'))
    TEMPLATE_PATH.append(ospath.join(root_app, 'wsgi', 'views', 'templates','priceprofor_restfulAPI'))

CONN_URI=None

application = default_app()




from bottle import get, static_file

import sys
from os import path as ospath
from os import environ as osenviron
try:
    root_app=ospath.join(osenviron['OPENSHIFT_REPO_DIR'])
except:
    root_app=ospath.join(sys.path[0])
finally:
    ospath.join(root_app, 'resources')

@get("/resources/<filepath:path>")
def serve_static(filepath):
    return static_file(str('/'+filepath), root = ospath.join(root_app, 'wsgi', 'static', 'resources'))

# setting the static serve files methods:
# Static Routes
@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    '''
    docstring
    '''
    return static_file(filename, root=ospath.join(root_app, 'wsgi', 'static', 'resources', 'js'))

@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    '''
    docstring
    '''
    return static_file(filename, root=ospath.join(root_app,'wsgi','static', 'resources','css'))

@get('/img/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    '''
    docstring
    '''
    return static_file(filename, root=ospath.join(root_app,'wsgi','static', 'resources','img'))

@get('/fonts/<filename:re:.*\.(eot|ttf|woff|svg)>')
def fonts(filename):
    '''
    '''
    return static_file(filename, root=ospath.join(root_app,'wsgi','static', 'resources','fonts'))

@get('/d3/<filename>')
def getd3(filename):
    '''
    '''
    return static_file(filename, root=ospath.join(root_app,'wsgi','static', 'resources','d3'))

@get("/uikit/<filepath:path>")
def uikitresources(filepath):
    """
    Controller for the uikit framework.
    """
    return static_file(str('/'+filepath), root = ospath.join(root_app, 'wsgi', 'static', 'resources','uikit'))
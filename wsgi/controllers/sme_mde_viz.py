from bottle import route, template

@route('/MercadoDiarioElectricidad')
def mde_viz():
    #assume you have a login page with two fields:
    #"email" and "password" and submit button
    return template('full_mde_data')

@route('/Historico2011')
def mde_viz_2011():
    #assume you have a login page with two fields:
    #"email" and "password" and submit button
    return template('datos_mde_2011')

@route('/Historico2012')
def mde_viz_2012():
    #assume you have a login page with two fields:
    #"email" and "password" and submit button
    return template('datos_mde_2012')

@route('/Historico2013')
def mde_viz_2013():
    #assume you have a login page with two fields:
    #"email" and "password" and submit button
    return template('datos_mde_2013')

@route('/Historico2014')
def mde_viz_2014():
    #assume you have a login page with two fields:
    #"email" and "password" and submit button
    return template('datos_mde_2014')


@route('/Historico2011Alt')
def mde_viz_2011_alt():
    #assume you have a login page with two fields:
    #"email" and "password" and submit button
    return template('datos_mde_2011_alt')

@route('/ValoresDeUnDia', method='GET')
def valoresmde_dia():
    #assume you have a login page with two fields:
    #"email" and "password" and submit button
    return template('datos_mde_2014')

@route('/ValoresDeUnDia', method='POST')
def valoresmde_dia():
    #assume you have a login page with two fields:
    #"email" and "password" and submit button
    return template('datos_mde_2014')
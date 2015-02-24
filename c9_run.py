# -*- coding: utf-8 -*-
"""

Run project with only the static_folder so one can perform web edit.

"""
# system imports
import os

static_folder = os.path.join('wsgi','priceprofor','static')


from flask import Flask, url_for, redirect
# from flask.ext.assets import Environment
app = Flask(__name__, static_folder=static_folder, static_url_path='')


@app.route("/")
def roothomeindex():
    """
    Default Project presentation page.
    """
    # print url_for('static', filename="index.html")
    return redirect(url_for('static', filename="index.html"))


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080,debug=True)
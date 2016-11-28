import os,sqlite3
from flask import request,session,Flask,render_template,make_response, \
    url_for,redirect,abort,g,flash

app = Flask(__name__)
databaseurl = app.config.from_envvar("FLASKR_SETTINGS",silent=True)
sql3 = sqlite3.connect(databaseurl)

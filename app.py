import os
import random
import string

import httplib2
import requests
from flask import request, json, make_response, Response, send_from_directory
from flask_cors import cross_origin
from flask_bootstrap import Bootstrap

from Models import CatalogCategory, CatalogItem, User
from app_init import app, db
from authentication import authentication_blueprint
from item_catalog_api import item_catalog_api_blueprint
from item_catalog_frontend import item_catalog_frontend_blueprint, setAppObject

app.config['SESSION_TYPE'] = 'SESSION_SQLALCHEMY'
app.secret_key = os.urandom(24)

# register the three blueprints for the authentication,
# the json endpoint and the flask/jinja frontend
app.register_blueprint(authentication_blueprint)
app.register_blueprint(item_catalog_api_blueprint)
app.register_blueprint(item_catalog_frontend_blueprint)

FLASK_APP = app
#Bootstrap(app)
setAppObject(app)
db.create_all()

if __name__ == '__main__':
#    db.create_all()
    app.debug = True
    app.run(host= '0.0.0.0')

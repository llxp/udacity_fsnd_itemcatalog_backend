# system/framework includes
# --------------------------------
from flask import Flask, json
from flask import jsonify
from flask import request
from flask import url_for
from flask import abort
from flask import g
# --------------------------------
# --------------------------------
from flask_httpauth import HTTPBasicAuth
#--------------------------------
from flask_jsontools import DynamicJSONEncoder
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# --------------------------------
from flask_cors import CORS, cross_origin
from Models import Category


#global flask object
app = Flask(__name__)
CORS(app)
app.json_encoder = DynamicJSONEncoder

#global flask authentication object
auth = HTTPBasicAuth()

#init db session object
engine = create_engine('sqlite:///users.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user/login')
def login():
    return 'login'


@app.route('/user/logout')
def logout():
    return 'logout'


@app.route('/user/gconnect')
def gconnect():
    return 'gconnect'


@app.route('/user/register')
def registerUser():
    return 'user registration'


@app.route('/categories')
@cross_origin()  # put there for debugging purposes
def categories():
    category1 = Category()
    category1.category = "Category1"
    category1.path = "/categories/1"

    category2 = Category()
    category2.category = "Category2"
    category2.path = "/categories/2"

    return json.dumps([category1, category2])


if __name__ == '__main__':
    app.run()

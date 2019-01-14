import os

from flask import Flask
from flask_cors import CORS
from flask_jsontools import DynamicJSONEncoder, JsonSerializableBase
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_session import SqlAlchemySessionInterface

# global flask object
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///itemcatalog.db'
db = SQLAlchemy(app, model_class=JsonSerializableBase)
CORS(app)
app.json_encoder = DynamicJSONEncoder
app.secret_key = os.urandom(24)
SqlAlchemySessionInterface(
    app=app,
    db=db,
    table='session',
    permanent=True,
    key_prefix='session_')

APPLICATION_NAME = "Item Catalog"

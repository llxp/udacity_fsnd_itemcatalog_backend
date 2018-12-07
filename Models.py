from flask import Flask
from flask_jsontools import JsonSerializableBase
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

Base = declarative_base(cls=(JsonSerializableBase,))


class Category(Base):
    __tablename__ = "Category"
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(255), unique=False, nullable=False)
    path = db.Column(db.String(255), unique=True, nullable=False)

class User(Base):
    __tablename__ = "User"
    id = db.column(db.Integer, primary_key=True)
    email = db.column(db.String(255), unique=True, nullable=False)
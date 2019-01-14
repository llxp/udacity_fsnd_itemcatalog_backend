from flask import Flask
from flask_jsontools import JsonSerializableBase
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy import DateTime
from sqlalchemy.ext.declarative import declarative_base

import app_init

app_init.db.create_all()


class CatalogCategory(app_init.db.Model):
    __tablename__: str = "Category"
    id: int = Column(Integer, primary_key=True)
    category: str = Column(String(255), unique=False, nullable=False)


class CatalogItem(app_init.db.Model):
    __tablename__: str = "CatalogItem"
    id: int = Column(Integer, primary_key=True)
    title: str = Column(String)
    description: str = Column(String)
    lastAccessed = Column(DateTime)
    category: int = Column(Integer, ForeignKey("Category.id"), nullable=False)


class User(app_init.db.Model):
    __tablename__: str = "User"
    id: int = Column(Integer, primary_key=True)
    email: str = Column(String(1024), unique=True, nullable=False)
    username: str = Column(String(32), index=True)
    picture: str = Column(String)
    userinfo_url: str = Column(String)

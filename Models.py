from flask import Flask
from flask_jsontools import JsonSerializableBase
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base

import app_init

# Base = declarative_base(cls=(JsonSerializableBase,))
app_init.db.create_all()

class CatalogCategory(app_init.db.Model):
    __tablename__: str = "Category"
    id: int = Column(Integer, primary_key=True)
    category: str = Column(String(255), unique=False, nullable=False)


class User(app_init.db.Model):
    __tablename__: str = "User"
    id: int = Column(Integer, primary_key=True)
    email: str = Column(String(1024), unique=True, nullable=False)
    username: str = Column(String(32), index=True)
    picture: str = Column(String)
    userinfo_url: str = Column(String)


class CatalogItem(app_init.db.Model):
    __tablename__: str = "CatalogItem"
    id: int = Column(Integer, primary_key=True)
    title: str = Column(String)
    description: str = Column(String)
    lastAccessed = Column(DateTime)
    category: int = Column(Integer, ForeignKey("Category.id"), nullable=False)


"""class SessionToken(db.Model):
    __tablename__: str = "SessionToken"
    id: int = Column(Integer, primary_key=True)
    token: str = Column(String(255), nullable=False)
    is_valid: bool = Column(db.Boolean(), nullable=False, default=True)
    created = Column(db.DateTime(), nullable=False, default=db.DateTime.utcnow)
    logged_in: bool = Column(db.Boolean(), nullable=False, default=False)
"""

# engine = create_engine('sqlite:///itemcatalog.db')


# Base.metadata.create_all(engine)


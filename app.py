import os
import random
import string

import httplib2
import requests
from flask import request, json, make_response, Response, send_from_directory
from flask_cors import cross_origin

from Models import CatalogCategory, CatalogItem, User

from app_init import app, db

# init db session object
# engine = create_engine('sqlite:///itemcatalog.db')
# Base.metadata.bind = engine
# DBSession = sessionmaker(bind=engine)
# session = scoped_session(DBSession())
from authentication import authentication_blueprint

db.create_all()

app.config['SESSION_TYPE'] = 'SESSION_SQLALCHEMY'
app.secret_key = os.urandom(24)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog"

session_tokens = []

app.register_blueprint(authentication_blueprint)

@app.route('/')
def hello_world():
    return 'Hello World!'


#@app.route("/<path:path>")
#def root(path):
#    print(os.path.join(os.getcwd(), "..\\frontend\\dist\\ItemCatalog\\index.html"), path)
#    return send_from_directory("C:\\Users\\llxp\\source\\repos\\Udacity_Project_ItemCatalog\\frontend\\dist\\ItemCatalog\\index.html", path)


@app.route('/api/catalog/categories')
@cross_origin()  # put there for debugging purposes
def categories():
    catalogCategories = CatalogCategory.query.all()
    category1 = CatalogCategory()
    category1.id = 1
    category1.category = "Category1"

    category2 = CatalogCategory()
    category2.id = 2
    category2.category = "Category2"

    print("/categories")
    return json.dumps(catalogCategories)


@app.route('/api/catalog/items/<int:category_id>')
@cross_origin()  # put there for debugging purposes
def items(category_id):
    current_items = CatalogItem.query.filter_by(category=category_id).all()
    if current_items is None:
        return "[]"
    return json.dumps(current_items)


@app.route('/api/catalog/item/<int:item_id>')
@cross_origin()  # put there for debugging purposes
def item(item_id):
    current_item = CatalogItem.query.filter_by(id=item_id).first()
    if current_item is None:
        return "{}"
    return json.dumps(current_item)


def check_login(token):
    return True


@app.route('/api/catalog/item', methods=['POST'])
@cross_origin()  # put there for debugging purposes
def add_item():
    token = request.form.get('token')
    title = request.form.get('title')
    description = request.form.get('description')
    category_id = request.form.get('category_id')
    if (
            token is not None and
            title is not None and
            description is not None and
            category_id is not None):
                if check_login(token) is True:
                    new_item = CatalogItem()
                    new_item.title = title
                    new_item.description = description
                    new_item.category = category_id
                    db.session.add(new_item)


FLASK_APP = app
if __name__ == '__main__':
    db.create_all()
    app.debug = True
    app.run()

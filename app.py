import os
import random
import string

import httplib2
import requests
from flask import request, json, make_response, Response, send_from_directory
from flask_cors import cross_origin

from Models import CatalogCategory, CatalogItem, User
from app_init import app, db
from authentication import authentication_blueprint, check_login

app.config['SESSION_TYPE'] = 'SESSION_SQLALCHEMY'
app.secret_key = os.urandom(24)

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


#insert new item
@app.route('/api/catalog/item', methods=['POST'])
@cross_origin()  # put there for debugging purposes
def add_item():
    session_token = request.args.get('session_token')
    if check_login(session_token) is True:
        title = request.form.get('title')
        description = request.form.get('description')
        category_id = request.form.get('category_id')
        if (session_token is not None and
            title is not None and
            description is not None and
            category_id is not None):
                new_item = CatalogItem()
                new_item.title = title
                new_item.description = description
                new_item.category = category_id
                db.session.add(new_item)
                db.session.commit()
                response = make_response(json.dumps('Item successfully added'), 200)
                response.headers['Content-Type'] = 'application/json'
                return response
        response = make_response(json.dumps('Item malformed'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    response = make_response(json.dumps('user not authorized'), 403)
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/api/catalog/item', methods=['PUT'])
@cross_origin()  # put there for debugging purposes
def update_item():
    session_token = request.args.get('session_token')
    if check_login(session_token) is True:
        title = request.form.get('title')
        description = request.form.get('description')
        category_id = request.form.get('category_id')
        item_id = request.form.get('item_id')
        found_item = CatalogItem.query.filter_by(id=item_id)
        if found_item is not None:
            found_item.title = title
            found_item.description = description
            found_item.category = category_id
            db.session.commit()
            response = make_response(json.dumps('Category successfully updated'), 200)
            response.headers['Content-Type'] = 'application/json'
            return response
        response = make_response(json.dumps('Item malformed'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    response = make_response(json.dumps('user not authorized'), 403)
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/api/catalog/category', methods=['POST'])
@cross_origin()
def add_category():
    session_token = request.args.get('session_token')
    if check_login(session_token) is True:
        category = request.form.get('category')
        if category is not None:
            new_category = CatalogCategory()
            new_category.category = category
            db.session.add(new_category)
            db.session.commit()
            response = make_response(json.dumps('Category successfully added'), 200)
            response.headers['Content-Type'] = 'application/json'
            return response
        response = make_response(json.dumps('Category malformed'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    response = make_response(json.dumps('user not authorized'), 403)
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/api/catalog/category', methods=['PUT'])
@cross_origin()
def update_category():
    session_token = request.args.get('session_token')
    if check_login(session_token) is True:
        category = request.form.get('category')
        category_id = request.form.get('category_id')
        found_category = CatalogCategory.query.filter_by(id=category_id)
        if found_category is not None:
            found_category.category = category
            db.session.commit()
            response = make_response(json.dumps('Category successfully updated'), 200)
            response.headers['Content-Type'] = 'application/json'
            return response
        response = make_response(json.dumps('Category not found'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    response = make_response(json.dumps('user not authorized'), 403)
    response.headers['Content-Type'] = 'application/json'
    return response


FLASK_APP = app
if __name__ == '__main__':
    db.create_all()
    app.debug = True
    app.run()

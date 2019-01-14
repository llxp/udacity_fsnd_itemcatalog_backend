from flask import json, request, make_response, flash, Blueprint, Response
from flask_cors import cross_origin

from Models import CatalogCategory, CatalogItem, User
from authentication import check_login
from app_init import app, db

item_catalog_api_blueprint = Blueprint(
    'item_catalog_api',
    __name__,
    template_folder='templates')


@item_catalog_api_blueprint.route('/api/catalog/categories', methods=['GET'])
@cross_origin()
def categories():
    catalogCategories = CatalogCategory.query.all()
    if catalogCategories is None:
        return "[]"
    return json.dumps(catalogCategories)


@item_catalog_api_blueprint.route(
    '/api/catalog/category/<int:category_id>',
    methods=['GET'])
@cross_origin()
def category(category_id: int):
    catalogCategory = CatalogCategory.query.filter_by(id=category_id)
    if catalogCategory is None:
        return "{}"
    return json.dumps(catalogCategory)


@item_catalog_api_blueprint.route('/api/catalog/category', methods=['POST'])
@cross_origin()
def add_category():
    session_token = request.args.get('session_token')
    if check_login(session_token) is True:
        # session is authenticated
        category = request.form.get('category')
        categoryLen = len(category)
        if (category is not None and categoryLen > 0):
                new_category = CatalogCategory()
                new_category.category = category
                db.session.add(new_category)
                db.session.commit()
                response = make_response(
                    json.dumps('Category successfully added'), 200)
                response.headers['Content-Type'] = 'application/json'
                return response
        response = make_response(
            json.dumps('Category malformed'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    response = make_response(
        json.dumps('user not authorized'), 403)
    response.headers['Content-Type'] = 'application/json'
    return response


@item_catalog_api_blueprint.route(
    '/api/catalog/category/<int:category_id>',
    methods=['PUT'])
@cross_origin()
def update_category(category_id: int):
    session_token = request.args.get('session_token')
    if check_login(session_token) is True:
        # session is authenticated
        category = request.form.get('category')
        categoryLen = len(category)
        found_category = CatalogCategory.query.filter_by(
            id=category_id).first()
        if (found_category is not None and
                categoryLen > 0):
            found_category.category = category
            db.session.commit()
            response = make_response(
                json.dumps('Category successfully updated'), 200)
            response.headers['Content-Type'] = 'application/json'
            return response
        response = make_response(
            json.dumps('Category not found'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    response = make_response(
        json.dumps('user not authorized'), 403)
    response.headers['Content-Type'] = 'application/json'
    return response


@item_catalog_api_blueprint.route(
    '/api/catalog/category/<int:category_id>',
    methods=['DELETE'])
@cross_origin()
def delete_category(category_id: int):
    session_token = request.args.get('session_token')
    if check_login(session_token) is True:
        # session is authenticated
        found_category = CatalogCategory.query.filter_by(
            id=category_id).first()
        if found_category is not None:
            db.session.delete(found_category)
            db.session.commit()
            response = make_response(
                json.dumps('Category successfully deleted'), 200)
            response.headers['Content-Type'] = 'application/json'
            return response
        response = make_response(
            json.dumps('Category not found'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    response = make_response(
        json.dumps('user not authorized'), 403)
    response.headers['Content-Type'] = 'application/json'
    return response


@item_catalog_api_blueprint.route(
    '/api/catalog/items/<int:category_id>',
    methods=['GET'])
@cross_origin()
def items(category_id: int):
    current_items = CatalogItem.query.filter_by(category=category_id).all()
    if current_items is None:
        return "[]"
    return json.dumps(current_items)


@item_catalog_api_blueprint.route(
    '/api/catalog/item/<int:item_id>',
    methods=['GET'])
@cross_origin()
def item(item_id: int):
    current_item = CatalogItem.query.filter_by(id=item_id).first()
    if current_item is None:
        return "{}"
    return json.dumps(current_item)


# function for adding a new item to the catalog
@item_catalog_api_blueprint.route('/api/catalog/item', methods=['POST'])
@cross_origin()
def add_item():
    session_token = request.args.get('session_token')
    if check_login(session_token) is True:
        # session is authenticated
        title = request.form.get('title')
        description = request.form.get('description')
        category_id = request.form.get('category_id')
        titleLen = len(title)
        descriptionLen = len(description)
        if (title is not None and
                description is not None and
                category_id is not None and
                titleLen > 0 and
                descriptionLen > 0):
                new_item = CatalogItem()
                new_item.title = title
                new_item.description = description
                new_item.category = category_id
                db.session.add(new_item)
                db.session.commit()
                response = make_response(
                    json.dumps('Item successfully added'), 200)
                response.headers['Content-Type'] = 'application/json'
                return response
        response = make_response(
            json.dumps('Item malformed'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    response = make_response(
        json.dumps('user not authorized'), 403)
    response.headers['Content-Type'] = 'application/json'
    return response


@item_catalog_api_blueprint.route(
    '/api/catalog/item/<int:item_id>',
    methods=['DELETE'])
@cross_origin()
def delete_item(item_id: int):
    session_token = request.args.get('session_token')
    if check_login(session_token) is True:
        # session is authenticated
        found_item = CatalogItem.query.filter_by(id=item_id).first()
        if found_item is not None:
            db.session.delete(found_item)
            db.session.commit()
            response = make_response(
                json.dumps('Item successfully removed'), 200)
            response.headers['Content-Type'] = 'application/json'
            return response
        response = make_response(
            json.dumps('Item not found'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    response = make_response(
        json.dumps('user not authorized'), 403)
    response.headers['Content-Type'] = 'application/json'
    return response


@item_catalog_api_blueprint.route(
    '/api/catalog/item/<int:item_id>',
    methods=['PUT'])
@cross_origin()
def update_item(item_id: int):
    session_token = request.args.get('session_token')
    if check_login(session_token) is True:
        # session is authenticated
        title = request.form.get('title')
        description = request.form.get('description')
        category_id = request.form.get('category_id')
        titleLen = len(title)
        descriptionLen = len(description)
        found_item: CatalogItem = CatalogItem.query.filter_by(
            id=item_id).first()
        if (found_item is not None and
                titleLen > 0 and
                descriptionLen > 0):
            found_item.title = title
            found_item.description = description
            found_item.category = category_id
            db.session.commit()
            response = make_response(
                json.dumps('Category successfully updated'), 200)
            response.headers['Content-Type'] = 'application/json'
            return response
        response = make_response(
            json.dumps('Item malformed'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    response = make_response(
        json.dumps('user not authorized'), 403)
    response.headers['Content-Type'] = 'application/json'
    return response


@item_catalog_api_blueprint.route(
    '/api/catalog/search_item/<string:search_text>',
    methods=['GET'])
@cross_origin()
def search_item(search_text: str):
    foundItems = db.session.query(CatalogItem).filter(
        CatalogItem.title.like("%"+search_text+"%")).all()
    if foundItems is not None:
        return make_response(json.dumps(foundItems))
    return make_response(json.dumps([]))

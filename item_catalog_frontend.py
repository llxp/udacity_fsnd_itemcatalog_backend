from flask import json, request, make_response
from flask import flash, Blueprint, Response
from flask import render_template, redirect, url_for
from flask_cors import cross_origin
from flask_bootstrap import Bootstrap
import sys
import os
import random
import string
import httplib2 as httplib2
import requests
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
from flask import session as login_session

from Models import CatalogCategory, CatalogItem, User
from login_sesssion import LoginSessionItem, LoginSession
from authentication import check_login, get_new_token, get_session_object
from authentication import delete_session_object, CLIENT_ID, create_user
from authentication import generate_random_string, add_session_object
from constants import REDIRECT_URI_FLASK

dir_path = os.path.dirname(os.path.realpath(__file__))

item_catalog_frontend_blueprint = Blueprint(
    'item_catalog_frontend',
    __name__,
    template_folder='templates')


def setAppObject(app):
    Bootstrap(app)


# this functions shows the startpage withits categories
@item_catalog_frontend_blueprint.route('/', methods=['GET'])
def index():
    catalogCategories = CatalogCategory.query.all()
    current_items = CatalogItem.query.all()
    if login_session.get('state') is None:
        # render the start page without any special permissions showing
        return render_template(
            'index.html', categories=catalogCategories, items=current_items)
    else:
        session_token: str = login_session.get('state')
        if check_login(session_token):
            # render the start page with the login flag set to true
            # # and a provided session object
            return render_template(
                'index.html',
                categories=catalogCategories,
                items=current_items,
                success=True,
                session=get_session_object(session_token))
        else:
            # render the start page without any special permissions showing
            return render_template(
                'index.html',
                categories=catalogCategories,
                items=current_items)


# this functions shows the items in a category when clicked on a category
@item_catalog_frontend_blueprint.route('/catalog/category/<int:category_id>')
def category(category_id: int):
    catalogCategories = CatalogCategory.query.all()
    current_items = CatalogItem.query.filter_by(category=category_id).all()
    if CatalogCategory.query.filter_by(id=category_id).first() is None:
        # show the startpage without any special permissions
        # and an error message showing, that the category was not found
        errorMessage = ('The selected category was not' +
                        'found or is no longer valid.')
        return render_template(
            'index.html',
            error_message=errorMessage,
            categories=catalogCategories,
            items=current_items)
    if login_session.get('state') is None:
        # render the start page without any special permissions showing
        # and a selected category
        return render_template(
            'index.html',
            categories=catalogCategories,
            selectedCategory=category_id,
            items=current_items)
    else:
        session_token: str = login_session.get('state')
        if check_login(session_token):
            # render the start page with the login flag set to true
            # and a provided session object
            # and a selected category
            return render_template(
                'index.html',
                categories=catalogCategories,
                selectedCategory=category_id,
                items=current_items,
                success=True,
                session=get_session_object(session_token))
        else:
            # render the start page without any special permissions showing
            # and a selected category
            return render_template(
                'index.html',
                categories=catalogCategories,
                selectedCategory=category_id,
                items=current_items)


# this function shows the content of an item
@item_catalog_frontend_blueprint.route(
    '/catalog/category/<int:category_id>/item/<int:item_id>')
def item(category_id: int, item_id: int):
    catalogCategories = CatalogCategory.query.all()
    current_items = CatalogItem.query.filter_by(category=category_id).all()
    if CatalogCategory.query.filter_by(id=category_id).first() is None:
        # show the startpage without any special permissions
        # and an error message showing, that the category was not found
        return render_template(
            'index.html',
            error_message=(
                'The selected category was not ' +
                'found or is no longer valid.'),
            categories=catalogCategories,
            items=current_items)
    if CatalogItem.query.filter_by(id=item_id).first() is None:
        # show the startpage without any special permissions
        # and an error message showing, that the item was not found
        return render_template(
            'index.html',
            error_message=(
                'The item was not found ' +
                'or is no longer valid.'),
            categories=catalogCategories,
            selectedCategory=category_id,
            items=current_items)
    if login_session.get('state') is None:
        # show the start page with a selected item showing,
        # but without any special permissions displayed
        return render_template(
            'index.html',
            categories=catalogCategories,
            selectedCategory=category_id,
            items=current_items,
            selectedItem=item_id)
    else:
        session_token: str = login_session.get('state')
        if check_login(session_token):
            # render the start page with the login flag set to true
            # and a provided session object
            # and a selected category
            # and a selected item
            return render_template(
                'index.html',
                categories=catalogCategories,
                selectedCategory=category_id,
                items=current_items,
                selectedItem=item_id,
                success=True,
                session=get_session_object(session_token))
        else:
            # show the start page with a selected item showing,
            # but without any special permissions displayed
            return render_template(
                'index.html',
                categories=catalogCategories,
                selectedCategory=category_id,
                items=current_items,
                selectedItem=item_id)


# this functions shows the login page
@item_catalog_frontend_blueprint.route('/user/login', methods=['GET'])
def login():
    if login_session.get('state') is None:
        session_token: str = generate_random_string()
        login_session['state'] = session_token
        # display the default login page
        return render_template('login.html', state=session_token)
    else:
        session_token: str = login_session.get('state')
        if check_login(session_token):
            # the user is already logged in,
            # so displaying then login page with current login information
            return render_template(
                'login.html',
                state=session_token,
                success=True,
                session=get_session_object(session_token))
        else:
            # display the default login page
            return render_template('login.html', state=session_token)


# this function is largely copied from the project.py file
# from the udacity github repository but changed to the needs of this project
# it handles the authorization using a google account
# this is the version to handle authorization request
# coming directly from the google redirect from the flask/jinja frontend
@item_catalog_frontend_blueprint.route('/user/gconnect', methods=['GET'])
def gconnect():
    session_token = request.args.get('state')
    # Obtain authorization code
    code = request.args.get('code')

    current_session_token = login_session.get('state')
    # Validate state token
    if (
        current_session_token is None and
            current_session_token == session_token):
        # state token invalid
        return render_template(
            'login.html',
            state=session_token,
            error="Invalid token state")

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets(dir_path + '/client_secrets.json', scope=[
            'https://www.googleapis.com/auth/plus.me',
            'email',
            'openid',
            'https://www.googleapis.com/auth/plus.login'])
        oauth_flow.redirect_uri = REDIRECT_URI_FLASK  # 'http://localhost:5000/user/gconnect'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError as e:
        print('error: ' + str(e))
        return render_template(
            'login.html',
            state=session_token,
            error="Failed to upgrade the authorization code.")

    # Check that the access token is valid.
    access_token: str = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        return render_template(
            'login.html',
            state=session_token,
            error=result.get('error'))

    # Verify that the access token is used for the intended user.
    gplus_id: str = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        return render_template(
            'login.html',
            state=session_token,
            error="Token's user ID doesn't match given user ID.")

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        return render_template(
            'login.html',
            state=session_token,
            error="Token's client ID does not match app's.")

    stored_access_token: str = get_session_object(login_session.get('state'))
    stored_gplus_id: str = get_session_object(login_session.get('state'))
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        # user already connected
        # redirect to the login page again to show the logged in user
        return redirect(url_for('item_catalog_frontend.login'))

    # Store the access token in the session for later use.
    current_session: LoginSessionItem = LoginSessionItem()
    current_session.access_token = credentials.access_token
    current_session.gplus_id = gplus_id
    current_session.session_token = login_session.get('state')

    # Get user info
    userinfo_url: str = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    current_session.username = data['name']
    current_session.picture = data['picture']
    current_session.email = data['email']
    current_session.userinfo_url = userinfo_url

    create_user(userinfo_url,
                current_session.email,
                current_session.picture,
                current_session.username)

    current_session.logged_in = True

    add_session_object(current_session)

    # redirect to the login page again to show the logged in user
    return redirect(url_for('item_catalog_frontend.login'))

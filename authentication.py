import os

import httplib2 as httplib2
import requests
from flask import json, request, make_response, flash, Blueprint, Response
from flask_cors import cross_origin
import string
import random
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from flask_sqlalchemy import xrange
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError

from app_init import app, db
from login_sesssion import LoginSession, LoginSessionItem
from Models import User


app.config['SESSION_TYPE'] = 'SESSION_SQLALCHEMY'
SESSION_TYPE = 'SESSION_SQLALCHEMY'

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog"

authentication_blueprint = Blueprint(
    'authentication',
    __name__,
    template_folder='templates')

# create global login session for storing user information at runtime
# used to be compatible with angularJS
# (cookies are getting deleted at page reload ==> no session)
login_session: LoginSession = LoginSession()


# these functions are used for accessing the session from the flask frontend
# ----------------------------------------------------------------
def get_session_object(session_token: str):
    return login_session[session_token]


def delete_session_object(session_token: str):
    del login_session[session_token]


def generate_random_string():
    return ''.join(random.choice(string.ascii_uppercase + string.digits)
                   for x in xrange(32))


def add_session_object(session_object: LoginSessionItem):
    login_session[session_object.session_token] = session_object


def get_new_token():
    session_token: str = generate_random_string()
    login_session[session_token] = LoginSessionItem
    login_session[session_token].session_token = session_token
    return session_token


def check_login(session_token):
    current_session: LoginSessionItem = login_session[session_token]
    if current_session is not None:
        return current_session.logged_in
    return False
# ----------------------------------------------------------------


# create an anti-forgery token
@authentication_blueprint.route('/api/user/new_session')
@cross_origin()
def new_session():
    session_token: str = get_new_token()
    response = Response(json.dumps(session_token))
    return response  # json.dumps(new_session_token)


# function to create a new user in the database
def create_user(userinfo_url, email, picture, username):
    existing_user: User = User.query.filter_by(username=username).first()
    if existing_user is None:
        new_user: User = User()
        new_user.email = email
        new_user.picture = picture
        new_user.username = username
        new_user.userinfo_url = userinfo_url
        db.session.add(new_user)
        db.session.commit()
        return json.dumps(new_user)
    return json.dumps(existing_user)


# this function is largely copied from the project.py file
# from the udacity github repository but changed to the needs of this project
# it handles the authorization using a google account
# this function handles all requests coming form a rest client like angularJS
@authentication_blueprint.route('/api/user/gconnect', methods=['POST'])
@cross_origin()
def gconnect():
    session_token = request.args.get('session_token')
    # Obtain authorization code
    code = request.data

    current_session: LoginSessionItem = login_session[session_token]
    # Validate state token
    if current_session is None:
        # state token invalid
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope=[
            'https://www.googleapis.com/auth/plus.me',
            'email',
            'openid',
            'https://www.googleapis.com/auth/plus.login'])
        oauth_flow.redirect_uri = 'http://localhost:4200/user/gconnect'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError as e:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token: str = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id: str = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token: str = current_session.access_token
    stored_gplus_id: str = current_session.gplus_id
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    current_session.access_token = credentials.access_token
    current_session.gplus_id = gplus_id

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

    response = make_response(json.dumps('User sucessfully connected.'), 200)
    response.headers['Content-Type'] = 'application/json'
    return response


# this function is largely copied from the project.py file
# from the udacity github repository but changed to the needs of this project
# DISCONNECT - Revoke a current user's token and reset their login_session
@authentication_blueprint.route('/api/user/gdisconnect', methods=['POST'])
@cross_origin()
def gdisconnect():
    session_token = request.args.get('session_token')
    current_session = login_session[session_token]
    if current_session is not None and current_session.logged_in:
        access_token: str = login_session[session_token].access_token
        current_session: LoginSessionItem = login_session[session_token]
        current_session.logged_in = False

        if access_token is None:
            response = make_response(
                json.dumps('Current user not connected.'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        url = (
            'https://accounts.google.com/o/oauth2/revoke?token=%s'
            % current_session.access_token)
        h = httplib2.Http()
        result = h.request(url, 'GET')[0]

        if result['status'] == '200':
            del login_session[session_token]  # delete the local session object
            response = make_response(
                json.dumps('Successfully disconnected.'), 200)
            response.headers['Content-Type'] = 'application/json'
            return response
        else:
            response = make_response(
                json.dumps('Failed to revoke token for given user.'), 400)
            response.headers['Content-Type'] = 'application/json'
            return response

    else:
        response = make_response(json.dumps('Session not authenticated'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response


@authentication_blueprint.route('/api/user/all_sessions', methods=['GET'])
@cross_origin()
def enumerate_session_tokens():
    session_token = request.args.get('session_token')
    tokens = []
    if login_session[session_token] is not None:
        username = login_session[session_token].username
        for key in login_session.keys():
            session: LoginSessionItem = login_session[key]
            if session is not None:
                if session.username == username and session.logged_in is True:
                    tokens.append(session.session_token)
    return json.dumps(tokens)


@authentication_blueprint.route('/api/user/userinfo', methods=['GET'])
@cross_origin()
def userinfo():
    session_token = request.args.get('session_token')
    current_session = login_session[session_token]
    if current_session is not None and current_session.logged_in:
        response = make_response(create_user(
            current_session.userinfo_url,
            current_session.email,
            current_session.picture,
            current_session.username), 200)
    else:
        response = make_response(json.dumps('Session not authenticated'), 401)

    response.headers['Content-Type'] = 'application/json'
    return response

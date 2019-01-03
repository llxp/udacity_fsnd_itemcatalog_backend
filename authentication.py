import os

import httplib2 as httplib2
import requests
from flask import json, request, make_response, flash, Blueprint, Response
import string
import random
#from flask import session as login_session


from flask_sqlalchemy import xrange
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError

from Models import User
from app_init import app, db
from login_sesssion import LoginSession, LoginSessionItem

app.config['SESSION_TYPE'] = 'SESSION_SQLALCHEMY'
SESSION_TYPE = 'SESSION_SQLALCHEMY'

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog"

authentication_blueprint = Blueprint('authentication', __name__, template_folder='templates')

login_session = LoginSession()


def generate_random_string():
    return ''.join(random.choice(string.ascii_uppercase + string.digits)
                   for x in xrange(32))


# create an anti-forgery token
@authentication_blueprint.route('/api/user/new_session')
def new_session():
    session_token: str = generate_random_string()
    response = Response(json.dumps(session_token))
    login_session[session_token] = LoginSessionItem
    login_session[session_token].session_token = session_token
    print(login_session)
    print("added new session object")
    # response.headers['X-XSRF-TOKEN'] = state
    return response  # json.dumps(new_session_token)


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


@authentication_blueprint.route('/api/user/gconnect', methods=['POST'])
def gconnect():
    for header in request.headers:
        print("header: " + str(header))
    session_token = request.args.get('session_token')
    print("session_token: " + str(session_token))
    current_session = login_session[session_token]
    # Validate state token
    if current_session is None:
        # state token invalid
        print(login_session.session_tokens)
        print("invalid token state")
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    current_session: LoginSessionItem = login_session[session_token]

    # Obtain authorization code
    code = request.data

    print("code: " + str(code))

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
        print('error: ' + str(e))
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    print(credentials.access_token)

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
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token: str = current_session.access_token
    stored_gplus_id: str = current_session.gplus_id
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        print("Current user is already connected.")
        response = make_response(json.dumps('Current user is already connected.'), 200)
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


# DISCONNECT - Revoke a current user's token and reset their login_session
@authentication_blueprint.route('/api/user/gdisconnect')
def gdisconnect():
    session_token = request.args.get('session_token')
    current_session = login_session[session_token]
    if current_session is not None and current_session.logged_in:
        access_token: str = login_session[session_token].access_token
        current_session: LoginSessionItem = login_session[session_token]
        print('In gdisconnect access token is %s', access_token)
        print('User name is: ')
        print(current_session.username)

        if access_token is None:
            print('Access Token is None')
            response = make_response(json.dumps('Current user not connected.'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % current_session.access_token
        h = httplib2.Http()
        result = h.request(url, 'GET')[0]
        print('result is ')
        print(result)

        if result['status'] == '200':
            del login_session[session_token]
            response = make_response(json.dumps('Successfully disconnected.'), 200)
            response.headers['Content-Type'] = 'application/json'
            return response
        else:
            response = make_response(json.dumps('Failed to revoke token for given user.'), 400)
            response.headers['Content-Type'] = 'application/json'
            return response

    else:
        response = make_response(json.dumps('Session not authenticated'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response


@authentication_blueprint.route('/api/user/all_sessions', methods=['GET'])
def enumerate_session_tokens():
    session_token = request.args.get('session_token')
    username = login_session[session_token].username
    tokens = []
    for x in login_session:
        if x.username == username and x.logged_in is True:
            tokens.append(x.session_token)
    return json.dumps(tokens)


@authentication_blueprint.route('/api/user/userinfo', methods=['GET'])
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


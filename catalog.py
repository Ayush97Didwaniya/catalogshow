from flask import Flask, render_template, \
    request, redirect, \
    jsonify, url_for, flash
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_with_user import Base, Category, Items, User

# New imports for create anti forgery state token
from flask import session as login_session
import random
import string

# IMPORTS FOR AUTHENTICATION AND AUTHORIZATION
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

# Connect to Database and create database session
engine = create_engine('sqlite:///itemcatalogwithUser.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog Project"


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
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
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
                                'Current user is already connected.'),
                                200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

# see if user exists, if it doesn't make a new
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px;' \
              'height:300px;' \
              'border-radius: 150px;' \
              '-webkit-border-radius: 150px;' \
              '-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps
                                 ('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' \
        % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect(url_for('categories_items'))
    else:
        response = make_response(json.dumps
                                 ('Failed to revoke token for given user.',
                                  400))
        response.headers['Content-Type'] = 'application/json'
        return response


# code for main page showing with latest item added list
@app.route('/')
@app.route('/categories_items')
def categories_items():
    categories = session.query(Category).all()
    items = session.query(Items).order_by(desc(Items.id)).limit(10).all()
    return render_template('first.html', categories=categories,
                           items=items, login=login_session)


# code for showing Items of specific category
@app.route('/catalog/<int:category_id>/category/items')
def items(category_id):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Items).filter_by(category_id=category_id).all()
    return render_template('second.html', categories=categories,
                           category=category, items=items, login=login_session)


# code showing description of item
@app.route('/catalog/<int:category_id>/<string:item_id>')
def description(category_id, item_id):
    item = session.query(Items).filter_by(id=item_id).one()
    return render_template('description.html', item=item, login=login_session)


# to give permission only to sign user
# if 'username' not in login_session:

# Code for add an item
@app.route('/catalog/additem', methods=['GET', 'POST'])
def add_item():
    categories = session.query(Category).all()
    if 'username' not in login_session:
        return redirect(url_for('categories_items'))
    else:
        if request.method == 'POST':
            category1 = session.query(Category).filter_by(
                name=request.form['category']).one()
            user = login_session['username']
            user1 = session.query(User).filter_by(
                name=user).one()
            new = Items(name=request.form['name'],
                        description=request.form['description'],
                        price='$'+request.form['price'],
                        category=category1, user=user1)
            session.add(new)
            flash('New Items %s Successfully Created' % new.name)
            session.commit()
            return redirect(url_for('categories_items'))
        else:
            return render_template('add.html', categories=categories,
                                   login=login_session)


# code for edit an item
@app.route('/catalog/category/item/<int:item_id>/edit', methods=['GET',
           'POST'])
def edit_item(item_id):
    if 'username' not in login_session:
        return redirect(url_for('categories_items'))
    else:
        categories = session.query(Category).all()
        editeditem = session.query(
            Items).filter_by(id=item_id).one()
        if login_session['user_id'] != editeditem.user_id:
            flash("You can edit only your items")
            return redirect(url_for('categories_items'))
        else:
            if request.method == 'POST':
                editeditem.name = request.form['name']
                editeditem.description = request.form['description']
                editeditem.price = '$' + request.form['price']
                category1 = session.query(Category).filter_by(
                    name=request.form['category']).one()
                editeditem.category = category1
                session.add(editeditem)
                flash('Item %s Successfully Edited' % editeditem.name)
                session.commit()
                return redirect(url_for('categories_items'))
            else:
                return render_template('edititem.html', categories=categories,
                                       item=editeditem, login=login_session)


# code for delete an item
@app.route('/catalog/category/item/<int:item_id>/delete', methods=['GET',
           'POST'])
def delete_item(item_id):
    if 'username' not in login_session:
        return redirect(url_for('categories_items'))
    else:
        deleteditem = session.query(Items).filter_by(id=item_id).one()
        if login_session['user_id'] != deleteditem.user_id:
            flash("You can delete only your items")
            return redirect(url_for('categories_items'))
        else:
            if request.method == 'POST':
                session.delete(deleteditem)
                flash('Item %s Successfully deleted' % deleteditem.name)
                session.commit()
                return redirect(url_for('categories_items'))
            else:
                return render_template(
                    'deleteitem.html', item=deleteditem, login=login_session)


# code for getting json data
@app.route('/catalog.json')
def category_item_json():
    categories = session.query(Category).all()
    items = session.query(Items).all()
    return jsonify(items=[i.serialize for i in items])

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)

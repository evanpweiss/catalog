from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
import bleach

env = 'vagrant'
if env == 'vagrant':
    secrets_path = 'client_secrets.json'

if env == 'ec2':
    secrets_path = '/var/www/catalog/client_secrets.json'

app = Flask(__name__)

CLIENT_ID = json.loads(
    open(secrets_path, 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog"

# Set up automap
Base = automap_base()
engine = create_engine('postgresql+psycopg2://catalog_user:catalog@localhost/catalog')
Base.prepare(engine, reflect=True)


# Set up classes for each table in catalog db
Item = Base.classes.item_table
User = Base.classes.users
Category = Base.classes.categories

# Connect to Database and create database session
session = Session(engine)

# User Helper Function
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

# Login / logout methods
# Create anti-forgery state token
@app.route('/login/')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render('login.html', STATE=state)

# Process login
@app.route('/gconnect/', methods=['POST'])
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
        oauth_flow = flow_from_clientsecrets(secrets_path, scope='')
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
        response = make_response(json.dumps('Current user is already connected.'),
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
    login_session['email'] = data['email']

    # check to see if user already exists, and if not, updated User table
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    return render('login_success.html', email=login_session['email'])

# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect/')
def gdisconnect():
    access_token = login_session['access_token']
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    if access_token is None:
        print 'Access Token is None'
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session[
        'access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['user_id']

        return render('logout_success.html')
    else:

        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# JSON API to return all catalog information
@app.route('/catalog/catalog.json')
def catalogJSON():
    catalog = {'Category': []}
    categories = session.query(Category).all()
    for category in categories:
        items = []
        result = session.query(Item).filter(
            Item.category_id == category.id).all()
        for item in result:
            items.append({"id": item.id,
                          "name": item.name,
                          "description": item.description})
        catalog['Category'].append({"id": category.id,
                                    "name": category.name,
                                    "Item": items})
    return jsonify(catalog)

# JSON API to return information for a single item
@app.route('/catalog/items/<int:item_id>.json')
def itemJSON(item_id):
    result = session.query(Item).filter(
        Item.id == item_id).join(Category).one()
    item = {"id": result.id,
            "name": result.name,
            "category": result.category.name,
            "description": result.description}
    return jsonify(item)

# PAGE HANDLERS
# helper render function to pass logged-in state to main template
def render(html_template, **kw):
    if 'user_id' in login_session:
        logged_in_id = login_session['user_id']
    else:
        logged_in_id = None
    return render_template(html_template, logged_in_id=logged_in_id, **kw)

# Show all categories and 10 most recently added items
@app.route('/')
@app.route('/catalog/')
def topPage():
    categories = session.query(Category).order_by(asc(Category.name)).all()
    ten_items = session.query(Item).order_by(desc(Item.id)).limit(10)
    return render('top.html', categories=categories, items=ten_items, item_header="Latest Items")

# Show all available items for a category
@app.route('/catalog/catgegories/<int:category_id>/')
def showItems(category_id):
    category = session.query(Category).filter(Category.id == category_id).one()
    categories = session.query(Category).order_by(asc(Category.name)).all()
    items = session.query(Item).filter(
        Item.category_id == category_id).order_by(asc(Item.name)).all()
    item_header = "%s Items (%s items)" % (category.name, len(items))
    return render('top.html', items=items, categories=categories, item_header=item_header)

# Show item description
@app.route('/catalog/items/<int:item_id>/')
def showItemDescription(item_id):
    item = session.query(Item).filter(Item.id == item_id).one()
    return render('item.html', item=item)

# Create a new item
@app.route('/catalog/newItem/', methods=['GET', 'POST'])
def newItem():
    if login_session.get('user_id') == None:
        flash("WARNING: must be logged in to create items")
        return redirect(url_for('topPage'))
    if request.method == 'POST':
        name = bleach.clean(request.form['name'])
        description = bleach.clean(request.form['description'])
        category_id = bleach.clean(request.form['category_id'])
        newItem = Item(name=name, description=description, category_id=category_id, user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash('Created item "%s"' % newItem.name)
        return redirect(url_for('topPage'))
    else:
        categories = session.query(Category).order_by(asc(Category.name)).all()
        return render('newItem.html', categories=categories)


# Edit an item
@app.route('/catalog/items/<int:item_id>/edit/', methods=['GET', 'POST'])
def editItem(item_id):
    editedItem = session.query(Item).filter_by(id=item_id).one()
    if login_session.get("user_id") == None:
      flash("WARNING: must be logged in to edit items")
      return redirect(url_for('topPage'))
    if login_session['user_id'] != editedItem.user_id:
      flash("WARNING: you can only edit your own items")
      return redirect(url_for('topPage'))
    if request.method == 'POST':
        editedItem.name = bleach.clean(request.form['name'])
        editedItem.description = bleach.clean(request.form['description'])
        editedItem.category_id = bleach.clean(request.form['category_id'])
        session.add(editedItem)
        session.commit()
        flash('Edited item "%s"' % editedItem.name)
        return redirect(url_for('topPage'))
    else:
        categories = session.query(Category).order_by(asc(Category.name)).all()
        return render('editItem.html', item=editedItem, categories=categories)


# Delete an items
@app.route('/catalog/items/<int:item_id>/delete/', methods=['GET', 'POST'])
def deleteItem(item_id):
    itemToDelete = session.query(Item).filter_by(id=item_id).one()
    if login_session.get("user_id") == None:
      flash("WARNING: must be logged in to delete items")
      return redirect(url_for('topPage'))
    if login_session['user_id'] != itemToDelete.user_id:
      flash("WARNING: you can only delete your own items")
      return redirect(url_for('topPage'))
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Deleted item "%s"' % itemToDelete.name)
        return redirect(url_for('topPage'))
    else:
        return render('deleteItem.html', item=itemToDelete)

if env == 'vagrant':

    # set up Flask app
    if __name__ == '__main__':
        app.secret_key = "super_secret_key"
        app.debug = True
        app.run(host="0.0.0.0", port=5000)

if env == 'ec2':

    # set up Flask app
    if __name__ == '__main__':
        app.debug = True
        app.run()
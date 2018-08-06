from flask import Flask, render_template, request
from flask import redirect, jsonify, url_for, flash, make_response
from flask import session as login_session
from functools import wraps
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from databaseSetup import Categorys, Base, CatItems, User
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import random
import string
import httplib2
import json
import requests

app = Flask(__name__)

# This will load my SQL database.
engine = create_engine('sqlite:///waylandDatabase.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# This loads the json file downloaded from google developer tools.
CLIENT_ID = json.loads(
                        open('client_secrets.json', 'r').read()
                        )['web']['client_id']
APPLICATION_NAME = "colonialMarines"


def verifyLogin(f):
    '''
    Verify Login Creds:
    This was found on: http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    '''
    @wraps(f)
    def loginCheck(*args, **kwargs):
        if 'username' not in login_session:
            # If user is not logged in, redirected to home!
            return redirect('/')
        return f(*args, **kwargs)
    return loginCheck


@app.route('/gconnect', methods=['POST'])
def gconnect():
    '''
    Used from course material.
    This fucntion checks the uniq state token matches
    as an anti-forgery measure, then logs into google
    to authenticate the user pulling their ID information
    from their google account.
    '''
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(
            json.dumps('Invalid state parameter.'), 401)
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
            'Current user is already connected.'), 200)
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

    output = ''
    output += login_session['username']
    output += login_session['picture']
    print "done!"
    return output


@app.route('/gdisconnect')
@verifyLogin
def gdisconnect():
    '''
    This was used from the Udacity Course material.
    This will dissconnect the user from their current
    signed in session.
    '''
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/')
@app.route('/home')
def homePage():
    '''
    This is the homepage function. It will verify if a user is
    not signed in and rediect them to the home page.
    '''
    if 'username' not in login_session:
        state = ''.join(random.choice(
            string.ascii_uppercase + string.digits) for x in xrange(32))
        login_session['state'] = state
        # The Public Main HTML is loaded if a user is not logged in.
        session.close()
        return render_template(
            'public_main.html',
            STATE=state)
    else:
        # This is loaded if a user is logged in.
        flash("you are now logged in as %s" % login_session['username'])
        categorys = session.query(Categorys).all()
        session.close()
        return render_template(
            'main.html',
            categorys=categorys,
            STATE=login_session['state'])


@app.route('/Catalog/<int:categorys_id>/')
@verifyLogin
def showCat(categorys_id):
    '''
    This will render the Cateogrys Page so a user can look at
    each category and items under.
    '''
    # If a user is signed in, it will try and load all items
    # for that category.
    categorys = session.query(Categorys).all()
    try:
        categoryname = session.query(
            Categorys).filter_by(id=categorys_id).one()
        items = session.query(
            CatItems).filter_by(categorys_id=categorys_id)
        session.close()
        return render_template(
            'items.html',
            category=categorys,
            items=items,
            categorys_id=categorys_id,
            catName=categoryname)
    except:
        # If an error happens, it is printed to terminal
        # and then they are returned to the main.html.
        session.close()
        flash("An error occured fetching database items.")
        return render_template(
            'main.html',
            categorys=categorys,
            STATE=login_session['state'])


@app.route('/Catalog/<int:categorys_id>/<int:item_id>/Description/')
@verifyLogin
def itemDescription(categorys_id, item_id):
    '''
    This will show the description text for items under a spesified
    cateogry.
    '''
    # This will return the Items name and Description.
    categoryname = session.query(Categorys).filter_by(id=categorys_id).one()
    itemDescriptionText = session.query(
        CatItems).filter(
        CatItems.id == item_id, CatItems.categorys_id == categorys_id).one()
    if getUserID(login_session['email']) != itemDescriptionText.user_id:
        session.close()
        return render_template(
            'description_noedit.html',
            gunInfo=itemDescriptionText,
            catName=categoryname)
    else:
        session.close()
        return render_template(
            'description.html',
            gunInfo=itemDescriptionText,
            catName=categoryname)


@app.route(
    '/Catalog/<int:categorys_id>/<int:item_id>/edit/',
    methods=['GET', 'POST'])
@verifyLogin
def editPage(categorys_id, item_id):
    '''
    This function can take Get or Post requests.
    IF a get request is recieved the user is directed to the edit page
    where they can edit information of an item under a spesified cateogry.
    A Post request is recieved then the information of an item will be
    changed in the database.
    '''
    itemDescriptionText = session.query(
        CatItems).filter(
        CatItems.id == item_id, CatItems.categorys_id == categorys_id).one()
    if getUserID(login_session['email']) != itemDescriptionText.user_id:
        categorys = session.query(Categorys).all()
        flash("You do not have permission to edit item")
        session.close()
        return render_template(
            'main.html',
            categorys=categorys,
            STATE=login_session['state'])
    else:
        itemToEdit = session.query(CatItems).filter(
            CatItems.id == item_id, CatItems.categorys_id == categorys_id).one()
        # If the server recieves a post request it runs this If statment.
        if request.method == 'POST':
            if request.form['name']:
                # In the edit page, it will pull the name from the html form.
                itemToEdit.name = request.form['name']
            if request.form['description']:
                # In the edit page, this pulls the item description from the
                # form if one is entered in the form.
                itemToEdit.description = request.form['description']
            session.add(itemToEdit)
            session.commit()
            # Once new information is added to the database, the item
            # description page is returned.
            session.close()
            return redirect(url_for(
                'itemDescription',
                item_id=item_id,
                categorys_id=categorys_id))
        else:
            # If a GET request was recieved, the Edit page is rendered.
            categoryname = session.query(Categorys).filter_by(id=categorys_id).one()
            session.close()
            return render_template(
                'edit.html',
                gunInfo=itemDescriptionText,
                catName=categoryname)
    session.close()


@app.route(
    '/Catalog/<int:categorys_id>/<int:item_id>/delete/',
    methods=['GET', 'POST'])
@verifyLogin
def deletePage(categorys_id, item_id):
    '''
    This function will take GET or Post requests.
    If a get is recieved then the user is directed to the delete
    conformation page, if a Post request is recieved the information
    is deleted of an item under the cateogry spesified.

    If a user tries to hit this page and they are not the owner of them
    they are redirected to the main page.
    '''
    itemDescriptionText = session.query(
        CatItems).filter(
        CatItems.id == item_id, CatItems.categorys_id == categorys_id).one()
    if getUserID(login_session['email']) != itemDescriptionText.user_id:
        categorys = session.query(Categorys).all()
        flash("You do not have permission to delete item")
        categorys = session.query(Categorys).all()
        session.close()
        return render_template(
            'main.html',
            categorys=categorys,
            STATE=login_session['state'])
    else:
        itemToDelete = session.query(
            CatItems).filter(
            CatItems.id == item_id, CatItems.categorys_id == categorys_id).one()
        if request.method == 'POST':
            # If a POST request is recieved, it will delete the item
            # in question.
            session.delete(itemToDelete)
            session.commit()
            session.close()
            return redirect(url_for(
                'showCat',
                categorys_id=categorys_id))
        else:
            session.close()
            return render_template(
                'delete.html',
                gunInfo=itemToDelete)


@app.route(
    '/Catalog/<int:categorys_id>/add/',
    methods=['GET', 'POST'])
@verifyLogin
def addItem(categorys_id):
    if request.method == 'POST':
        # If a POST request is received, this will pull the forum
        # data from the HTML page.
        newItem = CatItems(
            user_id=getUserID(login_session['email']),
            name=request.form['name'],
            description=request.form['description'],
            categorys_id=categorys_id)
        session.add(newItem)
        session.commit()
        session.close()
        return redirect(url_for('showCat', categorys_id=categorys_id))
    else:
        # If a GET request is recieved than the HTML page to add items
        # is rendered.
        categoryname = session.query(
            Categorys).filter_by(id=categorys_id).one()
        session.close()
        return render_template(
            'addItem.html',
            categorys_id=categorys_id,
            catName=categoryname)


# Information Gathering.
def getUserID(email):
    # This will return the user that is logged in USERS ID.
    # Used from the UDACITY Course Material.
    try:
        user = session.query(User).filter_by(email=email).one()
        session.close()
        return user.id
    except Exception as e:
        return None


# API Endpoints
@app.route('/api/')
def allCatApiEnd():
    # If the GET request is recieved, a Json query is returned of
    # all Categorys.
    categorys = session.query(Categorys).all()
    session.close()
    return jsonify(categorys=[i.serialize for i in categorys])


@app.route('/api/<int:categorys_id>/')
def listItemApiEnd(categorys_id):
    # If a GET request is recieved then it will return the items
    # listed in that category.
    items = session.query(CatItems).filter_by(categorys_id=categorys_id)
    session.close()
    return jsonify(items=[i.serialize for i in items])


@app.route('/api/<int:categorys_id>/<int:item_id>/')
def listItemApiItem(categorys_id, item_id):
    # If a GET request is recieved then it will return the items
    # listed in that category.
    items = session.query(CatItems).filter(
        CatItems.id == item_id,
        CatItems.categorys_id == categorys_id).one()
    session.close()
    return jsonify(items.serialize)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = False
    app.run(host='0.0.0.0', port=8000)
    session.close()

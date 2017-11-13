from studentapp import app
from studentapp.models import *
import studentapp.config as config
import studentapp.constants as constants
from studentapp.models.user import *
from studentapp.utils import *

from oic import rndstr
from oic.utils.http_util import Redirect 
from oic.oic import Client
from oic.utils.authn.client import CLIENT_AUTHN_METHOD
import requests
from requests.auth import HTTPBasicAuth
import json
import datetime
from functools import wraps

from flask import redirect, render_template, request, url_for, session

@app.route('/login', methods=['GET', 'POST'])
#@login_required
def login():
    # Compute redirect url
    print "here in login"

    # Check if already logged in

    if 'jwt' in request.cookies:
        print "in jwt!"
        try:
            id = decode_token(request.cookies['jwt'])
            user = User.query.filter_by(id=id).first()
            return redirect('/')
        except Exception as e:
            pass

    client = Client(client_authn_method=CLIENT_AUTHN_METHOD)
    error = ""

    try:
        if "code" in request.args and "state" in request.args and request.args["state"] == session["state"]:
            r = requests.post('https://oidc.mit.edu/token', auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET),
                               data={"grant_type": "authorization_code",
                                     "code": request.args["code"],
                                     "redirect_uri": redirect_url})
            auth_token = json.loads(r.text)["access_token"]
            r = requests.get('https://oidc.mit.edu/userinfo', headers={"Authorization": "Bearer " + auth_token})
            user_info = json.loads(r.text)
            if "email" in user_info and user_info["email_verified"] == True and user_info["email"].endswith("@mit.edu"):
                # Authenticated
                email = user_info["email"]
                name = user_info["name"]
                session["logged_in"] = True

                user = User.query.filter_by(email=email).first()
                if user is None:
                    # Initialize the user with a very old last_post time
                    user = User(email=email, name=name, last_post=datetime.datetime.min)
                    db.session.add(user)
                    db.session.commit()

                token = encode_token(user)
                response = app.make_response(redirect('/'))
                if 'redirect' in request.args:
                    response = app.make_response(redirect(request.args['redirect']))

                response.set_cookie('jwt', token, expires=datetime.datetime.now()+datetime.timedelta(days=90))
                print response
                return response
            else:
                if not "email" in user_info:
                    print "no email in user_info"
                else:
                    print "well...invalid everything I guess"

        session["state"] = rndstr()
        session["nonce"] = rndstr()

        args = {
            "client_id": constants.CLIENT_ID,
            "response_type": ["code"],
            "scope": ["email", "openid", "profile"],
            "state": session["state"],
            "nonce": session["nonce"],
            "redirect_uri": redirect_url
        }

        auth_req = client.construct_AuthorizationRequest(request_args=args)
        login_url = auth_req.request('https://oidc.mit.edu/authorize')

        if error == "":
            return redirect(login_url)
        else:
            return render_template('500.html', login_url=login_url)

    except Exception as e:
        session["state"] = rndstr()
        session["nonce"] = rndstr()

        args = {
            "client_id": constants.CLIENT_ID,
            "response_type": ["code"],
            "scope": ["email", "openid", "profile"],
            "state": session["state"],
            "nonce": session["nonce"],
            "redirect_uri": config.DOMAIN+'/login'
        }

        auth_req = client.construct_AuthorizationRequest(request_args=args)
        login_url = auth_req.request('https://oidc.mit.edu/authorize')

        return render_template('500.html', login_url=login_url)


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session['logged_in'] == True:
            return f(*args, **kwargs)
            return redirect(url_for('index'))
        else:
            flash("You need to login first")
            return redirect(url_for('login'))
    return wrap

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session['logged_in'] = False
    response = app.make_response(redirect('/'))
    response.set_cookie('jwt', '')
    return response
    return render_template("login.html")





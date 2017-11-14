from flask import Flask
from flask import Markup
from flask import render_template, flash, redirect, session, url_for, request, g, json, jsonify, send_from_directory
from studentapp import app, db
from studentapp.models import UserLogin, UserData, ButtonClicks
from studentapp.controllers import login, admin
from fakedata_functions import *
from queries import *
import numpy as np
import csv
import json
from datetime import datetime
import webbrowser
from functools import wraps


# GOOGLE_APPLICATION_CREDENTIALS = './my-first-project-00521592dba3.json'


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
# @login_required
def index():

    uid = '534584'
    print "in index function"
    session['uid'] = uid
    uid = int(uid)
    uname = "uname"

    login_check = UserData.query.filter_by(user_id=uid).first()
    print login_check

    latest = "latest"
    now = "now"

    if login_check != None:
        latest = str(login_check.login_date)
        latest = latest[0:10]
        now = str(datetime.utcnow())
        now = now[0:10]
        print latest, now

    if (login_check != None) and (latest == now):
        print "Yes!!"
        uname = login_check.username
        ndays_act = login_check.ndays_act 
        nproblems_attempted = login_check.nproblems_attempted 
        one_attempt = login_check.one_attempt 
        multiple_attempts = login_check.multiple_attempts
        not_completed = login_check.not_completed
        months = login_check.months
        values = [uid, uname, ndays_act, nproblems_attempted, one_attempt, multiple_attempts, not_completed]
        print values
        print months


        devicestr = str(request.user_agent)
        devicetup = tuple(filter(None,devicestr.split(' ')))
        devicemessy = devicetup[1]
        device = devicemessy[1:-1]

        browserstr = str(request.user_agent)
        browsertup = tuple(filter(None,devicestr.split(' ')))
        browsermessy = browsertup[11]
        browser = browsermessy[0:-14]

        clicks = 0

        userlogin = UserLogin(
            user_id = uid, 
            username = uname, 
            login_date = datetime.utcnow(), 
            ip_address = str(request.remote_addr), 
            device = device, 
            browser = browser)

        print "in user login"
        print uid, uname, datetime.utcnow(), str(request.remote_addr), device, browser, clicks
        db.session.add(userlogin)
        db.session.commit()

        buttonclicks = ButtonClicks(
            user_id = uid, 
            username = uname, 
            login_date = datetime.utcnow(), 
            nforum_click = clicks)

        print "in button clicks"
        db.session.add(buttonclicks)
        db.session.commit()

        login_inst = UserLogin.query.filter_by(user_id=uid).first()
        login_button = ButtonClicks.query.filter_by(user_id=uid).first()

        print login_inst
        print login_button

    else:
        print "This is a new entry for today"


        [uname, ndays_act] = query_ophelia(uid, uname)
        uname = uname[1:]
        [months, nproblems_attempted] = query_hamlet(uid, uname)
        [one_attempt, multiple_attempts, not_completed] = query_polonius(uid, uname)

        values = [uid, uname, ndays_act, nproblems_attempted, one_attempt, multiple_attempts, not_completed]
        print values
        print months

        devicestr = str(request.user_agent)
        devicetup = tuple(filter(None,devicestr.split(' ')))
        devicemessy = devicetup[1]
        device = devicemessy[1:-1]

        browserstr = str(request.user_agent)
        browsertup = tuple(filter(None,devicestr.split(' ')))
        browsermessy = browsertup[11]
        browser = browsermessy[0:-14]

        clicks = 0

        userlogin = UserLogin(
            user_id = uid, 
            username = uname, 
            login_date = datetime.utcnow(), 
            ip_address = str(request.remote_addr), 
            device = device, 
            browser = browser)

        print "in user login"
        print uid, uname, datetime.utcnow(), str(request.remote_addr), device, browser, clicks
        db.session.add(userlogin)
        db.session.commit()

        userdata = UserData(
            user_id = uid, 
            username = uname, 
            login_date = datetime.utcnow(), 
            ndays_act = ndays_act, 
            nproblems_attempted = nproblems_attempted, 
            one_attempt = one_attempt, 
            multiple_attempts = multiple_attempts, 
            not_completed = not_completed,
            months = str(months))

        print "in user data"
        print uid, uname, datetime.utcnow(), ndays_act, nproblems_attempted, one_attempt, multiple_attempts, not_completed, months
        db.session.add(userdata)
        db.session.commit()

        buttonclicks = ButtonClicks(
            user_id = uid, 
            username = uname, 
            login_date = datetime.utcnow(), 
            nforum_click = clicks)

        print "in button clicks"
        db.session.add(buttonclicks)
        db.session.commit()

        login_inst = UserLogin.query.filter_by(user_id=uid).first()
        login_button = ButtonClicks.query.filter_by(user_id=uid).first()
        login_data = UserData.query.filter_by(user_id=uid).first()

        print login_inst
        print login_button
        print login_data
    
    return render_template("index.html", values=values, months=months)


@app.route('/', methods=['GET', 'POST'])
@app.route('/admin', methods=['GET', 'POST'])
# @login_required
def admin():
    return render_template("admin.html")


@app.route('/forumclicks', methods=['GET', 'POST'])
def forumclicks():
    print "in forum clicks"

    if request.method == 'POST': 
        print "hello"
        results = request.form.getlist('clicks')
        print 'hi'
        print type(results[0])
        print results[0]

        buttonclicks = ButtonClicks.query.filter_by(username=results[0].decode('utf-8')).first()
        print buttonclicks
        buttonclicks.nforum_click += 1
        db.session.commit()
        buttonclicks = ButtonClicks.query.filter_by(username=results[0].decode('utf-8')).first()
        print buttonclicks.nforum_click
    return redirect('https://piazza.com/', 301)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

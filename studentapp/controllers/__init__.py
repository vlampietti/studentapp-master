from flask import Flask
from flask import Markup
from flask import render_template, flash, redirect, session, url_for, request, g, json, jsonify, send_from_directory
from studentapp import app, db
from sqlalchemy import desc
from studentapp.models import UserLogin, UserData, ButtonClicks
from studentapp.controllers import login, admin
from fake_queries import *
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

    uid = '534540'
    print "in index function"
    session['uid'] = uid
    uid = int(uid)
    uname = "uname"

    login_data = UserData.query.filter_by(user_id=uid).order_by(UserData.id.desc()).first()
    uname = login_data.username
    ndays_act = login_data.ndays_act
    completed = login_data.completed
    not_completed = login_data.not_completed
    one_attempt = login_data.one_attempt
    multiple_attempts = login_data.multiple_attempts
    daily_activity = login_data.daily_activity

    percent_complete = float(one_attempt+multiple_attempts)
    total_complete = float(one_attempt+multiple_attempts+not_completed)
    final = float((percent_complete/total_complete)*100)
    final_int = int(final)

    values = [uid, uname, ndays_act, completed, not_completed, one_attempt, multiple_attempts, final_int]

    devicestr = str(request.user_agent)
    devicetup = tuple(filter(None,devicestr.split(' ')))
    devicemessy = devicetup[1]
    device = devicemessy[1:-1]

    browserstr = str(request.user_agent)
    browsertup = tuple(filter(None,devicestr.split(' ')))
    browsermessy = browsertup[11]
    browser = browsermessy[0:-13]
    print browser

    clicks = 0

    userlogin = UserLogin(
        user_id = uid, 
        username = uname, 
        login_date = datetime.utcnow(), 
        ip_address = str(request.remote_addr), 
        device = device, 
        browser = browser)

    db.session.add(userlogin)
    db.session.commit()

    buttonclicks = ButtonClicks(
        user_id = uid, 
        username = uname, 
        login_date = datetime.utcnow(), 
        nforum_click = clicks)

    db.session.add(buttonclicks)
    db.session.commit()

    login_inst = UserLogin.query.filter_by(user_id=uid).first()
    login_button = ButtonClicks.query.filter_by(user_id=uid).first()

    return render_template("index.html", values=values)


@app.route('/forumclicks', methods=['GET', 'POST'])
def forumclicks():
    print "in forum clicks"

    if request.method == 'POST': 
        results = request.form.getlist('clicks')

        buttonclicks = ButtonClicks.query.filter_by(username=results[0].decode('utf-8')).first()
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

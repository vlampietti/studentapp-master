from flask import Flask
from flask import Markup
from flask import Flask
from flask import render_template, flash, redirect, session, url_for, request, g, json, jsonify, send_from_directory
from studentapp import app, db
from studentapp.models import UserLogin
from celery import Celery
from lookup_functions import lookup_days_active, match_uid_to_uname, determine_progress
import numpy as np
import csv
import json
from datetime import datetime
import os

#GOOGLE_APPLICATION_CREDENTIALS = './my-first-project-00521592dba3.json'

def query_ophelia(uid):
    import uuid
    from google.cloud import bigquery
    client = bigquery.Client()
    print "in query_ophelia"
    print uid
    
    query = """
        #standardSQL
        SELECT
            user_id, username, ndays_act, nvideos_total_watched, nforum_posts, sum_dt
        FROM `deidentified_data.person_course`
        WHERE user_id = @uid
        """
    query_job = client.run_async_query(
        str(uuid.uuid4()),
        query,
        query_parameters=(
            bigquery.ScalarQueryParameter('uid', 'INT64', uid),
            bigquery.ScalarQueryParameter(
                'uname', 'STRING', uname)))
    query_job.use_legacy_sql = False
    query_job.begin()
    query_job.result()

    destination_table = query_job.destination
    destination_table.reload()
    f = open("ophelia.csv", "w+")
    for row in destination_table.fetch_data():
        f.write(str(row[0])+","+str(row[1])+","+str(row[2])+","+str(row[3])+","+str(row[4])+","+str(row[5])+"\n")
    f.close()

def query_hamlet(uname):
    import uuid
    from google.cloud import bigquery
    ham_client = bigquery.Client()
    print "in query_hamlet"
    print uname
    
    query = """
        #standardSQL
        SELECT
            nprogcheck, username, nvideo, nproblems_attempted
        FROM `deidentified_data.person_course_day`
        WHERE username = @uname
        ORDER BY nproblems_attempted;
        """

    query_job = ham_client.run_async_query(
        str(uuid.uuid4()),
        query,
        query_parameters=(
            bigquery.ScalarQueryParameter('uid', 'INT64', uid),
            bigquery.ScalarQueryParameter(
                'uname', 'STRING', uname)))
    query_job.use_legacy_sql = False
    query_job.begin()
    query_job.result()

    destination_table2 = query_job.destination
    destination_table2.reload()
    h = open("hamlet.csv", "w+")
    for row in destination_table2.fetch_data():
        h.write(str(row[0])+","+str(row[1])+","+str(row[2])+","+str(row[3])+"\n")
    h.close()

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    print "Here in login"
    error = None
    if request.method == 'POST':
        global uid
        global uname
        global num1
        global num2
        global prog
        uid = request.form['username']

#admin uid redirects to login page 
        if str(uid) == 'admin':
            print uid
            return redirect(url_for('adminlogin'))

        uid = int(uid)
        [uid, uname] = match_uid_to_uname(uid)
        print uid, uname
        query_ophelia(uid)
        query_hamlet(uname)
        if uid >= 534220 and uid <= 534964:
            [uid, uname, num1, num2] = lookup_days_active(uid)
            [uname, prog] = determine_progress(uname)
            print uid, uname, num1, num2, prog
            session['uid'] = uid
            session['uname'] = uname
            session['num1'] = num1
            session['num2'] = num2
            session['prog'] = prog
            return redirect(url_for('index'))
            return uid
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template("login.html", error=error)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    labels = ["Videos","","Problems",""]
    values = [32,67,71,num1]

#an excessive amount of work to pull 'Device' from 'User_Agent'. Looking into alternatives...

    devicestr = str(request.user_agent)
    devicetup = tuple(filter(None,devicestr.split(' ')))
    devicemessy = devicetup[1]
    device = devicemessy[1:-1]

    global clicks
    clicks = 1

    if request.method == 'POST': 
        clicks = request.POST.get('forum_button')
        clicks = int(clicks)
        return clicks

    userlogin = UserLogin(user_id = uid, username = uname, login_date = datetime.utcnow(), device = device, nforum_click = clicks, ip_address = str(request.remote_addr))
    print "in userlogin"
    print uid, uname, datetime.utcnow(), str(request.remote_addr), device, clicks
    db.session.add(userlogin)
    db.session.commit()

    login_inst = UserLogin.query.filter_by(user_id=uid).first()
    return render_template("index.html", values=values, labels=labels, login_inst=login_inst)


@app.route('/', methods=['GET', 'POST'])
@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    print "Here in admin login"
    error = None
    if request.method == 'POST':
        global uid
        global uname
        global num1
        global num2
        uid = request.form['username']
        uid = int(uid)
        [uid, uname] = match_uid_to_uname(uid)
        print uid, uname
        query_ophelia(uid,uname)
        query_hamlet(uname)
        if uid >= 534220 and uid <= 534964:
            [uid, uname, num1, num2] = lookup_days_active(uid)
            print uid, uname, num1, num2
            session['uid'] = uid
            session['uname'] = uname
            session['num1'] = num1
            session['num2'] = num2
            return redirect(url_for('index'))
            return uid
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template("adminlogin.html", error=error)


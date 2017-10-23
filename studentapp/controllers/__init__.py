from flask import Flask
from flask import Markup
from flask import Flask
from flask import render_template, flash, redirect, session, url_for, request, g, json, jsonify, send_from_directory
from studentapp import app
from celery import Celery
from lookup_functions import lookup_days_active, match_uid_to_uname
import numpy as np
import csv

#load these credentials before opening the app
GOOGLE_APPLICATION_CREDENTIALS = './my-first-project-00521592dba3.json'

def query_shakespeare(uid,uname):
    import uuid
    from google.cloud import bigquery
    client = bigquery.Client()
    print "in query_shakespeare"
    print uid, uname
    
    query = """
        #standardSQL
        SELECT
            user_id, username, ndays_act, nvideos_total_watched
        FROM `deidentified_data.person_course`
        WHERE user_id = @uid
        UNION ALL
        SELECT
            nprogcheck, username, nvideo, nproblems_attempted
        FROM `deidentified_data.person_course_day`
        WHERE username = @uname;
        """

#if there is a forum linked to edX we will want to pull nforum_posts from `person_course`

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
    f = open("data-placeholder.csv", "w+")
    for row in destination_table.fetch_data():
        f.write(str(row[0])+","+str(row[1])+","+str(row[2])+","+str(row[3])+"\n")
    f.close()

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
        uid = int(request.form['username'])
        [uid, uname] = match_uid_to_uname(uid)
        print uid, uname
        query_shakespeare(uid,uname)
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
    return render_template("index.html", values=values, labels=labels)

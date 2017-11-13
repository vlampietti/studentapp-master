from flask import Flask
from flask import Markup
from flask import render_template, flash, redirect, session, url_for, request, g, json, jsonify, send_from_directory
from studentapp import app, db
from studentapp.models import UserLogin, ButtonClicks
from lookup_functions import *
from fakedata_queries import *
import numpy as np
import csv
import json
from datetime import datetime
import webbrowser
from functools import wraps
import studentapp.controllers.login

# GOOGLE_APPLICATION_CREDENTIALS = './my-first-project-00521592dba3.json'

# these are the google bigquery queries

def query_ophelia(uid, uname):
    import uuid
    from google.cloud import bigquery
    client = bigquery.Client()
    print "in query_ophelia"
    print uid, uname
    
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

    print('exported {} and {}'.format(uid, uname))

    destination_table = query_job.destination
    destination_table.reload()
    print destination_table
    #db.session.add(destination_table)
    #db.session.commit()

    f = open("ophelia.csv", "w+")
    for row in destination_table.fetch_data():
        f.write(str(row[0])+","+str(row[1])+","+str(row[2])+","+str(row[3])+","+str(row[4])+","+str(row[5])+"\n")
    f.close()


    """
    userlogin = UserLogin(user_id = uid, username = uname, login_date = datetime.utcnow(), ip_address = str(request.remote_addr), device = device, browser = browser)
    print "in user login"
    print uid, uname, datetime.utcnow(), str(request.remote_addr), device, browser, clicks
    db.session.add(userlogin)
    db.session.commit()
    """

def query_hamlet(uid, uname):
    import uuid
    from google.cloud import bigquery
    ham_client = bigquery.Client()
    print "in query_hamlet"
    print uid, uname
    
    query = """
        #standardSQL
        SELECT
            nprogcheck, username, nvideo, nproblems_attempted, first_event
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
        h.write(str(row[0])+","+str(row[1])+","+str(row[2])+","+str(row[3])+","+str(row[4])+"\n")
    h.close()

def query_polonius(uid, uname):
    import uuid
    from google.cloud import bigquery
    ham_client = bigquery.Client()
    print "in query_polonius"
    print uid, uname

    query = """
        #standardSQL
        SELECT
            user_id, problem_nid, problem_raw_score, problem_pct_score, n_attempts, date
        FROM `deidentified_data.person_problem`
        WHERE user_id = @uid
        ORDER BY problem_nid;
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

    destination_table3 = query_job.destination
    destination_table3.reload()
    g = open("polonius.csv", "w+")
    for row in destination_table3.fetch_data():
        g.write(str(row[0])+","+str(row[1])+","+str(row[2])+","+str(row[3])+","+str(row[4])+","+str(row[5])+"\n")
    g.close()

# end of google bigquery queries

# login form
"""@app.route('/login', methods=['GET', 'POST'])
def login():
    print "here in login"
    error = None
    if request.method == 'POST':
        uid = request.form['username']
        if str(uid) == 'admin':
            print uid
            return redirect(url_for('adminlogin'))

        uid = int(uid)

        if uid >= 534220 and uid <= 534964 and uid%2 == 0:
            session['logged_in'] = True
            session['uid'] = uid
            return redirect(url_for('index', uid=uid))
        elif uid >= 534220 and uid <= 534964 and uid%2 != 0:
            session['logged_in'] = True
            session['uid'] = uid
            return redirect(url_for('otherindex', uid=uid))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template("login.html", error=error)
"""

# error pages 
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


"""def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session['logged_in'] == True:
            return f(*args, **kwargs)
            return redirect(url_for('index'))
        else:
            flash("You need to login first")
            return redirect(url_for('login'))
    return wrap"""



# index function
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
#@login_required
def index():
    uid = '534592'
    print "in index function"
    session['uid'] = uid
    print uid
    uid = int(uid)
    [uid, uname] = match_uid_to_uname(uid)
    print uid, uname
    query_ophelia(uid, uname)
    query_hamlet(uid, uname)
    query_polonius(uid, uname)

    [uid, uname, num1] = lookup_days_active(uid)
    [uname, prog] = determine_progress(uname)
    [uid, one_attempt, multiple_attempts, not_completed] = problems(uid)
    [uname, jan, feb, mar, apr, may, jun, jul, aug, sep, october, nov, dec] = dates_active(uname)
    [uid, mon] = monthly_problems(uid)
    uname = uname[1:]
    print uid, uname, num1, prog, one_attempt, multiple_attempts, not_completed
    print "months!"
    print jan, feb, mar, apr, may, jun, jul, aug, sep, october, nov, dec
    print "we got this far"
    values = [uid, uname, num1, prog, one_attempt, multiple_attempts, not_completed]
    months = [jan, feb, mar, apr, may, jun, jul, aug, sep, october, nov, dec]
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

    userlogin = UserLogin(user_id = uid, username = uname, login_date = datetime.utcnow(), ip_address = str(request.remote_addr), device = device, browser = browser)
    print "in user login"
    print uid, uname, datetime.utcnow(), str(request.remote_addr), device, browser, clicks
    db.session.add(userlogin)
    db.session.commit()
    buttonclicks = ButtonClicks(user_id = uid, username = uname, login_date = datetime.utcnow(), nforum_click = clicks)
    print "in button clicks"
    db.session.add(buttonclicks)
    db.session.commit()

    login_inst = UserLogin.query.filter_by(user_id=uid).first()
    login_button = ButtonClicks.query.filter_by(user_id=uid).first()
    print login_inst
    print login_button
    print values

    
    return render_template("index.html", login_inst=login_inst, login_button=login_button, values=values, months=months)

@app.route('/otherindex', methods=['GET', 'POST'])
#@login_required
def otherindex():
    print "in other index function"
    uid = session['uid']
    print uid
    uid = int(uid)
    [uid, uname] = match_uid_to_uname(uid)
    print uid, uname
    query_ophelia(uid, uname)
    query_hamlet(uid, uname)
    query_polonius(uid, uname)

    [uid, uname, num1, num2] = lookup_days_active(uid)
    [uname, prog] = determine_progress(uname)
    [uid, one_attempt, multiple_attempts, not_completed] = problems(uid)
    [uname, jan, feb, mar, apr, may, jun, jul, aug, sep, october, nov, dec] = dates_active(uname)
    [uid, mon] = monthly_problems(uid)
    uname = uname[1:]
    print uid, uname, num1, num2, prog, one_attempt, multiple_attempts, not_completed
    print "months!"
    print jan, feb, mar, apr, may, jun, jul, aug, sep, october, nov, dec
    print "we got this far"
    values = [uid, uname, num1, num2, prog, one_attempt, multiple_attempts, not_completed]
    months = [jan, feb, mar, apr, may, jun, jul, aug, sep, october, nov, dec]
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

    userlogin = UserLogin(user_id = uid, username = uname, login_date = datetime.utcnow(), ip_address = str(request.remote_addr), device = device, browser = browser)
    print "in user login"
    print uid, uname, datetime.utcnow(), str(request.remote_addr), device, browser, clicks
    db.session.add(userlogin)
    db.session.commit()
    buttonclicks = ButtonClicks(user_id = uid, username = uname, login_date = datetime.utcnow(), nforum_click = clicks)
    print "in button clicks"
    db.session.add(buttonclicks)
    db.session.commit()

    login_inst = UserLogin.query.filter_by(user_id=uid).first()
    login_button = ButtonClicks.query.filter_by(user_id=uid).first()
    print login_inst
    print login_button
    print values

    
    return render_template("otherindex.html", login_inst=login_inst, login_button=login_button, values=values, months=months)


@app.route('/', methods=['GET', 'POST'])
@app.route('/admin', methods=['GET', 'POST'])
#@login_required
def admin():
    return render_template("admin.html")

# forum click function
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

@app.route('/example1', methods=['GET', 'POST'])
def example1():
    print "in example1"
    uid = '534566'
    session['uid'] = uid
    print uid
    uid = int(uid)
    [uid, uname] = match_uid_to_uname(uid)
    print uid, uname
    query_romeo(uid, uname)
    query_juliet(uid, uname)
    query_mercutio(uid, uname)

    [uid, uname, num1] = fake_lookup_days_active(uid)
    [uname, prog] = fake_determine_progress(uname)
    [uid, one_attempt, multiple_attempts, not_completed] = fake_problems(uid)
    [uname, jan, feb, mar, apr, may, jun, jul, aug, sep, october, nov, dec] = fake_dates_active(uname)
    [uid, mon] = fake_monthly_problems(uid)
    uname = uname[1:]
    print uid, uname, num1, prog, one_attempt, multiple_attempts, not_completed
    print "months!"
    print jan, feb, mar, apr, may, jun, jul, aug, sep, october, nov, dec
    print "we got this far"
    values = [uid, uname, num1, prog, one_attempt, multiple_attempts, not_completed]
    months = [jan, feb, mar, apr, may, jun, jul, aug, sep, october, nov, dec]
    print values
    print months

    return render_template("example.html", values=values, months=months)

@app.route('/example2', methods=['GET', 'POST'])
def example2():
    print "in example2"
    uid = '534580'
    session['uid'] = uid
    print uid
    uid = int(uid)
    [uid, uname] = match_uid_to_uname(uid)
    print uid, uname
    query_romeo(uid, uname)
    query_juliet(uid, uname)
    query_mercutio(uid, uname)

    [uid, uname, num1] = fake_lookup_days_active(uid)
    [uname, prog] = fake_determine_progress(uname)
    [uid, one_attempt, multiple_attempts, not_completed] = fake_problems(uid)
    [uname, jan, feb, mar, apr, may, jun, jul, aug, sep, october, nov, dec] = fake_dates_active(uname)
    [uid, mon] = fake_monthly_problems(uid)
    uname = uname[1:]
    print uid, uname, num1, prog, one_attempt, multiple_attempts, not_completed
    print "months!"
    print jan, feb, mar, apr, may, jun, jul, aug, sep, october, nov, dec
    print "we got this far"
    values = [uid, uname, num1, prog, one_attempt, multiple_attempts, not_completed]
    months = [jan, feb, mar, apr, may, jun, jul, aug, sep, october, nov, dec]
    print values
    print months

    return render_template("example.html", values=values, months=months)

@app.route('/example3', methods=['GET', 'POST'])
def example3():
    print "in example3"
    uid = '534401'
    session['uid'] = uid
    print uid
    uid = int(uid)
    [uid, uname] = match_uid_to_uname(uid)
    print uid, uname
    query_romeo(uid, uname)
    query_juliet(uid, uname)
    query_mercutio(uid, uname)

    [uid, uname, num1] = fake_lookup_days_active(uid)
    [uname, prog] = fake_determine_progress(uname)
    [uid, one_attempt, multiple_attempts, not_completed] = fake_problems(uid)
    [uname, jan, feb, mar, apr, may, jun, jul, aug, sep, october, nov, dec] = fake_dates_active(uname)
    [uid, mon] = fake_monthly_problems(uid)
    uname = uname[1:]
    print uid, uname, num1, prog, one_attempt, multiple_attempts, not_completed
    print "months!"
    print jan, feb, mar, apr, may, jun, jul, aug, sep, october, nov, dec
    print "we got this far"
    values = [uid, uname, num1, prog, one_attempt, multiple_attempts, not_completed]
    months = [jan, feb, mar, apr, may, jun, jul, aug, sep, october, nov, dec]
    print values
    print months

    return render_template("example.html", values=values, months=months)

@app.route('/example4', methods=['GET', 'POST'])
def example4():
    print "in example4"
    uid = '534508'
    session['uid'] = uid
    print uid
    uid = int(uid)
    [uid, uname] = match_uid_to_uname(uid)
    print uid, uname
    query_romeo(uid, uname)
    query_juliet(uid, uname)
    query_mercutio(uid, uname)

    [uid, uname, num1] = fake_lookup_days_active(uid)
    [uname, prog] = fake_determine_progress(uname)
    [uid, one_attempt, multiple_attempts, not_completed] = fake_problems(uid)
    [uname, jan, feb, mar, apr, may, jun, jul, aug, sep, october, nov, dec] = fake_dates_active(uname)
    [uid, mon] = fake_monthly_problems(uid)
    uname = uname[1:]
    print uid, uname, num1, prog, one_attempt, multiple_attempts, not_completed
    print "months!"
    print jan, feb, mar, apr, may, jun, jul, aug, sep, october, nov, dec
    print "we got this far"
    values = [uid, uname, num1, prog, one_attempt, multiple_attempts, not_completed]
    months = [jan, feb, mar, apr, may, jun, jul, aug, sep, october, nov, dec]
    print values
    print months

    return render_template("example.html", values=values, months=months)

# logout function
"""@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session['logged_in'] = False
    flash('You were logged out')
    return render_template("login.html")
"""


# admin login page
"""@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    print "Here in admin login"
    error = None
    if request.method == 'POST':
        uid = request.form['username']
        uid = int(uid)
        if uid >= 534220 and uid <= 534964 and uid%2 == 0:
            session['logged_in'] = True
            session['uid'] = uid
            return redirect(url_for('index', uid=uid))
        elif uid >= 534220 and uid <= 534964 and uid%2 != 0:
            session['logged_in'] = True
            session['uid'] = uid
            return redirect(url_for('otherindex', uid=uid))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template("adminlogin.html", error=error)
"""

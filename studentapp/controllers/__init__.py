from flask import render_template, flash, redirect, session, url_for, request, g, json, jsonify, send_from_directory
from studentapp import app
from lookup_functions import lookup_days_active
import numpy as np
import csv


GOOGLE_APPLICATION_CREDENTIALS = './my-first-project-00521592dba3.json'

def query_shakespeare():
    import uuid
    from google.cloud import bigquery
    client = bigquery.Client()

    query_job = client.run_async_query(
        str(uuid.uuid4()),
        """
        #standardSQL
        SELECT
            user_id, nevents, ndays_act 
        FROM `deidentified_data.person_course` 
        ORDER BY user_id
        """
        )
    query_job.begin()
    query_job.result()

    destination_table = query_job.destination
    destination_table.reload()
    f = open("data-placeholder.csv", "w+")
    for row in destination_table.fetch_data():
        f.write(str(row[0])+","+str(row[1])+","+str(row[2])+"\n")
    f.close()

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def home():
    query_shakespeare()
    return render_template("index.html")

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
    return render_template("index.html")

# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    print "Here in login"
    error = None
    if request.method == 'POST':
        uid = int(request.form['username'])
        if uid >= 534220 and uid <= 534964:
            [num1, num2] = lookup_days_active(uid)
            print num1, num2
            session['uid'] = uid
            session['num1'] = num1
            session['num2'] = num2
            return redirect(url_for('home'))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template("login.html", error=error)

from flask import Flask
from flask import Markup
from flask import render_template, flash, redirect, session, url_for, request, g, json, jsonify, send_from_directory
from studentapp import app, db
from studentapp.models import UserLogin, UserData, ButtonClicks
from streak import *
from fake_queries import *
from datetime import datetime

@app.route('/admin', methods=['GET', 'POST'])
# @login_required
def admin():

    print "here in admin"
    error = None
    if request.method == 'POST':
        global uid
        uid = int(request.form['username'])

        if uid >= 534220 and uid <= 534964:
            session['uid'] = uid
            print uid
            return redirect(url_for('view'))
            return uid
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template("admin.html", error=error)



@app.route('/view', methods=['GET', 'POST'])
def view():
    print "made it this far"
    global uid
    uid = int(uid)
    uname = 'uname'
    session['uid'] = uid
    uid = int(uid)
    print uid

    login_data = UserData.query.filter_by(user_id=uid).order_by(UserData.id.desc()).first()
    uname = login_data.username
    ndays_act = login_data.ndays_act
    completed = login_data.completed
    not_completed = login_data.not_completed
    one_attempt = login_data.one_attempt
    multiple_attempts = login_data.multiple_attempts


    percent_complete = float(one_attempt+multiple_attempts)
    total_complete = float(one_attempt+multiple_attempts+not_completed)

    if int(total_complete) != 0:
        final = float((percent_complete/total_complete)*100)
        final_int = int(final)
    else:
        final_int = 0

    values = [uid, uname, ndays_act, completed, not_completed, one_attempt, multiple_attempts, final_int]

    [month_act, week_act, three_five_seven, longest, current] = streak(uid)

    return render_template("view.html", 
        values=values, 
        month_act=month_act, 
        week_act=week_act,
        three_five_seven=three_five_seven,
        longest=longest,
        current=current)

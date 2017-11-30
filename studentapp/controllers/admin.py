from flask import Flask
from flask import Markup
from flask import render_template, flash, redirect, session, url_for, request, g, json, jsonify, send_from_directory
from studentapp import app, db
from studentapp.models import UserLogin, UserData, ButtonClicks
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
            return redirect(url_for('example'))
            return uid
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template("admin.html", error=error)



@app.route('/example', methods=['GET', 'POST'])
def example():
    print "made it this far"
    global uid
    uid = int(uid)
    uname = 'uname'
    session['uid'] = uid
    uid = int(uid)
    print uid

    # note! this function does not take input from the search form yet

    login_check = UserData.query.filter_by(user_id=uid).first()

    latest = "latest"
    now = "now"

    if login_check != None:
        latest = str(login_check.login_date)
        latest = latest[0:10]
        now = str(datetime.utcnow())
        now = now[0:10]

    if (login_check != None) and (latest == now):
        print "things are working!"
        uname = login_check.username
        ndays_act = login_check.ndays_act 
        nproblems_attempted = login_check.nproblems_attempted 
        one_attempt = login_check.one_attempt 
        multiple_attempts = login_check.multiple_attempts
        not_completed = login_check.not_completed
        months = login_check.months
        percent_complete = float(one_attempt+multiple_attempts)
        print percent_complete
        total_complete = float(one_attempt+multiple_attempts+not_completed)
        print total_complete
        if total_complete > 0:
            final = float((percent_complete/total_complete)*100)
            print final
            final_int = int(final)
        else: 
            final = 0
            final_int = 0
        print percent_complete, total_complete, final, final_int

        values = [uid, uname, ndays_act, nproblems_attempted, one_attempt, multiple_attempts, not_completed, final_int]
        print values
        
        devicestr = str(request.user_agent)
        devicetup = tuple(filter(None,devicestr.split(' ')))
        devicemessy = devicetup[1]
        device = devicemessy[1:-1]

        browserstr = str(request.user_agent)
        browsertup = tuple(filter(None,devicestr.split(' ')))
        browsermessy = browsertup[11]
        browser = browsermessy[0:-13]

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

        print login_inst.login_date
        print login_button.login_date

    else:
        print "no db entry"
        [uname, ndays_act] = query_romeo(uid, uname)
        uname = uname[1:]
        [months, nproblems_attempted] = query_juliet(uid, uname)
        [one_attempt, multiple_attempts, not_completed] = query_mercutio(uid, uname)

        percent_complete = float(one_attempt+multiple_attempts)
        print "percent complete: ", percent_complete

        total_complete = float(one_attempt+multiple_attempts+not_completed)
        print "total complete: ", total_complete
        if total_complete > 0:
            final = float((percent_complete/total_complete)*100)
            print final
            final_int = int(final)
        else:
            final = 0 
            final_int = 0
        print percent_complete, total_complete, final, final_int

        values = [uid, uname, ndays_act, nproblems_attempted, one_attempt, multiple_attempts, not_completed, final_int]
        print values
        
        devicestr = str(request.user_agent)
        devicetup = tuple(filter(None,devicestr.split(' ')))
        devicemessy = devicetup[1]
        device = devicemessy[1:-1]

        browserstr = str(request.user_agent)
        browsertup = tuple(filter(None,devicestr.split(' ')))
        browsermessy = browsertup[11]
        browser = browsermessy[0:-13]

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

        db.session.add(userdata)
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
        login_data = UserData.query.filter_by(user_id=uid).first()

        print login_inst.login_date
        print login_button.login_date
        print login_data.login_date


    return render_template("example.html", values=values, months=months)



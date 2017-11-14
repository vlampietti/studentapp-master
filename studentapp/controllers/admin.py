from flask import Flask
from flask import Markup
from flask import render_template, flash, redirect, session, url_for, request, g, json, jsonify, send_from_directory
from studentapp import app, db
from studentapp.models import UserLogin, UserData, ButtonClicks
from fake_queries import *
from datetime import datetime

@app.route('/example1', methods=['GET', 'POST'])
def example1():
    print "in example1"
    uid = '534566'
    uname = 'uname'
    session['uid'] = uid
    uid = int(uid)

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


        [uname, ndays_act] = query_romeo(uid, uname)
        uname = uname[1:]
        [months, nproblems_attempted] = query_juliet(uid, uname)
        [one_attempt, multiple_attempts, not_completed] = query_mercutio(uid, uname)

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


    return render_template("example.html", values=values, months=months)


@app.route('/example2', methods=['GET', 'POST'])
def example2():
    print "in example2"
    uname = "uname"
    uid = '534580'
    session['uid'] = uid
    print uid
    uid = int(uid)
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


        [uname, ndays_act] = query_romeo(uid, uname)
        uname = uname[1:]
        [months, nproblems_attempted] = query_juliet(uid, uname)
        [one_attempt, multiple_attempts, not_completed] = query_mercutio(uid, uname)

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


    return render_template("example.html", values=values, months=months)

@app.route('/example3', methods=['GET', 'POST'])
def example3():
    print "in example3"
    uid = '534401'
    uname = 'uname'
    session['uid'] = uid
    uid = int(uid)

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


        [uname, ndays_act] = query_romeo(uid, uname)
        uname = uname[1:]
        [months, nproblems_attempted] = query_juliet(uid, uname)
        [one_attempt, multiple_attempts, not_completed] = query_mercutio(uid, uname)

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


    return render_template("example.html", values=values, months=months)

@app.route('/example4', methods=['GET', 'POST'])
def example4():
    print "in example4"
    uname = "uname"
    uid = '534508'
    session['uid'] = uid
    uid = int(uid)

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


        [uname, ndays_act] = query_romeo(uid, uname)
        uname = uname[1:]
        [months, nproblems_attempted] = query_juliet(uid, uname)
        [one_attempt, multiple_attempts, not_completed] = query_mercutio(uid, uname)

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


    return render_template("example.html", values=values, months=months)
    
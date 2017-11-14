from flask import Flask
from flask import Markup
from flask import render_template, flash, redirect, session, url_for, request, g, json, jsonify, send_from_directory
from studentapp import app, db
from fakedata_functions import *

@app.route('/example1', methods=['GET', 'POST'])
def example1():
    print "in example1"
    uname = "uname"
    uid = '534566'
    session['uid'] = uid
    print uid
    uid = int(uid)
    uname = "uname"
    [uname, ndays_act] = query_romeo(uid, uname)
    uname = uname[1:]
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
    uname = "uname"
    uid = '534580'
    session['uid'] = uid
    print uid
    uid = int(uid)
    uname = "uname"
    [uname, ndays_act] = query_romeo(uid, uname)
    uname = uname[1:]
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
    uid = int(uid)
    uname = "uname"
    [uname, ndays_act] = query_romeo(uid, uname)
    uname = uname[1:]
    print uid, uname
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
    uname = "uname"
    uid = '534508'
    session['uid'] = uid
    print uid
    uid = int(uid)
    uname = "uname"
    [uname, ndays_act] = query_romeo(uid, uname)
    uname = uname[1:]
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
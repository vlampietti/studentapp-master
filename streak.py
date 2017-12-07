from studentapp import app, db
from studentapp.models import *
from flask import render_template, flash, redirect, session, url_for, request, g, json, jsonify, send_from_directory
import calendar
import datetime
from operator import itemgetter
import os

def streak(uid):
	session['uid'] = uid
	print "in streak function for user", uid
	user_data = UserActivity.query.filter_by(user_id=uid).order_by(UserActivity.id.desc()).first()
	daily_activity = user_data.daily_activity


	for x in daily_activity:
		x.encode('UTF8')

	daily_activity = daily_activity[2:]
	daily_activity = daily_activity[:-2]

	daily_activity = daily_activity.split("], [")

	daily_list = []

	for y in daily_activity:
		y = y.split(", ")
		daily_list.append([y[0][1:-1], int(y[1])])

	daily_list = sorted(daily_list, key=itemgetter(0))

	n = ['',0]
	rejects = []

	for dt in daily_list:
		if dt[0] == n[0]:
			if dt[1] >= n[1]:
				rejects.append(n)
			else:
				rejects.append(dt)
		n = dt

	for x in daily_list:
		for y in rejects:
			if x == y:
				daily_list.remove(x)

	first_date = daily_list[0]
	first_date = first_date[0]
	initial_year = int(first_date[0:4])
	initial_month = int(first_date[5:7])

	cal = calendar.Calendar()

	coursecal = []

	monday = []
	tuesday = []
	wednesday = []
	thursday = []
	friday = []
	saturday = []
	sunday = []

	while initial_month <= 12:
		for x in cal.itermonthdays2(initial_year,initial_month):
			if int(x[0]) != 0:
				activity = 0
				weekday = int(x[1])

				for y in daily_list:
					if int(y[0][5:7]) == int(initial_month) and int(y[0][8:10]) == int(x[0]):
						activity = int(y[1])

				eachday = [(str(initial_month)+"-"+str(x[0])),activity,weekday]
				coursecal.append(eachday)
		initial_month+=1

	zeros = []

	for x in coursecal:
		if int(x[1]) == 0:
			zeros.append(x)
		else:
			break

	for y in zeros:
		for x in coursecal:
			if y[0] == x[0] and y[1] == x[1]:
				coursecal.remove(x)

	todaysdate = datetime.datetime.utcnow()
	todaysdate = str(todaysdate)
	todaysmonth = int(todaysdate[5:7])
	todaysday = int(todaysdate[8:10])

	today = str(todaysmonth)+"-"+str(todaysday)

	# this is temporary please remove

	print "the real date is", today

	coursecalupdate = [] 

	for x in coursecal:
		if today != x[0]:
			coursecalupdate.append(x)
		elif today == x[0]:
			coursecalupdate.append(x)
			break

	coursecal = coursecalupdate

	streak_data = []

	for x in coursecal:
		streak_data.append(x[1])

	streak = 0
	allstreaks = []

	for x in streak_data:
		if x > 0:
			streak+=1
		else:
			allstreaks.append(streak)
			streak = 0
	allstreaks.append(streak)

	threestreak=0
	fourstreak=0
	fivestreak=0
	sixstreak=0
	sevenstreak=0
	eightstreak=0
	ninestreak=0
	tenstreak=0

	for y in allstreaks:
		if y >= 3:
			threestreak+=1
			if y >= 4:
				fourstreak+=1
				if y >= 5:
					fivestreak+=1
					if y >= 6:
						sixstreak+=1
						if y >= 7:
							sevenstreak+=1
							if y >= 8:
								eightstreak+=1
								if y >= 9:
									ninestreak+=1
									if y >= 10:
										tenstreak+=1

	print threestreak, fourstreak, fivestreak, sixstreak, sevenstreak, eightstreak, ninestreak, tenstreak

	three_five_seven = [threestreak, fivestreak, sevenstreak]

	# longest streak
	longest = 0

	for x in allstreaks:
		if x > longest:
			longest = x

	# current streak
	current = 1
	if streak_data[len(streak_data)-1] > 0:
		current+=allstreaks[len(allstreaks)-1]

	to_date = int(len(coursecal))

	this_week = []

	for n in range(1,8):
		this_week.append(coursecal[to_date-n])

	this_week_new = []

	for x in this_week:
		if x[2] == 0:
			this_week_new.append(x)
			break
		else:
			this_week_new.append(x)

	this_week = this_week_new


	week_act = []

	for x in this_week:
		week_act.insert(0, x[1])
		

	for z in coursecal:
		if z[2] == 0:
			a = [z[0],z[1]]
			monday.append(a)
		if z[2] == 1:
			tuesday.append(z)
			a = [z[0],z[1]]
		if z[2] == 2:
			wednesday.append(z)
			a = [z[0],z[1]]
		if z[2] == 3:
			thursday.append(z)
			a = [z[0],z[1]]
		if z[2] == 4:
			friday.append(z)
			a = [z[0],z[1]]
		if z[2] == 5:
			saturday.append(z)
			a = [z[0],z[1]]
		if z[2] == 6:
			sunday.append(z)
			a = [z[0],z[1]]

	monday_act = 0
	tuesday_act = 0
	wednesday_act = 0
	thursday_act = 0
	friday_act = 0
	saturday_act = 0
	sunday_act = 0

	for x in monday:
		monday_act+=x[1]
	monday_act = float(monday_act)/float(len(monday))
	monday_act = float(format(monday_act, '.2f'))

	for x in tuesday:
		tuesday_act+=x[1]
	tuesday_act = float(tuesday_act)/float(len(tuesday))
	tuesday_act = float(format(tuesday_act, '.2f'))

	for x in wednesday:
		wednesday_act+=x[1]
	wednesday_act = float(wednesday_act)/float(len(wednesday))
	wednesday_act = float(format(wednesday_act, '.2f'))

	for x in thursday:
		thursday_act+=x[1]
	thursday_act = float(thursday_act)/float(len(thursday))
	thursday_act = float(format(thursday_act, '.2f'))

	for x in friday:
		friday_act+=x[1]
	friday_act = float(friday_act)/float(len(friday))
	friday_act = float(format(friday_act, '.2f'))

	for x in saturday:
		saturday_act+=x[1]
	saturday_act = float(saturday_act)/float(len(saturday))
	saturday_act = float(format(saturday_act, '.2f'))

	for x in sunday:
		sunday_act+=x[1]
	sunday_act = float(sunday_act)/float(len(sunday))
	sunday_act = float(format(sunday_act, '.2f'))



	month_act = [monday_act, tuesday_act, wednesday_act, thursday_act, friday_act, saturday_act, sunday_act]
	
	new_month_act = []

	return month_act, week_act, three_five_seven, longest, current


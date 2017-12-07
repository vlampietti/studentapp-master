from studentapp import app, db
from studentapp.models import *
from query import *
import numpy as np
import datetime
from operator import itemgetter
import calendar
import os
import csv

# pull relevant data for all users from BQ

# person_course_query()

# person_problem_query()

# time_on_task_query()

# calculate relevant variables unique to each user

with open("csv/person_course.csv","rb") as file:
	print "opening file #1"
	filereader = csv.reader(file, delimiter=",")

	uid = ""
	uname = ""
	ndays_act = ""

	for row in filereader:

		uid = row[0]
		uname = row[1]
		ndays_act = row[2]
		#print uid, uname, ndays_act

		attempts = 0
		one_attempt = 0
		multiple_attempts = 0

		completed = 0
		problem_id = 0
		not_completed = 0

		print uid, uname, ndays_act

		with open("csv/person_problem.csv","rb") as filetwo:
			print "opening file #2"
			filetworeader = csv.reader(filetwo, delimiter=",")

			temp_list = []
			problem_list = []
			for rowtwo in filetworeader:
				if str(uid) == rowtwo[0]:
					temp_list.append(rowtwo)

			for x in temp_list:
				completed += 1
				if int(x[1]) > problem_id:
				    problem_id = int(x[1])
				not_completed = problem_id - completed

				attempts = int(x[2])
				if attempts == 1:
					one_attempt += 1
				elif attempts > 1:
					multiple_attempts += 1

		problem_list = [completed, not_completed, one_attempt, multiple_attempts]

		with open("csv/time_on_task.csv","rb") as filethree:
			print "opening file #3"
			filethreereader = csv.reader(filethree, delimiter=",")

			og_list = []
			for rowthree in filethreereader:
				if str(uname) == rowthree[0]:
					og_list.append(rowthree)

			binary_list = []
			todays_date = str(datetime.datetime.utcnow())
			todays_date = todays_date[0:10]

			for u in og_list:
				video_time = 0
				problem_time = 0
				text_time = 0
				dt = str(u[1])
				if u[2] != 'None':
					video_time += 1
				if u[3] != 'None':
					problem_time += 1
				if u[4] != 'None':
					text_time += 1

				glom = video_time + problem_time + text_time + 1
				glom_by_date = [dt, glom]
				binary_list.append(glom_by_date)

			if (UserData.query.filter_by(user_id=uid).first()) != None:

				user_data = UserData.query.filter_by(user_id=uid).first()

				user_data.query_date = todays_date
				user_data.ndays_act = ndays_act
				user_data.completed = problem_list[0]
				user_data.not_completed = problem_list[1]
				user_data.one_attempt = problem_list[2]
				user_data.multiple_attempts = problem_list[3]

				print "successful update"

				db.session.merge(user_data)
				db.session.flush()
				db.session.commit()

				user_act = UserActivity.query.filter_by(user_id=uid).first()

				user_act.query_date = todays_date
				user_act.daily_activity = str(binary_list)

				print user_act.daily_activity

				print "another successful one"

				db.session.merge(user_act)
				db.session.flush()
				db.session.commit()

				print UserData.query.filter_by(user_id=uid).order_by(UserData.id.desc()).all()
				user_act = UserActivity.query.filter_by(user_id=uid).order_by(UserActivity.id.desc()).all()

				print user_act

			else:
				print "this is a new case!"

				userdata = UserData(
					user_id = uid,
					username = uname,
					query_date = todays_date,
					ndays_act = ndays_act,
					completed = problem_list[0],
					not_completed = problem_list[1],
					one_attempt = problem_list[2],
					multiple_attempts = problem_list[3])

				db.session.add(userdata)
				db.session.commit()

				useractivity = UserActivity(
					user_id = uid,
					username = uname,
					query_date = todays_date,
					daily_activity = str(binary_list))

				db.session.add(useractivity)
				db.session.commit()

				login_data = UserData.query.filter_by(user_id=uid).order_by(UserData.id.desc()).first()
				print login_data.user_id, login_data.query_date
				print login_data.username, login_data.ndays_act
				print login_data.completed, login_data.not_completed, login_data.one_attempt, login_data.multiple_attempts

				user_act = UserActivity.query.filter_by(user_id=uid).order_by(UserActivity.id.desc()).first()
				print user_act.daily_activity

				# this is temporary

			user_data = UserActivity.query.filter_by(user_id=uid).order_by(UserActivity.id.desc()).first()
			daily_activity = user_data.daily_activity


			for x in daily_activity:
				x.encode('UTF8')

			print "this is your daily activity", daily_activity

			print str(daily_activity)

			if str(daily_activity) != '[]':
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

				print "this far"


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

				twostreak=0
				threestreak=0
				fourstreak=0
				fivestreak=0
				sixstreak=0
				sevenstreak=0
				eightstreak=0
				ninestreak=0
				tenstreak=0

				streak_list = []


				for y in allstreaks:
					if y >= 10:
						tenstreak+=1
					elif y >= 9:
						ninestreak+=1
					elif y >= 8:
						eightstreak+=1
					elif y >= 7:
						sevenstreak+=1
					elif y >= 6:
						sixstreak+=1
					elif y >= 5:
						fivestreak+=1
					elif y >= 4:
						fourstreak+=1
					elif y >= 3:
						threestreak+=1
					elif y >= 2:
						twostreak+=1

				streak_list = [twostreak, threestreak, fourstreak, fivestreak, sixstreak, sevenstreak, eightstreak, ninestreak, tenstreak]

			else:
				streak_list = [0,0,0,0,0,0,0,0,0]
				print "this is your streak", streak_list

			with open("csv/streak_data.csv","a") as f:
				f.write(str(streak_list[0])+","+str(streak_list[1])+","+str(streak_list[2])+","+str(streak_list[3])+","+str(streak_list[4])+","+str(streak_list[5])+","+str(streak_list[6])+","+str(streak_list[7])+","+str(streak_list[8])+"\n")


        	
        print "done looping through all users!"

    	# os.remove("csv/person_course.csv")
    	# os.remove("csv/person_problem.csv")
    	# os.remove("csv/time_on_task.csv")

    	# print "all files removed"





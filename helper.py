from studentapp import app, db
from studentapp.models import *
from query import *
import numpy as np
from datetime import datetime
import os
import csv

# pull relevant data for all users from BQ

person_course_query()
print "it should be working.."

person_course_day_query()
print "This one too.."

person_problem_query()
print "On a roll my friend!"

time_on_task_query()
print "Ah, yes."


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
			todays_date = str(datetime.utcnow())
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

    		for v in binary_list:
    			month_day = str(v[0])

    		userdata = UserData(
    			user_id = uid,
    			username = uname,
    			login_date = todays_date, 
            	ndays_act = ndays_act, 
            	completed = problem_list[0], 
            	not_completed = problem_list[1],
            	one_attempt = problem_list[2], 
            	multiple_attempts = problem_list[3], 
            	daily_activity = str(binary_list))

    		db.session.add(userdata)
        	db.session.commit()

        	login_data = UserData.query.filter_by(user_id=uid).order_by(UserData.id.desc()).first()
        	print login_data.user_id, login_data.login_date
        	print login_data.username, login_data.ndays_act
        	print login_data.completed, login_data.not_completed, login_data.one_attempt, login_data.multiple_attempts

    	
    	print "done looping through all users!"

    	os.remove("csv/person_course.csv")
    	os.remove("csv/person_course_day.csv")
    	os.remove("csv/person_problem.csv")
    	os.remove("csv/time_on_task.csv")

    	print "all files removed"





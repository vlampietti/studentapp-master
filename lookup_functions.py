import string
import csv


def match_uid_to_uname(uid):
    uname=""
    with open("uid-uname.csv","rU") as file:
        filereader = csv.reader(file, delimiter=",")
        for row in filereader:
            if str(uid) == row[0]:
                uname=str(row[1])

    print "in match_uid_to_name"
    return(uid,uname)

def lookup_days_active(uid):
    num1 = 0
    with open("ophelia.csv","rb") as csvfile:
    	csvreader = csv.reader(csvfile, delimiter=",")
    	for row in csvreader:
    		if str(uid) == row[0]:
    			uname=str(row[1])
    			num1=row[2]

    print "in lookup_days_active"
    return(uid,uname,num1)

def fake_lookup_days_active(uid):
    num1 = 0
    with open("romeo.csv","rb") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",")
        for row in csvreader:
            if str(uid) == row[0]:
                uname=str(row[1])
                num1=row[2]
    print "in fake lookup_days_active"
    return(uid,uname,num1)

def determine_progress(uname):
    prog = 0
    with open("hamlet.csv","rb") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",")
        for row in csvreader:
            prog = int(row[3])

# note that the assumption here is that there are 100 problems in the course:
# sthis can be changed once we have access to actual numbers.

    print "in determine_progress function"
    return uname, prog

def fake_determine_progress(uname):
    prog = 0
    with open("juliet.csv","rb") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",")
        for row in csvreader:
            prog = int(row[2])

# note that the assumption here is that there are 100 problems in the course:
# sthis can be changed once we have access to actual numbers.

    print "in fake determine_progress function"
    return uname, prog

def problems(uid):
    attempts = 0
    one_attempt = 0
    multiple_attempts = 0
    no_attempts = 0

    completed_problems = 0
    problem_id = 0
    not_completed = 0
    date = " "

    with open("polonius.csv","rb") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",")
        for row in csvreader:
            completed_problems += 1
            problem_id = int(row[1])
            not_completed = problem_id - completed_problems

            attempts = int(row[4])
            if int(attempts) == 1:
                one_attempt += 1
            elif int(attempts) > 1:
                multiple_attempts += 1

    print "in problems function"
    return uid, one_attempt, multiple_attempts, not_completed

def fake_problems(uid):
    attempts = 0
    one_attempt = 0
    multiple_attempts = 0
    no_attempts = 0

    completed_problems = 0
    problem_id = 0
    not_completed = 0
    date = " "

    with open("mercutio.csv","rb") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",")
        for row in csvreader:
            completed_problems += 1
            problem_id = int(row[1])
            not_completed = problem_id - completed_problems

            attempts = int(row[4])
            if int(attempts) == 1:
                one_attempt += 1
            elif int(attempts) > 1:
                multiple_attempts += 1

    print "in fake problems function"
    print uid, one_attempt, multiple_attempts, not_completed
    return uid, one_attempt, multiple_attempts, not_completed

def monthly_problems(uid):
    dt = ""
    mon = 0
    one_attempt = 0
    multiple_attempts = 0


    with open("polonius.csv","rb") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",")
        for row in csvreader:
            dt = str(row[5])
            mon = int(dt[5:7])
            if mon == 10:
                attempts = int(row[4])
                if int(attempts) == 1:
                    one_attempt += 1
                elif int(attempts) > 1:
                    multiple_attempts += 1

        print "the number of single attempts in october is %i" % one_attempt
        print "the number of multiple attempts in october is %i" % multiple_attempts

    print "in monthly_problems"
    print mon
    return uid, mon

def fake_monthly_problems(uid):
    dt = ""
    mon = 0
    one_attempt = 0
    multiple_attempts = 0

    with open("mercutio.csv","rb") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",")
        print "in fake monthly_problems"
        for row in csvreader:
            dt = str(row[5])
            mon = int(dt[5:7])
            if mon == 10:
                attempts = int(row[4])
                if int(attempts) == 1:
                    one_attempt += 1
                elif int(attempts) > 1:
                    multiple_attempts += 1

        print "the number of single attempts in october is %i" % one_attempt
        print "the number of multiple attempts in october is %i" % multiple_attempts

    print "in fake monthly_problems"
    return uid, mon


def dates_active(uname):
    jan = 0
    feb = 0
    mar = 0
    apr = 0
    may = 0
    jun = 0
    jul = 0
    aug = 0
    sep = 0
    october = 0
    nov = 0
    dec = 0

    with open("hamlet.csv","rb") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",")
        for row in csvreader:
            date = row[4]
            month = int(date[5:7])
            if month == 1:
                jan +=1
            if month == 2:
                feb+=1
            if month == 3:
                mar+=1
            if month == 4:
                apr +=1
            if month == 5:
                may+=1
            if month == 6:
                jun+=1
            if month == 7:
                jul+=1
            if month == 8:
                aug+=1
            if month == 9:
                sep+=1
            if month == 10:
                october+=1
            if month == 11:
                nov+=1
            if month == 12:
                dec+=1
    print "in dates_active function"
    return uname, jan, feb, mar, apr, may, jun, jul, aug, sep, october, nov, dec

def fake_dates_active(uname):
    print "in fake dates active"
    jan = 0
    feb = 0
    mar = 0
    apr = 0
    may = 0
    jun = 0
    jul = 0
    aug = 0
    sep = 0
    october = 0
    nov = 0
    dec = 0

    with open("juliet.csv","rb") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",")
        for row in csvreader:
            date = row[3]
            month = int(date[5:7])
            if month == 1:
                jan +=1
            if month == 2:
                feb+=1
            if month == 3:
                mar+=1
            if month == 4:
                apr +=1
            if month == 5:
                may+=1
            if month == 6:
                jun+=1
            if month == 7:
                jul+=1
            if month == 8:
                aug+=1
            if month == 9:
                sep+=1
            if month == 10:
                october+=1
            if month == 11:
                nov+=1
            if month == 12:
                dec+=1
    print "in fake dates_active function"
    return uname, jan, feb, mar, apr, may, jun, jul, aug, sep, october, nov, dec


if __name__ == '__main__':
    uid = raw_input("please provide a user id: ")
    uid = int(uid)
    lookup_days_active(uid)

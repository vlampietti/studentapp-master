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
    num2 = 0
    with open("ophelia.csv","rb") as csvfile:
    	csvreader = csv.reader(csvfile, delimiter=",")
    	for row in csvreader:
    		if str(uid) == row[0]:
    			uname=str(row[1])
    			num1=row[2]
                num2=row[3]


    print "in lookup_days_active"
    return(uid,uname,num1,num2)

def determine_progress(uname):
    prog = 0
    with open("hamlet.csv","rb") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",")
        for row in csvreader:
            prog = int(row[3])

# note that the assumption here is that there are 100 problems in the course:
# sthis can be changed once we have access to actual numbers.

    print "in determine_progress"
    return uname, prog


if __name__ == '__main__':
    uid = raw_input("please provide a user id: ")
    uid = int(uid)
    lookup_days_active(uid)

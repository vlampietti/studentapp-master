import string
import csv

def lookup_days_active(uid):
    #read the csv file
    num1=0
    num2=0
    with open("data-placeholder.csv","rb") as csvfile:
    	csvreader = csv.reader(csvfile, delimiter=",")
    	for row in csvreader:
    		if str(uid) == row[0]:
    			num1=row[1]
    			num2=row[2]

    print "in lookup_days_active"
    return(num1,num2)

if __name__ == '__main__':
    uid = raw_input("please provide a user id: ")
    uid = int(uid)
    lookup_days_active(uid)

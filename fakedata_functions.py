import string
import csv

def query_romeo(uid, uname):
    import uuid
    from google.cloud import bigquery
    client = bigquery.Client()
    print "in query_romeo"
    
    query = """
        #standardSQL
        SELECT
            user_id, username, ndays_act, nvideos_total_watched, sum_dt
        FROM `fake_deidentified_data.person_course`
        WHERE user_id = @uid
        """
    query_job = client.run_async_query(
        str(uuid.uuid4()),
        query,
        query_parameters=(
            bigquery.ScalarQueryParameter('uid', 'INT64', uid),
            bigquery.ScalarQueryParameter(
                'uname', 'STRING', uname)))
    query_job.use_legacy_sql = False
    query_job.begin()
    query_job.result()

    destination_table = query_job.destination
    destination_table.reload()

    f = open("romeo.csv", "w+")
    for row in destination_table.fetch_data():
        f.write(str(row[0])+","+str(row[1])+","+str(row[2])+","+str(row[3])+","+str(row[4])+"\n")
        romeo_list = [row[1], row[2]]
        print romeo_list
        return romeo_list
    f.close()

def query_juliet(uid, uname):
    import uuid
    from google.cloud import bigquery
    ham_client = bigquery.Client()
    print "in query_juliet"
    print uid, uname
    
    query = """
        #standardSQL
        SELECT
            username, nvideo, nproblems_attempted, date
        FROM `fake_deidentified_data.person_course_day`
        WHERE username = @uname
        ORDER BY nproblems_attempted;
        """

    query_job = ham_client.run_async_query(
        str(uuid.uuid4()),
        query,
        query_parameters=(
            bigquery.ScalarQueryParameter('uid', 'INT64', uid),
            bigquery.ScalarQueryParameter(
                'uname', 'STRING', uname)))
    query_job.use_legacy_sql = False
    query_job.begin()
    query_job.result()

    destination_table2 = query_job.destination
    destination_table2.reload()
    h = open("juliet.csv", "w+")
    for row in destination_table2.fetch_data():
        h.write(str(row[0])+","+str(row[1])+","+str(row[2])+","+str(row[3])+"\n")
    h.close()

def query_mercutio(uid, uname):
    import uuid
    from google.cloud import bigquery
    ham_client = bigquery.Client()
    print "in query_mercutio"
    print uid, uname

    query = """
        #standardSQL
        SELECT
            user_id, problem_nid, problem_raw_score, problem_pct_score, n_attempts, date
        FROM `fake_deidentified_data.person_problem`
        WHERE user_id = @uid
        ORDER BY problem_nid;
        """

    query_job = ham_client.run_async_query(
        str(uuid.uuid4()),
        query,
        query_parameters=(
            bigquery.ScalarQueryParameter('uid', 'INT64', uid),
            bigquery.ScalarQueryParameter(
                'uname', 'STRING', uname)))
    query_job.use_legacy_sql = False
    query_job.begin()
    query_job.result()

    destination_table3 = query_job.destination
    destination_table3.reload()
    g = open("mercutio.csv", "w+")
    for row in destination_table3.fetch_data():
        g.write(str(row[0])+","+str(row[1])+","+str(row[2])+","+str(row[3])+","+str(row[4])+","+str(row[5])+"\n")
    g.close()

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

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

    for row in destination_table.fetch_data():
        uname = row[1]
        romeo_list = [row[1], row[2]]
        print romeo_list
        return romeo_list


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

    juliet_list = []

    for row in destination_table2.fetch_data():
        juliet = [row[0], row[2], row[3]]
        juliet_list.append(juliet)

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

    nproblems_attempted = 0
    for y in juliet_list:
        nproblems_attempted = int(y[1])

    for x in juliet_list:
        dt = str(x[2])
        month = int(dt[5:7])

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


    print "calculating months..."
    months = [jan, feb, mar, apr, may, jun, jul, aug, sep, october, nov, dec]
    print months
    return months, nproblems_attempted

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

    polonius_list = []
    for row in destination_table3.fetch_data():
        polonius = [row[0], row[1], row[4], row[5]]
        polonius_list.append(polonius)

    attempts = 0
    one_attempt = 0
    multiple_attempts = 0

    completed_problems = 0
    problem_id = 0
    not_completed = 0

    for x in polonius_list:
        completed_problems += 1
        problem_id = int(x[1])
        not_completed = problem_id - completed_problems

        attempts = int(x[2])
        if attempts == 1:
            one_attempt += 1
        elif attempts > 1:
            multiple_attempts += 1

    print "in this damn thing"
    print uid, one_attempt, multiple_attempts, not_completed
    return one_attempt, multiple_attempts, not_completed


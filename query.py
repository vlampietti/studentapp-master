from studentapp import app, db
from datetime import datetime

def person_course_query():
    import uuid
    from google.cloud import bigquery
    client = bigquery.Client()
    print "in the FIRST query"

    query = """
        #standardSQL
        SELECT
            user_id, username, ndays_act
        FROM `deidentified_data.person_course`
        ORDER BY user_id;
        """

    query_job = client.run_async_query(
        str(uuid.uuid4()),
        query)
    query_job.use_legacy_sql = False
    query_job.begin()
    query_job.result()

    dest_table = query_job.destination
    dest_table.reload()

    f = open("csv/person_course.csv","w+")

    for row in dest_table.fetch_data():
        f.write(str(row[0])+","+str(row[1][1:])+","+str(row[2])+"\n")
    f.close()

def person_course_day_query():
    import uuid
    from google.cloud import bigquery
    client = bigquery.Client()
    print "in the SECOND(!) query"

    query = """
        #standardSQL
        SELECT
            username, nproblems_attempted, first_event
        FROM `deidentified_data.person_course_day`
        ORDER BY username;
        """

    query_job = client.run_async_query(
        str(uuid.uuid4()),
        query)
    query_job.use_legacy_sql = False
    query_job.begin()
    query_job.result()

    dest_table = query_job.destination
    dest_table.reload()

    f = open("csv/person_course_day.csv","w+")

    for row in dest_table.fetch_data():
        f.write(str(row[0])+","+str(row[1])+","+(str(row[2])[0:10])+"\n")
    f.close()

def person_problem_query():
    import uuid
    from google.cloud import bigquery
    client = bigquery.Client()
    print "in the ~THIRD~ query"

    query = """
        #standardSQL
        SELECT
            user_id, problem_nid, n_attempts, date
        FROM `deidentified_data.person_problem`
        ORDER BY user_id;
        """

    query_job = client.run_async_query(
        str(uuid.uuid4()),
        query)
    query_job.use_legacy_sql = False
    query_job.begin()
    query_job.result()

    dest_table = query_job.destination
    dest_table.reload()

    f = open("csv/person_problem.csv","w+")

    for row in dest_table.fetch_data():
        f.write(str(row[0])+","+str(row[1])+","+str(row[2])+","+str(row[3])+"\n")
    f.close()

def time_on_task_query():
    import uuid
    from google.cloud import bigquery
    client = bigquery.Client()
    print "in the fourth, and last, query"

    query = """
        #standardSQL
        SELECT
            username, date, serial_video_time_30, serial_problem_time_30, serial_text_time_30
        FROM `deidentified_data.time_on_task`
        ORDER BY username;
        """

    query_job = client.run_async_query(
        str(uuid.uuid4()),
        query)
    query_job.use_legacy_sql = False
    query_job.begin()
    query_job.result()

    dest_table = query_job.destination
    dest_table.reload()

    f = open("csv/time_on_task.csv","w+")

    for row in dest_table.fetch_data():
        f.write(str(row[0])+","+str(row[1])+","+str(row[2])+","+str(row[3])+","+str(row[4])+"\n")
    f.close()


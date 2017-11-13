def query_romeo(uid, uname):
    import uuid
    from google.cloud import bigquery
    client = bigquery.Client()
    print "in query_romeo"
    print uid, uname
    
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
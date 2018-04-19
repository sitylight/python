import psycopg2
import datetime
import os
import subprocess
import urllib.request
import zipfile


def urlretrieveDBDump(url, saveFileName):
    try:
        if os.path.isfile(saveFileName):
            print('file existed')
            m_time = os.path.getmtime(saveFileName)
            m_date = datetime.date.fromtimestamp(m_time)
            print(m_date)
            if m_date == datetime.date.today():
                print('file had been downloaded before, no need to download again')
            else:
                urllib.request.urlretrieve(url, saveFileName)
        else:
            urllib.request.urlretrieve(url, saveFileName)
        zip_file_object = zipfile.ZipFile(saveFileName, 'r')
        zip_file_object.extract(zip_file_object.namelist()[0])
        print('extract ' + saveFileName + ' to get ' + zip_file_object.namelist()[0])
        return (zip_file_object.namelist()[0])
    except:
        print('fail to retrieve db dump')


def get_database_name(pre_fix):
    weekDay = datetime.datetime.today().weekday() + 1
    print('current week day is ' + str(weekDay))
    if pre_fix is None:
        pre_fix = 'cbx6_u_'
    print(pre_fix + str(weekDay))
    return (pre_fix + str(weekDay))


def createDatabase(host, port, database_name):
    drop_user_sql = "drop user if exists " + database_name
    drop_database_sql = "drop database if exists " + database_name
    create_user_sql = "create user " + database_name + " with password 'p'"
    create_database_sql = "create database " + database_name + " WITH OWNER " + database_name + " ENCODING 'UTF8'"
    grant_privileges_sql = "GRANT ALL PRIVILEGES ON DATABASE " + database_name + " TO " + database_name + ""
    # connect to postgres and create new database
    conn_string = "host='" + host + "' user='postgres' password='p' port='" + port + "'"
    try:
        print('connect to postgres with :' + conn_string)
        conn = psycopg2.connect(conn_string)
        conn.autocommit = True
        cur = conn.cursor()
    except:
        print('can not connec to postgresql')
    try:
        # print('try to remove existed user and database, then create new user and database')
        print('execute ' + drop_database_sql)
        cur.execute(drop_database_sql)
        print('execute ' + drop_user_sql)
        cur.execute(drop_user_sql)
        print('execute ' + create_user_sql)
        cur.execute(create_user_sql)
        print('execute ' + create_database_sql)
        cur.execute(create_database_sql)
        print('execute ' + drop_user_sql)
        cur.execute(grant_privileges_sql)
        cur.close()
        conn.close()
        print(database_name + ' is created')
    except:
        print('create database failure, please check whether others are connecting')
    # connect to new created database and create function
    try:
        print('connect to database "' + database_name + '" to create "uuid_generate_v4()" function')
        conn_string2 = "host='" + host + "' user='postgres' password='p' port='" + port + "' dbname='" \
                       + database_name + "'"
        conn2 = psycopg2.connect(conn_string2)
        conn2.autocommit = True
        cur2 = conn2.cursor()
        uuid_function = "CREATE OR REPLACE FUNCTION uuid_generate_v4() RETURNS uuid AS '$libdir/uuid-ossp', " \
                        "'uuid_generate_v4'LANGUAGE c VOLATILE STRICT COST 1"
        cur2.execute(uuid_function)
        cur2.close()
        conn2.close()
        print('function is created')
    except:
        print('fail to create "uuid_generate_v4()"')


def restore(host, port, dumpName, database_string):
    current_dir = os.getcwd() + '\\'
    command = 'pg_restore -h ' + host + ' -p ' + port + ' -U ' + database_string + ' -O -d ' + database_string \
              + ' ' + current_dir + dumpName
    print('restore db with command: ' + command)
    my_env = os.environ.copy()
    my_env["PGPASSWORD"] = 'p'
    print('start to restore db dump')
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=my_env)
    stdout, stderr = p.communicate()
    poll = p.poll()
    if poll is None:
        print('restore still running')
    else:
        print("db " + database_string + " restored")


url = 'http://192.168.2.55:8081/view/CBX6/job/cbx6-db-upgrade/lastSuccessfulBuild/artifact/' \
      'cbx-build-dbdump-upgrade-pgsql/release_dbdump/full-upgrade.dump.zip'
host = '192.168.5.132'
# host = 'localhost'
# host = '192.168.1.105'
port = '5432'
saveFileName = 'upgrade.zip'

try:
    dumpFileName = urlretrieveDBDump(url, saveFileName)
    database_name = get_database_name('cbx6_u_')
    createDatabase(host, port, database_name)
    restore(host, port, dumpFileName, database_name)
except:
    print('fail to restore db')

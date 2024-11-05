from configparser import ConfigParser
import psycopg2
import datetime

def select_hours_by_person():
    con = connect()
    if con is not None:
        cursor = con.cursor()

        SQL = 'SELECT consultant_name, start_time, end_time FROM entries;'

        cursor.execute(SQL, )
        data = cursor.fetchall()
        cursor.close()
        con.close()
        return data

def select_hours_by_customer():
    con = connect()
    if con is not None:
        cursor = con.cursor()

        SQL = 'SELECT customer_name, start_time, end_time FROM entries;'

        cursor.execute(SQL, )
        data = cursor.fetchall()
        cursor.close()
        con.close()
        return data

def config(filename="database.ini", section="postgresql"):
    parser = ConfigParser()
    parser.read(filename)
    db = {}

    if parser.has_section(section):
        params = parser.items(section)
        for p in params:
            db[p[0]] = p[1]
    else:
        raise Exception(f"Section {section} not found in file {filename}")
    
    return db

def connect():
    con = None

    try:
        con = psycopg2.connect(**config())
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        if con is not None:
            con.close()
    
    return con

def reporting():
    print(select_hours_by_person())
    print(select_hours_by_customer())

reporting()
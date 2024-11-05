from configparser import ConfigParser
import psycopg2
import pandas as pd
import datetime

def select_hours_by_person():
    con = connect()
    if con is not None:
        cursor = con.cursor()

        SQL = 'SELECT consultant_name, start_time, end_time, lunch_break FROM entries;'

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
    persondata = pd.DataFrame(select_hours_by_person())
    persondata = persondata.rename(columns={0:'Consultant_name', 1:'Start_time', 2:'End_time', 3:'Lunch_break'})
    persondata = persondata.assign(Work_hours=(persondata['End_time']-persondata['Start_time']-persondata['Lunch_break']*pd.to_timedelta(30, unit='min')))
    persondata['Work_hours'] = persondata['Work_hours'].dt.total_seconds().div(3600).round(2).apply("{:g}h".format)
    persondata = persondata[['Consultant_name', 'Work_hours']].groupby(by='Consultant_name').sum()
    print(persondata)
    
    #print(select_hours_by_customer())

reporting()
from configparser import ConfigParser
import psycopg2
import pandas as pd
from datetime import datetime

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

        SQL = 'SELECT customer_name, start_time, end_time, lunch_break FROM entries;'

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
    persondata = persondata.assign(Date=persondata['Start_time'].dt.date)
    persondata = persondata[['Consultant_name', 'Work_hours', 'Date']].groupby(by=['Consultant_name', 'Date']).sum()
    persondata['Work_hours'] = persondata['Work_hours'].dt.total_seconds().div(3600).round(2).apply("{:g}h".format)
    
    customerdata = pd.DataFrame(select_hours_by_customer())
    customerdata = customerdata.rename(columns={0:'Customer_name', 1:'Start_time', 2:'End_time', 3:'Lunch_break'})
    customerdata = customerdata.assign(Work_hours=(customerdata['End_time']-customerdata['Start_time']-customerdata['Lunch_break']*pd.to_timedelta(30, unit='min')))
    customerdata = customerdata.assign(Date=customerdata['Start_time'].dt.date)
    customerdata = customerdata[['Customer_name', 'Work_hours', 'Date']].groupby(by=['Customer_name', 'Date']).sum()
    customerdata['Work_hours'] = customerdata['Work_hours'].dt.total_seconds().div(3600).round(2).apply("{:g}h".format)

    filename = f"timelog_{datetime.now().strftime('%Y-%m-%d')}.txt"
    persondata.to_csv(filename, sep='\t', index=True)  # Writes to a tab-delimited file
    print("Data has been written to {filename}")

    filename = f"timelog_{datetime.now().strftime('%Y-%m-%d')}.txt"
    customerdata.to_csv(filename, sep='\t', index=True)  # Writes to a tab-delimited file
    print("Data has been written to {filename}")

reporting()
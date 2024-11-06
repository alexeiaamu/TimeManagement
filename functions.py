

import psycopg2
import pandas as pd
from psycopg2.extras import RealDictCursor
from config import config
from datetime import datetime

def db_create_log(start_time: datetime, end_time: datetime, lunch_break: bool, consultant_name: str, customer_name: str):
    con = None
    try:
        con = psycopg2.connect(**config())
        cursor = con.cursor(cursor_factory=RealDictCursor)
        
        SQL = '''
        INSERT INTO entries (start_time, end_time, lunch_break, consultant_name, customer_name)
        VALUES (%s, %s, %s, %s, %s);
        '''
        
        cursor.execute(SQL, (start_time, end_time, lunch_break, consultant_name, customer_name))
        con.commit()
        
        result = {"message": "Time logged successfully"}
        
        cursor.close()
        return result  
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        return {"error": "Database error occurred"}
    finally:
        if con is not None:
            con.close()

def total_hours(consultant_id):
    con = None
    try:
        con = psycopg2.connect(**config())
        cursor = con.cursor(cursor_factory=RealDictCursor)
        
        SQL = '''
        SELECT start_time, end_time, lunch_break FROM entries WHERE consultant_id = %s;
        '''

        data = (consultant_id, )

        hours = pd.DataFrame(cursor.execute(SQL, data).fetchall())
        hours['Total_hours'] = hours.assign(Work_hours=(hours[1]-hours[0]-hours[2]*pd.to_timedelta(30, unit='min')))
        
        total = hours['Total_hours'].sum()

        SQL = '''
        INSERT INTO total_hours (consultant_id, total_hours) VALUES (%s, %s)
        '''
        data = (consultant_id, total)

        cursor.execute(SQL, data)
        con.commit()
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        return {"error": "Database error occurred"}
    finally:
        if con is not None:
            con.close()
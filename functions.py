import psycopg2
from psycopg2.extras import RealDictCursor
from config import config
from datetime import datetime

import psycopg2
from psycopg2.extras import RealDictCursor
from config import config
from datetime import datetime

def db_create_log(start_time: datetime, end_time: datetime, lunch_break: bool, consultant_name: str, customer_name: str):
    con = None
    try:
        con = psycopg2.connect(**config())
        cursor = con.cursor(cursor_factory=RealDictCursor)
        
        SQL = '''
        INSERT INTO timemanagement (start_time, end_time, lunch_break, consultant_name, customer_name)
        VALUES (%s, %s, %s, %s, %s);
        '''
        
        cursor.execute(SQL, (start_time, end_time, lunch_break, consultant_name, customer_name))
        con.commit()
        
        result = {"message": "Time logged successfully"}
        
        cursor.close()
        return result  # Return as a dictionary (not JSON string)
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        return {"error": "Database error occurred"}
    finally:
        if con is not None:
            con.close()

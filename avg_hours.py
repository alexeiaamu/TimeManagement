import psycopg2
import pandas as pd
from psycopg2.extras import RealDictCursor
from config import config
from datetime import datetime

def avg_hours():
    con=None
    try:
        con = psycopg2.connect(**config())
        cursor = con.cursor(cursor_factory=RealDictCursor)
    

        # SQL query to calculate the average hours worked per day per consultant
        query = """
        SELECT 
            consultant_id,
            consultant_name,
            AVG(
                (EXTRACT(EPOCH FROM (end_time - start_time)) / 3600) - 
                CASE WHEN lunch_break THEN 0.5 ELSE 0 END
            ) AS avg_hours_per_day
        FROM 
            entries
        GROUP BY
            consultant_id, consultant_name, DATE(start_time);
        """

        # Execute the query
        cursor.execute(query)
        

        # Fetch the results
        results = cursor.fetchall()

        # Print results or return them
        for row in results:
            consultant_id = row['consultant_id']
            consultant_name = row['consultant_name']
            avg_hours_per_day = row['avg_hours_per_day']
            print(f"Consultant {consultant_name} (ID: {consultant_id}) averaged {avg_hours_per_day} hours per day.")

        cursor.close()
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        return {"error": "Database error occurred"}

    finally:
        if con is not None:
            con.close()

avg_hours()
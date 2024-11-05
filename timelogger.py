from flask import Flask, request
from functions import db_create_log

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return {"index": True}

@app.route("/timelog", methods=['POST'])
def create_log():
    try: 
        data = request.get_json()
        start_time = data['start_time']
        end_time = data['end_time']
        lunch_break = data['lunch_break']
        consultant_name=data['consultant_name']
        customer_name=data['customer_name']
        db_create_log(start_time, end_time, lunch_break, consultant_name, customer_name)
        return {"Time logged"}
    except:
        return {"error logging time, please check input and try again"}
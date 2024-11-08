from flask import Flask, request, jsonify
from functions import db_create_log, total_hours

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return jsonify({"index": True})

@app.route("/timelog", methods=['POST'])
def create_log():
    try: 
        data = request.get_json()
        start_time = data['start_time']
        end_time = data['end_time']
        lunch_break = data['lunch_break']
        consultant_id= data['consultant_id']
        consultant_name = data['consultant_name']
        customer_id= data['customer_id']
        customer_name= data['customer_name']
        db_create_log(start_time, end_time, lunch_break, consultant_id, consultant_name, customer_id, customer_name)
        total_hours(consultant_id)
        return jsonify({"message": "Time logged successfully"})
    except Exception as e:
        return jsonify({"error": f"Error logging time: {str(e)}"}), 400

if __name__ == "__main__":
    app.run(debug=True)

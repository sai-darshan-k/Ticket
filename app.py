from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder="templates", static_url_path="")
CORS(app)

# Initialize seats
seats = [{"id": i, "status": "Available", "category": "Regular", "price": 100} for i in range(1, 51)]

@app.route("/")
def index():
    return send_from_directory("templates", "index.html")

@app.route("/seats", methods=["GET"])
def get_seats():
    return jsonify(seats)

@app.route("/book", methods=["POST"])
def book_seat():
    seat_id = request.json.get("id")
    for seat in seats:
        if seat["id"] == seat_id:
            if seat["status"] == "Available":
                seat["status"] = "Booked"
                return jsonify({"message": f"Seat {seat_id} booked successfully!"}), 200
            else:
                return jsonify({"message": f"Seat {seat_id} is already booked!"}), 400
    return jsonify({"message": "Seat not found!"}), 404

@app.route("/cancel", methods=["POST"])
def cancel_booking():
    seat_id = request.json.get("id")
    for seat in seats:
        if seat["id"] == seat_id:
            if seat["status"] == "Booked":
                seat["status"] = "Available"
                return jsonify({"message": f"Booking for seat {seat_id} canceled!"}), 200
            else:
                return jsonify({"message": f"Seat {seat_id} is not booked!"}), 400
    return jsonify({"message": "Seat not found!"}), 404

@app.route("/summary", methods=["GET"])
def booking_summary():
    booked_seats = [seat for seat in seats if seat["status"] == "Booked"]
    total_revenue = sum(seat["price"] for seat in booked_seats)
    booked_percentage = (len(booked_seats) / len(seats)) * 100
    return jsonify({"total_revenue": total_revenue, "booked_percentage": booked_percentage})

if __name__ == "__main__":
    app.run(debug=True)

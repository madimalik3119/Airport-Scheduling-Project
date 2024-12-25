from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Sample flight data
flights = [
    {'flightNumber': 'AA101', 'origin': 'New York', 'destination': 'London', 'time': '10:00 AM', 'status': 'Ready'},
    {'flightNumber': 'BA202', 'origin': 'London', 'destination': 'New York', 'time': '02:00 PM', 'status': 'On the Way'},
    {'flightNumber': 'CA303', 'origin': 'Los Angeles', 'destination': 'Tokyo', 'time': '11:30 AM', 'status': 'Cancelled'},
    {'flightNumber': 'DA404', 'origin': 'Paris', 'destination': 'Berlin', 'time': '01:15 PM', 'status': 'Ready'},
]

bookings = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/flights', methods=['GET'])
def get_flights():
    return jsonify(flights)

@app.route('/book', methods=['POST'])
def book_flight():
    data = request.get_json()
    flight_number = data['flightNumber']
    passenger_name = data['passengerName']
    passenger_email = data['passengerEmail']

    flight = next((f for f in flights if f['flightNumber'] == flight_number), None)

    if flight and flight['status'] == 'Ready':
        bookings.append({'flightNumber': flight_number, 'passengerName': passenger_name, 'passengerEmail': passenger_email})
        flight['status'] = 'Booked'
        return jsonify({'message': 'Booking successful!'}), 200
    else:
        return jsonify({'message': 'Flight not available for booking.'}), 400

@app.route('/cancel', methods=['POST'])
def cancel_booking():
    data = request.get_json()
    flight_number = data['flightNumber']

    booking_index = next((i for i, b in enumerate(bookings) if b['flightNumber'] == flight_number), None)

    if booking_index is not None:
        flight = next((f for f in flights if f['flightNumber'] == bookings[booking_index]['flightNumber']), None)
        flight['status'] = 'Ready'
        bookings.pop(booking_index)
        return jsonify({'message': 'Booking cancelled successfully!'}), 200
    else:
        return jsonify({'message': 'No booking found for the provided flight number.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
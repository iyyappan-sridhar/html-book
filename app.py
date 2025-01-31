from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/booking_app'
db = SQLAlchemy(app)

# Define Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)  # Store as string for simplicity
    time = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default='available')

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable=False)

# Create Tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/appointments', methods=['GET'])
def get_appointments():
    appointments = Appointment.query.all()
    return jsonify([{
        'id': app.id,
        'date': app.date,
        'time': app.time,
        'status': app.status
    } for app in appointments])

@app.route('/api/book', methods=['POST'])
def book_appointment():
    data = request.json
    user = User(name=data['name'], email=data['email'])
    db.session.add(user)
    db.session.commit()

    booking = Booking(user_id=user.id, appointment_id=data['appointment_id'])
    db.session.add(booking)

    appointment = Appointment.query.get(data['appointment_id'])
    appointment.status = 'booked'
    db.session.commit()

    return jsonify({'message': 'Booking successful!'})

if __name__ == '__main__':
    app.run(debug=True)
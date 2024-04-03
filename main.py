from flask import Flask, render_template, url_for, redirect, request
import sqlite3

app = Flask(__name__)

# Function to create a database connection
def get_db_connection():
    conn = sqlite3.connect('registrations.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create the database table
def create_table():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS registrations (
                    id INTEGER PRIMARY KEY,
                    full_name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL,
                    destination TEXT NOT NULL,
                    activities TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Initialize the database
create_table()

@app.route('/', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        full_name = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        destination = request.form['destination']
        activities = ', '.join(request.form.getlist('activities'))

        # Insert registration data into the database
        conn = get_db_connection()
        conn.execute('INSERT INTO registrations (full_name, email, password, destination, activities) VALUES (?, ?, ?, ?, ?)',
                     (full_name, email, password, destination, activities))
        conn.commit()
        conn.close()

        return redirect('/destinations')
    return render_template('registration.html')

@app.route('/destinations')
def destinations():
    destinations = [
        {'name': 'United Kingdom', 'image': 'uk.jpg'},
        {'name': 'France', 'image': 'france.jpg'},
        {'name': 'Italy', 'image': 'italy.jpg'},
        {'name': 'United States', 'image': 'usa.jpg'},
        {'name': 'Algeria', 'image': 'algeria.jpg'}
    ]
    return render_template('destinations.html', destinations=destinations)

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Handle form submission here
    return 'Form submitted successfully!'

@app.route('/trip_plan/<destination_name>')
def trip_plan(destination_name):
    return render_template('trip_plan.html', destination_name=destination_name)

if __name__ == '__main__':
    app.run(debug=True)



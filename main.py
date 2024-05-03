from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my secrect key is nothing'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///registrations.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

db = SQLAlchemy(app)

# Registration Model
class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(50), nullable=False)
    activities = db.Column(db.String(200), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

# Registration Form Class
class RegistrationForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    destination = SelectField('Destination', choices=[('uk', 'United Kingdom'), ('fr', 'France'), ('it', 'Italy'), ('us', 'United States'), ('al', 'Algeria')], validators=[DataRequired()])
    activities = StringField('Activities', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Route for index page
@app.route('/')
def index():
    return render_template('index.html')

# Route for registration page
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        full_name = form.full_name.data
        email = form.email.data
        password = form.password.data
        destination = form.destination.data
        activities = form.activities.data
        
        # Insert registration data into the database
        registration = Registration(full_name=full_name, email=email, password=password,
                                    destination=destination, activities=activities)
        try:
            db.session.add(registration)
            db.session.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('destinations'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error occurred: {str(e)}', 'danger')
    return render_template('registration.html', form=form)

# Route for displaying destinations
@app.route('/destinations')
def destinations():
    destinations = [
        {'name': 'United Kingdom', 'image': 'uk.jpg'},
        {'name': 'France', 'image': 'france.jpg'},
        {'name': 'Italy', 'image': 'italy.jpg'},
        {'name': 'United States', 'image': 'usa.jpg'},
        {'name': 'Algeria', 'image': 'algeria.jpg'},
        {'name': 'Spain', 'image': 'spain.webp'},
        {'name': 'Japan', 'image': 'japan.webp'}
    ]
    return render_template('destinations.html', destinations=destinations)

# Trip Plan page
@app.route('/trip_plan')
def trip_plan():
    return render_template('trip_plan.html')

# Route for London UK page
@app.route('/london_uk')
def london_uk():
    return render_template('london_uk.html') 

# Trip Plan 2 page
@app.route('/trip_plan2')
def trip_plan2():
    return render_template('trip_plan2.html')


# Route for france page page
@app.route('/france')
def france():
    return render_template('france.html') 

# Form page
@app.route('/form')
def form():
    return render_template('form.html')

# Form page
@app.route('/submission')
def submission():
    return render_template('submission.html')


# Submit form route
@app.route('/submit', methods=['POST'])
def submit():
    # Handle form submission here
    return 'Form submitted successfully!'

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

# Internal server error
@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables before running the app
    app.run(debug=True)

from flask import Flask, request, jsonify, render_template, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from extension import db
from models import User

app = Flask(__name__) 

repair_request = []

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data_testing.db' 
app.secret_key = "user_name_-123"
db.init_app(app)  # Initialize the database with the Flask app  


@app.route('/') 
def index():
    return render_template('index.html')  # Render the index template


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if email and password:
            user = User.query.filter_by(email=email).first() 
            
            if user and check_password_hash(user.password, password): 
                session['username'] = user.username 
                flash('Login successful!', 'success') 
                return redirect('/')
            
            else: 
                flash('Invalid email or password', 'danger')
        else:
            flash('Please enter both email and password', 'warning') 
            return redirect('/sigup')
        
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup(): 
    
    if request.method == 'POST': 
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if username and email and password:
            existing_user = User.query.filter_by(email=email).first() 
            
            if existing_user:
                flash('Email already exists', 'danger') 
                return redirect('/signup')
            
            new_user = User(username=username, email=email, password=generate_password_hash(password)) 
            db.session.add(new_user) 
            db.session.commit() 
            flash('Registration successful!', 'success') 
            return redirect('/login')
        
        else:
            flash('Please fill in all fields', 'warning') 
            return redirect('/signup')
        
    return render_template('signup.html')  # Render the signup template

if __name__ == '__main__': 
    with app.app_context():
        db.create_all()  # Create database tables if they don't exist
    app.run(debug=True)  # Run the Flask application in debug mode 
    
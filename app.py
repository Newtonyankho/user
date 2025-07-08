from flask import Flask, render_template, request, redirect, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Connect to database
def get_db():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize DB if not exists
def init_db():
    with get_db() as db:
        db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fullname TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            );
        ''')
        db.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        ''')

# Home page (login/register)
@app.route('/')
def index():
    return render_template('index.html')

# Handle registration
@app.route('/register', methods=['POST'])
def register():
    fullname = request.form['fullname']
    email = request.form['email']
    password = request.form['password']
    confirm = request.form['confirm_password']

    if password != confirm:
        flash("Passwords do not match")
        return redirect('/')

    hashed = generate_password_hash(password)
    db = get_db()
    try:
        db.execute('INSERT INTO users (fullname, email, password) VALUES (?, ?, ?)',
                   (fullname, email, hashed))
        db.commit()
        flash("Account created. Please login.")
    except sqlite3.IntegrityError:
        flash("Email already registered")
    return redirect('/')

# Handle login
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

    if user and check_password_hash(user['password'], password):
        session['user'] = user['fullname']
        return redirect('/dashboard')
    else:
        flash("Invalid email or password")
        return redirect('/')

# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')
    db = get_db()
    posts = db.execute('SELECT * FROM posts ORDER BY timestamp DESC').fetchall()
    return render_template('dashboard.html', username=session['user'], posts=posts)

# Handle post submission
@app.route('/post', methods=['POST'])
def post():
    if 'user' not in session:
        return redirect('/')
    content = request.form['content']
    db = get_db()
    db.execute('INSERT INTO posts (username, content) VALUES (?, ?)', (session['user'], content))
    db.commit()
    return redirect('/dashboard')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

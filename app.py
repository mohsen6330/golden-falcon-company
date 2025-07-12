import sqlite3
from flask import Flask, render_template, request, redirect, url_for, make_response

app = Flask(__name__)

app.secret_key = 'your-secret-key-here'

@app.route('/')
def index():
    if request.cookies.get('logged_in') == 'true':
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()
    conn.close()
    if user:
        response = make_response(redirect(url_for('dashboard')))
        response.set_cookie('logged_in', 'true')
        return response
    else:
        return redirect(url_for('index', error='Invalid username or password'))

@app.route('/dashboard')
def dashboard():
    if request.cookies.get('logged_in') == 'true':
        return render_template('dashboard.html')
    else:
        return redirect(url_for('index'))

@app.route('/users')
def users_page():
    if request.cookies.get('logged_in') == 'true':
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT username, password FROM users")
        users = c.fetchall()
        conn.close()
        return render_template('users.html', users=users)
    else:
        return redirect(url_for('index'))

# New route for the invoice page
@app.route('/invoice')
def invoice_page():
    if request.cookies.get('logged_in') == 'true':
        return render_template('invoice.html')
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('index')))
    response.set_cookie('logged_in', '', expires=0)
    return response

if __name__ == '__main__':
    app.run(debug=True)
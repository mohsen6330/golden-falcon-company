import sqlite3
from flask import Flask, render_template, request, redirect, url_for, make_response

app = Flask(__name__)

# Route to display the login page
@app.route('/')
def index():
    return render_template('login.html')

# Route to handle user login
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
        # If login is successful, create a response and set a cookie
        response = make_response(redirect(url_for('dashboard')))
        response.set_cookie('logged_in', 'true')
        return response
    else:
        # If login fails, redirect back to the login page with a message
        return redirect(url_for('index', error='Invalid username or password'))

# Route to display the dashboard page
@app.route('/dashboard')
def dashboard():
    # Check if the user is logged in
    if request.cookies.get('logged_in') == 'true':
        return render_template('dashboard.html')
    else:
        return redirect(url_for('index'))

# Route to display the users page
@app.route('/users')
def users_page():
    # Check if the user is logged in
    if request.cookies.get('logged_in') == 'true':
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT username, password FROM users")
        users = c.fetchall()
        conn.close()
        
        return render_template('users.html', users=users)
    else:
        return redirect(url_for('index'))

# Route to handle logout
@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('index')))
    response.set_cookie('logged_in', '', expires=0) # Clear the cookie by setting an expiration date in the past
    return response

if __name__ == '__main__':
    # You must use a secret key for session management, even if we are not using Flask's session.
    # It's a good practice for security.
    app.secret_key = 'your-secret-key-here' 
    app.run(debug=True)
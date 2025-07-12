import sqlite3
from flask import Flask, render_template, request, redirect, url_for, make_response

app = Flask(__name__)

app.secret_key = 'your-secret-key-here'

@app.route('/')
def index():
    if request.cookies.get('logged_in') == 'true':
        return redirect(url_for('dashboard'))
    return render_template('index.html')

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
        return render_template('index.html', error='Invalid username or password')

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

@app.route('/inventory/add_product', methods=['GET', 'POST'])
def add_product_page():
    if request.cookies.get('logged_in') == 'true':
        if request.method == 'POST':
            barcode = request.form.get('barcode')
            name = request.form.get('name')
            price = request.form.get('price')
            quantity = 0 # Quantity is now set to 0 by default
            try:
                conn = sqlite3.connect('database.db')
                c = conn.cursor()
                c.execute("INSERT INTO products (barcode, name, price, quantity) VALUES (?, ?, ?, ?)",
                          (barcode, name, price, quantity))
                conn.commit()
                conn.close()
                return render_template('add_product.html', success="تمت إضافة المنتج بنجاح.")
            except sqlite3.IntegrityError:
                return render_template('add_product.html', error="رمز الباركود موجود بالفعل. الرجاء استخدام رمز آخر.")
            except Exception as e:
                return render_template('add_product.html', error=f"حدث خطأ: {e}")
        return render_template('add_product.html')
    else:
        return redirect(url_for('index'))

@app.route('/inventory/add_warehouse')
def add_warehouse_page():
    if request.cookies.get('logged_in') == 'true':
        return render_template('add_warehouse.html')
    else:
        return redirect(url_for('index'))

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
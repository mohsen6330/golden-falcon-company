from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# دالة لإنشاء الاتصال بقاعدة البيانات وإنشاء الجدول إذا لم يكن موجوداً
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# استدعاء الدالة عند تشغيل التطبيق
init_db()

@app.route('/', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # هنا سنقوم بالتحقق من بيانات المستخدم في قاعدة البيانات
        return redirect(url_for('dashboard_page'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        
        # حفظ بيانات المستخدم في قاعدة البيانات
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()

        return redirect(url_for('dashboard_page'))
    
    return render_template('register.html')

@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')

@app.route('/users')
def users_page():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    # استرجاع جميع المستخدمين من قاعدة البيانات
    c.execute("SELECT username, password FROM users")
    users = c.fetchall()
    conn.close()
    
    return render_template('users.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
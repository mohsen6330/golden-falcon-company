from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(f"Login attempt - Username: {username}, Password: {password}")
        return "تم استقبال بيانات تسجيل الدخول بنجاح!"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(f"Registration attempt - Username: {username}, Password: {password}")
        return "تم استقبال بيانات التسجيل بنجاح!"
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
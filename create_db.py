import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users
             (username TEXT, password TEXT)''')

c.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin')")

conn.commit()
conn.close()

print("Database and users table created successfully.")
print("Admin user 'admin' with password 'admin' has been added.")
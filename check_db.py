import sqlite3

try:
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()
    print("Tables found in database:")
    for table in tables:
        print(table[0])
    conn.close()
except sqlite3.Error as e:
    print(f"An error occurred: {e}")
    
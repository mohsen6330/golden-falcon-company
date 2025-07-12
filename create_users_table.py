import sqlite3

def create_users_table():
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        c.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin')")
        conn.commit()
        print("Users table created and default user added successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    create_users_table()
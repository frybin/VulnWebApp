import os
import sqlite3

DATABASE_PATH=os.path.join(os.path.dirname(__file__), 'database.db')

def connect_db():
    return sqlite3.connect(DATABASE_PATH)

def create_tables():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('''
            CREATE TABLE IF NOT EXISTS user(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(32),
            password VARCHAR(32)
            )''')
    conn.commit()
    conn.close()


def init_data():
    users = [
        ('Admin', 'Letmein')
    ]
    conn = connect_db()
    cur = conn.cursor()
    cur.executemany('INSERT INTO `user` VALUES(NULL,?,?)', users)
    conn.commit()
    conn.close()


def init():
    create_tables()
    init_data()

if __name__ == "__main__":
    init()
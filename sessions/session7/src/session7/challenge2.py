import sqlite3
from contextlib import contextmanager

@contextmanager
def connectDB():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    try:    
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
        );
        ''')
        yield cursor
    finally:
        conn.commit()
        conn.close()

if __name__ == "__main__":
    with connectDB():
        print("Done")
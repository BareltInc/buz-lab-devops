import os
import sqlite3

def get_db_path():
    return os.environ.get('DB_PATH', 'db.sqlite')

def init_db():
    db_path = get_db_path()
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS words (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        arabic TEXT NOT NULL,
        translation TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()
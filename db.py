import sqlite3

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        purpose TEXT,
        person TEXT,
        amount INTEGER
    )
    """)

    conn.commit()
    conn.close()
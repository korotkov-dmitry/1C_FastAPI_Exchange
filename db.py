import sqlite3
import os

DB_PATH = os.getenv("DB_PATH", "data/data_from1c.db")

def init_db():
    os.makedirs("data", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS data1c (
        id INTEGER PRIMARY KEY,
        uid TEXT NOT NULL UNIQUE,
        title TEXT NOT NULL,
        done INTEGER NOT NULL
    )
    """)

    conn.commit()
    conn.close()

def get_data():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT uid, title, done FROM data1c")
    rows = cursor.fetchall()

    conn.close()

    # преобразуем в список словарей
    return [
        {
            "uid": row["uid"],
            "title": row["title"],
            "done": bool(row["done"])
        }
        for row in rows
    ]

def add_data(data: dict):
    conn = sqlite3.connect(DB_PATH, timeout=10)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO data1c (uid, title, done)
    VALUES (?, ?, ?)
    ON CONFLICT(uid) DO UPDATE SET
        title = excluded.title,
        done  = excluded.done
    """, (
        data["uid"],
        data["title"],
        int(data["done"])
    ))

    conn.commit()
    conn.close()

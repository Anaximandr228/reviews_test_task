import sqlite3


def init_db():
    con = sqlite3.connect("reviews.db")
    cursor = con.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS reviews (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      text TEXT NOT NULL,
                      sentiment TEXT NOT NULL,
                      created_at TEXT NOT NULL)
                      """)
    con.commit()
    con.close()

import sqlite3
from datetime import datetime


def get_db_connection():
    return sqlite3.connect("reviews.db")


def insert_review(con, text, sentiment, created_at):
    cursor = con.cursor()
    cursor.execute(
        'INSERT INTO reviews (text, sentiment, created_at) VALUES (?, ?, ?)',
        (text, sentiment, created_at)
    )
    review_id = cursor.lastrowid
    con.commit()
    return review_id


def get_reviews(conn, sentiment_filter=None):
    cursor = conn.cursor()

    if sentiment_filter:
        cursor.execute(
            'SELECT id, text, sentiment, created_at FROM reviews WHERE sentiment = ?',
            (sentiment_filter,)
        )
    else:
        cursor.execute('SELECT id, text, sentiment, created_at FROM reviews')

    reviews = []
    for row in cursor.fetchall():
        reviews.append({
            'id': row[0],
            'text': row[1],
            'sentiment': row[2],
            'created_at': row[3]
        })

    return reviews

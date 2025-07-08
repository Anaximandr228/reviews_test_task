import sqlite3
from datetime import datetime
from flask import Flask, jsonify, request
from create_db import init_db


app = Flask(__name__)


def get_db():
    con = sqlite3.connect("rewiews.db")
    return con


def compare_sentiment(text):
    positive_words = ['хорош', 'любл']
    negative_words = ['плох', 'ненавиж']

    text_lower = text.lower()

    for word in positive_words:
        if word in text_lower:
            return 'positive'

    for word in negative_words:
        if word in text_lower:
            return 'negative'

    return 'neutral'

@app.route('/reviews', methods=['POST'])
def create_review():
    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({'error': 'Invalid data, "text" field is required'}), 400

    text = data['text']
    sentiment = compare_sentiment(text)
    created_at = datetime.utcnow().isoformat()

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO reviews (text, sentiment, created_at) VALUES (?, ?, ?)',
        (text, sentiment, created_at)
    )
    review_id = cursor.lastrowid
    conn.commit()

    review = {
        'id': review_id,
        'text': text,
        'sentiment': sentiment,
        'created_at': created_at
    }

    conn.close()
    return jsonify(review), 201


@app.route('/reviews', methods=['GET'])
def get_reviews():
    sentiment_filter = request.args.get('sentiment')

    con = get_db()
    cursor = con.cursor()

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

    con.close()
    return jsonify(reviews)


if __name__ == '__main__':
    init_db()
    app.run()

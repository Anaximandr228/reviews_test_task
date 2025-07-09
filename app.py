import sqlite3
from datetime import datetime
from flask import Flask, jsonify, request
from create_db import init_db
from storage import get_db_connection, insert_review

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

    con = get_db_connection()
    try:
        review_id = insert_review(con, text, sentiment, created_at)

        review = {
            'id': review_id,
            'text': text,
            'sentiment': sentiment,
            'created_at': created_at
        }

        return jsonify(review), 201
    finally:
        con.close()


@app.route('/reviews', methods=['GET'])
def get_reviews():
    sentiment_filter = request.args.get('sentiment')

    conn = get_db_connection()
    try:
        reviews = get_reviews(conn, sentiment_filter)
        return jsonify(reviews)
    finally:
        conn.close()


if __name__ == '__main__':
    init_db()
    app.run()

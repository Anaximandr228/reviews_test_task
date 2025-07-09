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

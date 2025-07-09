def compare_sentiment(text):
    positive_words = ['хорош', 'любл']
    negative_words = ['плох', 'ненавиж']

    text_lower = text.lower()

    has_positive = any(word in text_lower for word in positive_words)
    has_negative = any(word in text_lower for word in negative_words)

    # Если есть и положительные, и отрицательные слова - возвращаем neutral
    if has_positive and has_negative:
        return 'neutral'

    # Если только положительные
    if has_positive:
        return 'positive'

    # Если только отрицательные
    if has_negative:
        return 'negative'

    # Если ничего не найдено
    return 'neutral'
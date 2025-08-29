from flask import Flask, request, jsonify
from src.sentiment_analysis import analyze_mood
from src.openlibrary_test import fetch_books_from_openlibrary

app = Flask(__name__)

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    mood_text = data.get('mood_text', '')
    if not mood_text:
        return jsonify({'error': 'No mood_text provided'}), 400
    mood_query, confidence = analyze_mood(mood_text)
    books = fetch_books_from_openlibrary(mood_query, limit=10)
    return jsonify({
        'mood': mood_query,
        'confidence': confidence,
        'books': books
    })

if __name__ == '__main__':
    app.run(debug=True)

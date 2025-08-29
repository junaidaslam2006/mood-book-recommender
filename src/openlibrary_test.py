
import requests

def fetch_books_from_openlibrary(mood_query, limit=10):
    # Search OpenLibrary by subject (mood_query)
    url = f"https://openlibrary.org/subjects/{mood_query}.json?limit={limit}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            books = [book['title'] for book in data.get('works', [])]
            return books
        else:
            return []
    except Exception:
        return []

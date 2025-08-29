import streamlit as st
from src.sentiment_analysis import analyze_mood
from src.openlibrary_test import fetch_books_from_openlibrary

st.title("📚 Mood Book Recommender")

user_input = st.text_input("Describe how you feel today:")

if st.button("Get Book Suggestions"):
    if user_input:
        mood_query, confidence = analyze_mood(user_input)

        st.write(f"**Detected Mood Keyword:** {mood_query}")
        st.write(f"**Confidence:** {confidence:.2f}")

        st.subheader("📖 Recommended Books:")
        books = fetch_books_from_openlibrary(mood_query, limit=10)
        
        if books:
            for book in books:
                st.write(f"- {book}")
        else:
            st.write("No books found. Try a different mood.")

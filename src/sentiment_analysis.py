import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"

def analyze_mood(user_input):
    # Use a free model from OpenRouter (e.g., openrouter/auto)
    try:
        response = openai.ChatCompletion.create(
            model="openrouter/auto",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that detects the user's mood and suggests a book category keyword for OpenLibrary. Respond ONLY with a JSON object: {mood: <mood>, confidence: <confidence>, keyword: <book_category>}. Do not add any explanation or extra text."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=100
        )
        content = response.choices[0].message["content"]
        print("LLM raw response:", content)  # Debug print
        import json
        try:
            result = json.loads(content)
            mood_query = result.get("keyword", "general")
            confidence = float(result.get("confidence", 0.8))
            return mood_query, confidence
        except Exception as parse_error:
            print("Error parsing LLM response:", parse_error)
            # Fallback: try to extract keyword from text
            import re
            keyword_match = re.search(r'keyword\s*[:=]\s*["\']?(\w+)["\']?', content, re.IGNORECASE)
            if keyword_match:
                mood_query = keyword_match.group(1)
            else:
                # Try to extract mood from text
                mood_match = re.search(r'mood\s*[:=]\s*["\']?(\w+)["\']?', content, re.IGNORECASE)
                mood_query = mood_match.group(1) if mood_match else "general"
            # Try to extract confidence
            conf_match = re.search(r'confidence\s*[:=]\s*([0-9\.]+)', content, re.IGNORECASE)
            confidence = float(conf_match.group(1)) if conf_match else 0.5
            return mood_query, confidence
    except Exception as api_error:
        print("Error calling LLM API:", api_error)
        return "general", 0.5


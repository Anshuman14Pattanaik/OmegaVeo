# main.py
import os
import requests
import wikipedia
from dotenv import load_dotenv
import google.generativeai as genai

# ----------------- LOAD ENV + CONFIG GEMINI -----------------
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY not set in environment variables")

genai.configure(api_key=GOOGLE_API_KEY)

# Use a model that your key supports (from your check_models.py output)
GEMINI_MODEL_NAME = "models/gemini-2.5-flash"


# ----------------- HELPER FUNCTIONS -----------------
def get_weather(city: str) -> str:
    """Call OpenWeather and return a short description string."""
    if not OPENWEATHER_API_KEY:
        return "Weather API key not set."

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"}

    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        hum = data["main"]["humidity"]
        return f"Weather in {city}: {desc}, {temp}°C, humidity {hum}%."
    except Exception as e:
        return f"Could not fetch weather for {city}: {e}"


def get_wikipedia_summary(topic: str, sentences: int = 3) -> str:
    """Get a short summary from Wikipedia."""
    try:
        return wikipedia.summary(topic, sentences=sentences)
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Topic '{topic}' is ambiguous. Some options: {e.options[:5]}"
    except Exception as e:
        return f"Could not fetch Wikipedia summary: {e}"


def answer_query(query: str) -> str:
    """
    Simple 'agent' logic without LangChain:
    - If question mentions 'weather in <city>', call weather API.
    - Always try to get a Wikipedia summary.
    - Send everything to Gemini to write the final answer.
    """
    query_lower = query.lower()

    # Very basic weather intent + city extraction
    weather_info = ""
    if "weather" in query_lower and " in " in query_lower:
        city_part = query_lower.split(" in ", 1)[1]
        city = city_part.split("?")[0].split(".")[0].strip().title()
        if city:
            weather_info = get_weather(city)

    wiki_info = get_wikipedia_summary(query)

    prompt = f"""
You are OmegaVeo, a helpful research assistant.

User question:
{query}

Wikipedia information:
{wiki_info}

Weather information (if relevant):
{weather_info}

Using the information above, write a clear, concise answer for the user.
If something is missing or uncertain, say so honestly.
"""

    try:
        model = genai.GenerativeModel(GEMINI_MODEL_NAME)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error while calling Gemini model: {e}"

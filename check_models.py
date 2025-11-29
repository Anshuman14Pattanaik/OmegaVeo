import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise RuntimeError("GOOGLE_API_KEY not set in .env")

genai.configure(api_key=api_key)

print("google-generativeai version:", genai.__version__)
print("Available models:")
for m in genai.list_models():
    print(m.name, "->", m.supported_generation_methods)
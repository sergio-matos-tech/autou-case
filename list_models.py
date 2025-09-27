import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

print("--- Modelos disponíveis para sua chave de API ---")
for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)
print("-------------------------------------------------")

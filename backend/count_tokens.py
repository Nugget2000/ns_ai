import os
import google.generativeai as genai

def load_env():
    try:
        with open('.env') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
    except FileNotFoundError:
        pass

load_env()

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY not found in environment")
    exit(1)

genai.configure(api_key=api_key)

try:
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    
    with open('emanuel_prompt.txt', 'r', encoding='utf-8') as f:
        text = f.read()
        
    response = model.count_tokens(text)
    print(f"Token count: {response.total_tokens}")
    
except Exception as e:
    print(f"Error: {e}")

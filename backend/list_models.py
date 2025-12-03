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
    print("Listing models that support countTokens:")
    for m in genai.list_models():
        if 'countTokens' in m.supported_generation_methods:
            print(m.name)
            
    # Try with 'models/gemini-1.5-flash' explicitly if it wasn't tried before
    # But let's just list first.
    
except Exception as e:
    print(f"Error: {e}")

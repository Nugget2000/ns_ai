import sys
import os

# Add the current directory to sys.path so we can import app
sys.path.append(os.getcwd())

from app.services.gemini import get_emanuel_prompt

def test_prompt_loading():
    print("Testing prompt loading...")
    prompt = get_emanuel_prompt()
    if prompt and len(prompt) > 0:
        print("Successfully loaded prompt.")
        print(f"Prompt length: {len(prompt)}")
        print(f"First 50 chars: {prompt[:50]}")
    else:
        print("Failed to load prompt or prompt is empty.")

if __name__ == "__main__":
    test_prompt_loading()

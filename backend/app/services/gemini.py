import os
import google.generativeai as genai
from typing import AsyncGenerator

# Configure Gemini
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("Warning: GEMINI_API_KEY not set")

genai.configure(api_key=API_KEY)

# Initialize model with system instruction
model = genai.GenerativeModel(
    "gemini-2.5-flash",
    system_instruction="Your name is Emanuel and I will try to help. The answers are short and consise and always 100% correct, never lie or come up with answes."
)

async def generate_emanuel_response(prompt: str) -> AsyncGenerator[str, None]:
    """
    Generates a streaming response from Emanuel (Gemini).
    """
    try:
        response = await model.generate_content_async(prompt, stream=True)
        async for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"Error: {str(e)}"

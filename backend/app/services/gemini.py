import os
import time
import traceback

from google import genai
from google.genai import types
from typing import AsyncGenerator

# Configure Gemini
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("Warning: GEMINI_API_KEY not set")

client = genai.Client(api_key=API_KEY)

def get_emanuel_prompt():
    """Reads the Emanuel prompt from the local text file."""
    return """You are Emanuel, an AI assistant for the Nightscout and Loop community.
              Explicitly only answer using the information in the following context.
              Always answer with clickable links and clear instructions.
              If the answer is not in the context, state that you don't know based on the available information."""



# generate a response from Emanuel (Gemini) using search store
async def generate_emanuel_response(prompt: str) -> AsyncGenerator[str, None]:
    """
    Generates a streaming response from Emanuel (Gemini).
    Yields JSON strings:
    - {"type": "prompt", "text": "..."} (once at start)
    - {"type": "content", "text": "..."} (streaming)
    - {"type": "usage", "input_tokens": ..., "output_tokens": ...} (at end)
    """
    import json
    try:
        
        # 1. Send the system prompt first
        system_instruction = get_emanuel_prompt()
        yield json.dumps({"type": "prompt", "text": system_instruction}) + "\n"

        # Use the async client: client.aio.models.generate_content
        # Correct arguments for google-genai SDK
        # We use stream=True if supported, but let's try non-streaming first to fix the TypeError.
        # If we want streaming, we might need to check the SDK docs or trial and error.
        # For now, we will yield the whole response as one chunk.

        # File name will be visible in citations
        file_search_store = client.file_search_stores.create(config={'display_name': 'emanuel_search_store'})

        operation = client.file_search_stores.upload_to_file_search_store(
            file='emanuel_prompt.txt',
            file_search_store_name=file_search_store.name,
            config={
                'display_name' : 'emanuel_prompt',
            }
        )

        while not operation.done:
            print("Uploading file...")
            time.sleep(1)
            operation = client.operations.get(operation)
            

        print("File uploaded successfully")
        
        response = await client.aio.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                tools=[
            types.Tool(
                file_search=types.FileSearch(
                    file_search_store_names=[file_search_store.name]
                )
            )
        ]
            )
        )
        
        if response.text:
            yield json.dumps({"type": "content", "text": response.text}) + "\n"
        
        # Usage metadata
        if response.usage_metadata:
             yield json.dumps({
                "type": "usage", 
                "input_tokens": response.usage_metadata.prompt_token_count,
                "output_tokens": response.usage_metadata.candidates_token_count
            }) + "\n"
        
    except Exception as e:
        print(f"Error: {e}")
        print(traceback.format_exc())
        yield json.dumps({"type": "error", "text": str(e)}) + "\n"

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
              Always answer with clickable links from where you got the information and clear instructions.
              Always reference the source and extract time of the information if available.
              Ex:
              Source: 
                 URL: https://www.loopnlearn.org/sl-build/
                 Extraction Time: 2025-11-28 07:55:19
                 
              If the answer is not in the context, state that you don't know based on the available information."""

def get_file_store_info():
    """
    Gets information about all available file search stores.
    Returns list of dicts, each with size_mb, upload_date, and display_name.
    """
    try:
        file_search_stores = client.file_search_stores.list()
        stores_info = []
        
        for store in file_search_stores:
            # Convert size_bytes to MB
            size_mb = store.size_bytes / (1024 * 1024) if store.size_bytes else 0.0
            
            # Use update_time as upload date (or create_time if update_time is not available)
            upload_date = store.update_time if hasattr(store, 'update_time') and store.update_time else (
                store.create_time if hasattr(store, 'create_time') and store.create_time else None
            )
            
            stores_info.append({
                "size_mb": round(size_mb, 2),
                "upload_date": upload_date,
                "display_name": store.display_name
            })
        
        return stores_info
    except Exception as e:
        print(f"Error getting file store info: {e}")
        print(traceback.format_exc())
        return []



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


        # check if file exists
        if not os.path.exists('emanuel_prompt.txt'):
            print("info: there is no emanuel_prompt.txt in this environment.")

        # delete all file search stores
        #print("Deleting all file search stores")
        #for file_search_store in client.file_search_stores.list():
        #    print(f"deleting...{file_search_store.name}")
        #    client.file_search_stores.delete(name=file_search_store.name, config={"force": True})

        # check if file search store exists and has content
        print("Checking for file in emanuel_scrape_store")
        file_search_stores = client.file_search_stores.list()
        file_search_store = None
        for store in file_search_stores:
            if store.display_name == 'emanuel_scrape_store':
                file_search_store = store
                break

        
        if file_search_store:
            print(f"File found in emanuel_scrape_store. name={file_search_store.name} size_bytes={file_search_store.size_bytes} display_name={file_search_store.display_name}. created={file_search_store.create_time} updated={file_search_store.update_time}")
            if not file_search_store.size_bytes or file_search_store.size_bytes == 0:
                print("Error: emanuel_scrape_store is empty.")
                yield json.dumps({"type": "error", "text": "Emanuel's knowledge base is empty. Please run the scraper to update it."}) + "\n"
                return
        else:
            print("No file search store found.")
            yield json.dumps({"type": "error", "text": "Emanuel's knowledge base (file_search_store) not found. Please run the scraper."}) + "\n"
            return



        print("generating response...")        
        response = await client.aio.models.generate_content_stream(
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
        
        async for chunk in response:
            if chunk.text:
                yield json.dumps({"type": "content", "text": chunk.text}) + "\n"
            
            # Usage metadata can come in chunks or at the end
            if chunk.usage_metadata:
                 yield json.dumps({
                    "type": "usage", 
                    "input_tokens": chunk.usage_metadata.prompt_token_count,
                    "output_tokens": chunk.usage_metadata.candidates_token_count
                }) + "\n"

        print("Done")
        
    except Exception as e:
        print(f"Error: {e}")
        print(traceback.format_exc())
        yield json.dumps({"type": "error", "text": str(e)}) + "\n"

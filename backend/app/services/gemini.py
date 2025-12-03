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
            raise HTTPException(status_code=404, detail="File not found")

        # delete all file search stores
        #print("Deleting all file search stores")
        #for file_search_store in client.file_search_stores.list():
        #    print(f"deleting...{file_search_store.name}")
        #    client.file_search_stores.delete(name=file_search_store.name, config={"force": True})

        # list the file search stores
        print("Listing file search stores")
        for file_search_store in client.file_search_stores.list():
            print(f"file search store: {file_search_store}")


        file_search_stores = client.file_search_stores.list()
        check_file_search_store = [file_search_store for file_search_store in file_search_stores if file_search_store.display_name == 'emanuel_scrape_store']
           

        # upload file if file doesnt exists in emanuel_search_store
        print("Checking for file in emanuel_scrape_store")
        if [file_search_store for file_search_store in file_search_stores if file_search_store.display_name == 'emanuel_scrape_store']:
            print(f"File found in emanuel_scrape_store. name={file_search_store.name} size_bytes={file_search_store.size_bytes} display_name={file_search_store.display_name}. created={file_search_store.create_time} updated={file_search_store.update_time}")
        else:
            print("No file store found, creating...")
            file_search_store = client.file_search_stores.create(config={'display_name': 'emanuel_scrape_store'})

            print("File not found in emanuel_scrape_store, uploading...")
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


        print("generating response...")        
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

        print("Done")
        
    except Exception as e:
        print(f"Error: {e}")
        print(traceback.format_exc())
        yield json.dumps({"type": "error", "text": str(e)}) + "\n"

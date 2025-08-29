import os
import sys
from dotenv import load_dotenv
from google import genai
from constants import *

load_dotenv()
api_key=os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

import os
import sys
from dotenv import load_dotenv
from google import genai
from constants import *

load_dotenv()
api_key=os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def main():
    if len(sys.argv) <= 1:
        print("Must provide a prompt as the first argument")
        sys.exit(1)
    user_prompt = sys.argv[1]
    verbose = None
    if "--verbose" in sys.argv:
        verbose = True
        
    content = client.models.generate_content(model=GEMINI_MODEL, contents=user_prompt)
    print(content.text)
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {content.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {content.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()

import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from constants import *
from functions.get_files_info import schema_get_files_info

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

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
        ]
    )
        
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt, tools=[available_functions]),
    )
    print(response.text)
    for function_call_part in response.function_calls:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()

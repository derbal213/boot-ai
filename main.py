import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from constants import *
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python import schema_run_python

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
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python
        ]
    )
        
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt, tools=[available_functions]),
    )
    if not response.function_calls:
        return response.text

    for function_call_part in response.function_calls:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

def pretty_print(header, text):
    header = f"########## {header} ##########"
    print(header)
    print(text)
    print(f"{'#' * len(header)}")

if __name__ == "__main__":
    main()

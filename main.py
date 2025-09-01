import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from constants import *
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python import schema_run_python, run_python_file
from functions.call_function import call_function

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

    When utilizing file names or paths from previous messages, do not add the working directory root directory to the path.
    When asked to fix a bug, do not make new files. Look at the command and determine what the problem is. If it's an issue with a calculation, then the problem lies in ./calculator/pkg/calculator.py
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
    
    i = 0
    keep_running = True
    prompt_tokens = 0
    response_tokens = 0
    
    try:
        while keep_running:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=messages,
                config=types.GenerateContentConfig(system_instruction=system_prompt, tools=[available_functions]),
            )

            for cand in response.candidates:
                messages.append(cand.content)

            if not response.function_calls:
                keep_running = False
                pretty_print("Final Response", response.text)
                break

            for function_call_part in response.function_calls:
                #print(f"Calling function: {function_call_part.name}({function_call_part.args})")
                results = call_function(function_call_part, verbose)
                
                if len(results.parts) > 0 and results.parts[0].function_response.response != None:
                    print(f"-> {results.parts[0].function_response.response}")
                    response_parts = types.Content(role="user", parts=results.parts)
                    messages.append(response_parts)
                    #pretty_print("DEBUGGING", results)
                else:
                    raise Exception(f"Error: calling function {function_call_part.name} did not return a result")
            
            if verbose:
                prompt_tokens = response.usage_metadata.prompt_token_count
                response_tokens = response.usage_metadata.candidates_token_count
            
            i += 1
            if i > 20:
                keep_running = False
    except Exception as e:
        raise Exception(f"There was an error within the loop: {e}")
    
    if verbose:
        pretty_print_messages("Messages", messages)
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

def pretty_print(header, text):
    header = f"########## {header} ##########"
    print(header)
    print(text)
    print(f"{'#' * len(header)}")

def pretty_print_messages(header, messages):
    header = f"---------- {header} ----------"
    print(header)
    for item in messages:
        if isinstance(item, list):
            pretty_print_messages("Message sub-item", item)
        else:
            if len(item.parts) <= 0:
                pretty_print("Sub-message details", item)
            elif item.parts[0].text != None:
                pretty_print("Sub-message text", item.parts[0].text)
            elif item.parts[0].function_response != None and item.parts[0].function_response.response["result"] != None and item.parts[0].function_response.response["result"]["result"] != None:
                pretty_print("Sub-message response", item.parts[0].function_response.response["result"]["result"])
            else:
                pretty_print("Sub-message details", item)
    print(f"{'-' * len(header)}")

def test():
    print("RUNNING TESTS")
    #print(get_file_content("calculator", "calculator/main.py"))
    #print(run_python_file("calculator", "main.py", ["3 + 5"]))
    #print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    print(get_files_info("calculator", "calculator/pkg"))

if __name__ == "__main__":
    main()
    #test()

# import re
# import json
# from urllib3 import response
from gemini import client, tools, config
from executor import command_response
# from google.protobuf.json_format import MessageToDict

SYSTEM_PROMPT = """
You are a terminal assistant. Given a user request in natural language, output a JSON object with the following structure:

{
  "command": "<shell_command>",
  "explanation": "<brief explanation>"
}

Your job is to translate natural language into appropriate shell commands. Ensure your response is ONLY the JSON object, with no extra text or formatting.

Additional Instructions:
- If the user requests a command that is not installed (e.g., `htop`, `neofetch`), suggest the appropriate install command (e.g., `sudo apt-get install htop`) instead of the missing command.
- Use common defaults: assume Debian-based Linux (like Ubuntu) and use `apt-get` for installation unless specified otherwise.
- Only suggest direct shell commands, not Python or other scripts.
"""

def commands(user_input: str) -> command_response:
    response = client.models.generate_content(
        contents= f"Convert this into a shell command: {user_input}",
        model='gemini-2.5-flash',
        config=config,
    )
    
    if response.candidates and hasattr(response.candidates[0], "content") and response.candidates[0].content and hasattr(response.candidates[0].content, "parts") and response.candidates[0].content.parts:
        for part in response.candidates[0].content.parts:
            # if part.function_call.args:  -> Convert _StructValue or ListValue (existance of protobuf value)
            if hasattr(part, "function_call") and part.function_call is not None and hasattr(part.function_call, "args") and part.function_call.args:
                # args = part.function_call.args
                args = part.function_call.args
                return command_response(**args) # type: ignore (cursor false negative)

    raise ValueError(f"Failed to get tool call response: {response}")

# def commands(user_input: str) -> command_response:
#     prompt = f"{SYSTEM_PROMPT}\n\nUser request: {user_input}"

#     response = model.generate_content(prompt)

#     if response.text:
#         try:
#             response_data = json.loads(response.text.strip())
#             return command_response(**response_data)
#         except json.JSONDecodeError:
#             json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
#             if json_match:
#                 try:
#                     response_data = json.loads(json_match.group())
#                     return command_response(**response_data)
#                 except json.JSONDecodeError:
#                     pass

#     raise ValueError(f"Failed to get tool call response: {response}")
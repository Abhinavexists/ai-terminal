# import re
# import json
# from urllib3 import response
from gemini import model
from executor import command_response
# from google.protobuf.json_format import MessageToDict

SYSTEM_PROMPT = """
You are a terminal assistant. Given a user request in natural language, output a JSON object with the following structure:

{
  "command": "<shell_command>",
  "explanation": "<brief explanation>"
}

Ensure your response is ONLY the JSON object, no extra text or formatting.
"""

def commands(user_input: str) -> command_response:
    response = model.generate_content(
        f"Convert this into a shell command: {user_input}",
    )
    
    if response.candidates:
        for part in response.candidates[0].content.parts:
            # if part.function_call.args:  -> Convert _StructValue or ListValue (existance of protobuf value)
            if hasattr(part, "function_call") and part.function_call.args:
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
import re
import json
from gemini import client, config
from executor import CommandResponse
from os_info import operating_system

def get_system_prompt():
    os = operating_system.get_os()
    return f"""You are a terminal assistant. Given a user request in natural language, output a JSON object with the following structure:

    {{
    "command": "<shell_command>",
    "explanation": "<brief explanation>"
    }}

    Your job is to translate natural language into appropriate shell commands. Ensure your response is ONLY the JSON object, with no extra text or formatting.

    Current System Context:
    {operating_system.get_context()}

    Additional Instructions:
    - Use the appropriate package manager for this system: {operating_system.get_os()['package_manager']}
    - For package installation, use: {operating_system.get_os()['install']} <package_name>
    - For package updates, use: {operating_system.get_os()['update']}
    - For package upgrades, use: {operating_system.get_os()['upgrade']}
    - For package removal, use: {operating_system.get_os()['remove']} <package_name>
    - Only suggest direct shell commands, not Python or other scripts.
    - If a command is not available on this system, suggest alternatives or installation methods.
    - When moving files, consider the current working directory and use relative paths appropriately
    - Use "." to refer to the current directory and ".." for parent directory
    - Always verify that source files exist and target directories are valid before suggesting commands
    """

def parse_json(text: str) -> dict | None:
    """Try to parse JSON from text, handling code fences and other wrappers."""
    if not text:
        return None
    json_match = re.search(r'\{.*\}', text, flags=re.DOTALL)
    if not json_match:
        return None
    try:
        return json.loads(json_match.group())
    except json.JSONDecodeError:
        return None

def commands(user_input: str, current_dir: str = None) -> CommandResponse:
    prompt = get_system_prompt()
    if current_dir:
        prompt += f"\n\nCurrent Working Directory: {current_dir}"
    
    response = client.models.generate_content(
        contents= f"{prompt}\n\nUser request: {user_input}",
        model='gemini-2.5-flash',
        config=config,
    )
    
    if response.candidates and hasattr(response.candidates[0], "content") and response.candidates[0].content and hasattr(response.candidates[0].content, "parts") and response.candidates[0].content.parts:
        for part in response.candidates[0].content.parts:
            # if part.function_call.args:  -> Convert _StructValue or ListValue (existance of protobuf value)
            if hasattr(part, "function_call") and part.function_call is not None and hasattr(part.function_call, "args") and part.function_call.args:
                # args = part.function_call.args
                args = part.function_call.args
                return CommandResponse(**args) # type: ignore
            
            if hasattr(part, "text") and part.text: # parsing JSON from text
                data = parse_json(part.text)
                if data and "command" in data and "explanation" in data:
                    return CommandResponse(**data)

    raise ValueError(f"Failed to get tool call response: {response}")

from terminal.utils.gemini import client, generate_config
from terminal.utils.config import config
from terminal.core.executor import CommandResponse
from terminal.utils.os_info import operating_system
from terminal.utils.parsers import parse_json

def prompt_shell():
    os = operating_system.get_os()
    return f"""You are a specialized terminal command assistant. Your job is to translate natural language requests into appropriate shell commands.

Output a JSON object with the following structure:

{{
    "command": "<shell_command>",
    "explanation": "<brief explanation>",
    "response_type": "shell_command"
}}

Current System Context:
{operating_system.get_context()}

Instructions:
- Use the appropriate package manager: {operating_system.get_os()['package_manager']}
- For package installation: {operating_system.get_os()['install']} <package_name>
- For package updates: {operating_system.get_os()['update']}
- For package upgrades: {operating_system.get_os()['upgrade']}
- For package removal: {operating_system.get_os()['remove']} <package_name>
- Only suggest direct shell commands, not Python or other scripts
- Consider the current working directory and use relative paths appropriately
- Always verify file/directory existence before suggesting commands

Ensure your response is ONLY the JSON object, with no extra text or formatting."""



def process_shell_request(user_input: str, current_dir: str = None, context: str = "") -> CommandResponse:
    prompt = prompt_shell()
    if current_dir:
        prompt += f"\n\nCurrent Working Directory: {current_dir}"
    if context:
        prompt += f"\n\nAdditional Context: {context}"
    
    model_config = config.get_model_config()
    response = client.models.generate_content(
        contents=f"{prompt}\n\nUser request: {user_input}",
        model=model_config["model"],
        config=generate_config,
    )
    
    if response.candidates and hasattr(response.candidates[0], "content") and response.candidates[0].content and hasattr(response.candidates[0].content, "parts") and response.candidates[0].content.parts:
        for part in response.candidates[0].content.parts:
            if hasattr(part, "function_call") and part.function_call is not None and hasattr(part.function_call, "args") and part.function_call.args:
                args = part.function_call.args
                return CommandResponse(**args)
            
            if hasattr(part, "text") and part.text:
                data = parse_json(part.text)
                if data and "command" in data and "explanation" in data:
                    return CommandResponse(**data)

    raise ValueError(f"Failed to get shell command response: {response}")

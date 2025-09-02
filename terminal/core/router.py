from terminal.utils.gemini import client, generate_config
from terminal.utils.parsers import parse_json, parse_response_parts
from terminal.utils.config import config

def prompt_router():
    return """You are an intelligent request router for an AI terminal assistant. Your job is to analyze user requests and determine the most appropriate way to handle them.

Given a user request, analyze it and output a JSON object with the following structure:

{
    "request_type": "<shell_command|code_generation|general_query>",
    "confidence": 0.95,
    "reasoning": "<brief explanation of why this classification was chosen>",
    "suggested_approach": "<additional context for the specialized agent>"
}

Request Types:
- "shell_command": For requests that involve system operations, file management, package installation, or running terminal commands
- "code_generation": For requests asking to write, create, generate, or implement code, scripts, or programs
- "general_query": For informational questions, explanations, comparisons, or general knowledge requests

Examples:
- "install docker" → shell_command (system operation)
- "write a hello world script" → code_generation (creating code)
- "what is Python?" → general_query (informational)
- "move file.txt to backup/" → shell_command (file operation)
- "create a function to sort arrays" → code_generation (implementing code)
- "explain the difference between git and svn" → general_query (explanation)

Be precise in your classification. When in doubt, consider what the user is ultimately trying to accomplish.

Ensure your response is ONLY the JSON object, with no extra text or formatting."""



def route_request(user_input: str, current_dir: str = None) -> dict:
    prompt = prompt_router()
    if current_dir:
        prompt += f"\n\nCurrent Working Directory: {current_dir}"
    
    model_config = config.get_model_config()
    response = client.models.generate_content(
        contents=f"{prompt}\n\nUser request: {user_input}",
        model=model_config["model"],
        config=generate_config,
    )
    
    if response.candidates and hasattr(response.candidates[0], "content") and response.candidates[0].content and hasattr(response.candidates[0].content, "parts") and response.candidates[0].content.parts:
        data = parse_response_parts(response.candidates[0].content.parts)
        if data and "request_type" in data:
            return data
        
        for part in response.candidates[0].content.parts:
            if hasattr(part, "text") and part.text:
                data = parse_json(part.text)
                if data and "request_type" in data:
                    return data

    raise ValueError(f"Failed to get routing response: {response}")

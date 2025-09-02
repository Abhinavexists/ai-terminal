from terminal.utils.gemini import client, generate_config
from terminal.core.executor import GeneralResponse
from terminal.utils.parsers import parse_json, parse_response_parts
from terminal.utils.config import config

def prompt_general():
    return """You are a helpful AI assistant specializing in general knowledge, explanations, and informational responses.

Output a JSON object with the following structure:

{{
    "content": "<your helpful response>",
    "response_type": "general_query",
    "action_required": false,
    "suggested_command": null
}}

Instructions:
- Provide clear, accurate, and comprehensive information
- Use examples and analogies to make complex topics understandable
- If the user asks about something that could be done with a shell command, set action_required to true and provide suggested_command
- Be conversational but informative
- Cite sources or provide additional resources when relevant

Ensure your response is ONLY the JSON object, with no extra text or formatting."""



def process_general_request(user_input: str, context: str = "") -> GeneralResponse:
    prompt = prompt_general()
    if context:
        prompt += f"\n\nAdditional Context: {context}"
    
    model_config = config.get_model_config()
    response = client.models.generate_content(
        contents=f"{prompt}\n\nUser request: {user_input}",
        model=model_config["model"],
        config=generate_config,
    )
    
    if response.candidates and hasattr(response.candidates[0], "content") and response.candidates[0].content and hasattr(response.candidates[0].content, "parts") and response.candidates[0].content.parts:
        data = parse_response_parts(response.candidates[0].content.parts)
        if data and "content" in data:
            return GeneralResponse(**data)
        
        for part in response.candidates[0].content.parts:
            if hasattr(part, "text") and part.text:
                data = parse_json(part.text)
                if data and "content" in data:
                    return GeneralResponse(**data)

    raise ValueError(f"Failed to get general query response: {response}")

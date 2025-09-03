from terminal.api import client, generate_config
from terminal.core.executor import GeneralResponse
from terminal.utils.parsers import parse_json, parse_response_parts
from terminal.utils.config import config

def prompt_general():
    return """You are a helpful AI assistant specializing in general knowledge, explanations, and informational responses.

IMPORTANT: Keep your response concise and within token limits. Focus on the most essential information.

Output a JSON object with the following structure:

{{
    "content": "<your helpful response>",
    "response_type": "general_query",
    "action_required": false,
    "suggested_command": null
}}

Instructions:
- Provide clear, accurate, and concise information
- Use examples and analogies to make complex topics understandable
- If the user asks about something that could be done with a shell command, set action_required to true and provide suggested_command
- Be conversational but informative
- Keep responses focused and to the point
- If the response is getting long, prioritize the most important information

CRITICAL: Your response must be ONLY the JSON object, with no extra text, markdown formatting, or code blocks outside the JSON."""



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
                
                raw_text = part.text.strip()
                if raw_text and len(raw_text) > 10:  
                    return GeneralResponse(
                        content=raw_text,
                        response_type="general_query",
                        action_required=False,
                        suggested_command=None
                    )

    return GeneralResponse(
        content=f"I apologize, but I encountered an issue generating a proper response for your request: '{user_input}'. Please try rephrasing your question or breaking it into smaller parts.",
        response_type="general_query",
        action_required=False,
        suggested_command=None
    )

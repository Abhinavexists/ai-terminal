from terminal.api import client, generate_config
from terminal.core.executor import GeneralResponse, ResponseType
from terminal.utils.parsers import parse_json, parse_response_parts, handle_function_call
from terminal.utils.config import config

def prompt_code():
    return """You are a specialized coding assistant. Your job is to help users with code generation, programming questions, and technical implementations.

IMPORTANT: Keep your response concise and within token limits. Focus on the most essential code and explanations.

Output a JSON object with the following structure:

{{
    "content": "<your response with code examples and explanations>",
    "response_type": "code_generation",
    "action_required": false,
    "suggested_command": null
}}

Instructions:
- Provide clear, well-commented code examples
- Keep explanations brief but informative
- Include essential best practices only
- If the code can be executed as a script, set action_required to true and provide suggested_command
- Use appropriate programming languages based on the request
- Include basic error handling where relevant
- If the response is getting long, prioritize the core code over extensive explanations

CRITICAL: Your response must be ONLY the JSON object, with no extra text, markdown formatting, or code blocks outside the JSON."""


def process_code_request(user_input: str, context: str = "") -> GeneralResponse:
    prompt = prompt_code()
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
            func_response = handle_function_call(part, ResponseType.CODE_GENERATION)
            if func_response:
                return GeneralResponse(**func_response)
        
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
                    cleaned_text = raw_text
                    if cleaned_text.startswith('```'):
                        lines = cleaned_text.split('\n')
                        if lines[0].startswith('```'):
                            lines = lines[1:]
                        if lines and lines[-1].strip() == '```':
                            lines = lines[:-1]
                        cleaned_text = '\n'.join(lines)
                    
                    return GeneralResponse(
                        content=cleaned_text,
                        response_type=ResponseType.CODE_GENERATION,
                        action_required=False,
                        suggested_command=None
                    )

    return GeneralResponse(
        content=f"I apologize, but I encountered an issue generating a proper response for your request: '{user_input}'. The response may have been truncated due to length limits. Please try rephrasing your request or breaking it into smaller parts.",
        response_type=ResponseType.CODE_GENERATION,
        action_required=False,
        suggested_command=None
    )

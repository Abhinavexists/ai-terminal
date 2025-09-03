import re
import json

def parse_json(text: str) -> dict | None:
    if not text:
        return None
    
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*$', '', text)
    text = text.strip()
    
    json_match = re.search(r'\{.*\}', text, flags=re.DOTALL)
    if not json_match:
        return None

    json_text = json_match.group()
    
    try:
        return json.loads(json_text)
    except json.JSONDecodeError:
        try:
            # Handle truncated JSON by trying to close it properly
            if json_text.count('{') > json_text.count('}'):
                missing_braces = json_text.count('{') - json_text.count('}')
                json_text += '}' * missing_braces
            
            if json_text.count('"') % 2 != 0:
                last_quote = json_text.rfind('"')
                if last_quote > json_text.rfind(':'):
                    json_text = json_text[:last_quote + 1] + '"'
            
            return json.loads(json_text)
        except json.JSONDecodeError:
            try:
                content_match = re.search(r'"content"\s*:\s*"([^"]*(?:\\.[^"]*)*)"', json_text, re.DOTALL)
                if content_match:
                    return {
                        "content": content_match.group(1),
                        "response_type": "code_generation",
                        "action_required": False,
                        "suggested_command": None
                    }
            except:
                pass
            return None

def parse_response_parts(parts) -> dict | None:
    full_text = ""
    for part in parts:
        if hasattr(part, "text") and part.text:
            full_text += part.text
    return parse_json(full_text)

def handle_function_call(part, response_type, action_required=True):
    if hasattr(part, "function_call") and part.function_call is not None and hasattr(part.function_call, "args") and part.function_call.args:
        args = part.function_call.args
        content = f"**Command:** {args.get('command', '')}\n\n**Explanation:** {args.get('explanation', '')}"
        return {
            "content": content,
            "response_type": response_type,
            "action_required": action_required,
            "suggested_command": args.get('command', '')
        }
    return None

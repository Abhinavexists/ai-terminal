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

    try:
        return json.loads(json_match.group())
    except json.JSONDecodeError:
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

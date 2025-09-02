from terminal.core.executor import CommandResponse
from terminal.core.router import route_request
from terminal.agents.shell_agent import process_shell_request
from terminal.agents.code_agent import process_code_request
from terminal.agents.general_agent import process_general_request


def process_request(user_input: str, current_dir: str = None):
    routing_info = route_request(user_input, current_dir)
    request_type = routing_info.get("request_type", "shell_command")
    context = routing_info.get("suggested_approach", "")
    
    if request_type == "shell_command":
        return process_shell_request(user_input, current_dir, context)
    elif request_type == "code_generation":
        return process_code_request(user_input, context)
    else:
        return process_general_request(user_input, context)

def commands(user_input: str, current_dir: str = None) -> CommandResponse:
    """Backward compatibility function for shell commands only."""
    return process_shell_request(user_input, current_dir)

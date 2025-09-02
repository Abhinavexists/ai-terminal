from dotenv import load_dotenv
from google import genai
from google.genai import types
from terminal.utils.config import config

load_dotenv()

api_key = config.get_api_key()
client = genai.Client(api_key=api_key)

generate_command_function = {
                "name": "generate_command",
                "description": "Generate a shell command and explain what it does",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "command": {
                            "type": "string",
                            "description": "The shell command to execute"
                        },
                        "explanation": {
                            "type": "string",
                            "description": "Explanation of what the command does"
                        },
                    },
                    "required": ["command", "explanation"]
                }
            }

tools = types.Tool(function_declarations=[generate_command_function])

model_config = config.get_model_config()
generate_config = types.GenerateContentConfig(
    tools=[tools],
    temperature=model_config["temperature"],
    max_output_tokens=model_config["max_tokens"]
)

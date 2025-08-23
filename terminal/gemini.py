import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

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
config = types.GenerateContentConfig(tools=[tools])

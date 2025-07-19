import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key = os.getenv("GEMINI_API_KEY"))  # type: ignore

model = genai.GenerativeModel("gemini-2.5-flash",   # type: ignore
        tools=[
        {
            "function_declarations": [
                {
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
            ]
        }
    ]
) 
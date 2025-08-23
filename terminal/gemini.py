import os
import json
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

def get_api_key():
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        return api_key
    
    config_file = Path.home() / ".ai_terminal_config.json"
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                if config.get("gemini_api_key"):
                    return config["gemini_api_key"]
        except:
            pass
    
    print("\n🔑 Gemini API Key Required")
    print("To use AI features, you need a Gemini API key from Google AI Studio.")
    print("Get one at: https://aistudio.google.com/app/apikey")
    print()
    
    while True:
        api_key = input("Enter your Gemini API key: ").strip()
        if api_key and len(api_key) > 10:
            try:
                config = {"gemini_api_key": api_key}
                with open(config_file, 'w') as f:
                    json.dump(config, f)
                os.chmod(config_file, 0o600)
                print("✅ API key saved securely!")
                return api_key
            except Exception as e:
                print(f"❌ Failed to save config: {e}")
                return api_key
        else:
            print("❌ Invalid API key. Please try again.")

api_key = get_api_key()
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
config = types.GenerateContentConfig(tools=[tools])

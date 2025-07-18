import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key = os.getenv("GEMINI_API_KEY"))  # type: ignore
model = genai.GenerativeModel("gemini-2.5-flash") # type: ignore

def clean_output(output: str):
    if not output:
        return ""
    return (
        output.replace("```bash", "").replace("```", "").strip()
    )

def commands(prompt: str) -> str:
    instruction = ("You are a Linux shell assistant. Convert user input into a single valid shell command. "
                  "If the input is too vague or meaningless, respond with 'Please clarify your request.' "
                  "Only return the command. Do not include explanations, markdown or code blocks.")
    
    try:
      response  = model.generate_content([instruction, prompt])

      # DEBUG: Show raw output
      raw = response.text
      print(f"[dim]Raw response:[/dim] {repr(raw)}")

      cleaned = clean_output(raw)
      return cleaned if cleaned else "Please clarify your request."
    
    except Exception as e:     
      return f"Error: {e}"

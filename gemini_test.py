import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY")) # type: ignore

def test_gemini():
    try:
        model = genai.GenerativeModel("gemini-2.5-flash") # type: ignore
        response = model.generate_content("Hello, what is the current Linux command to list files?")
        print("API Call Successful")
        print("Response:")
        print(response.text)
    except Exception as e:
        print("API Call Failed")
        print(f"Error: {e}")

if __name__ == "__main__":
    test_gemini()

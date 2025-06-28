import os
import requests
from dotenv import load_dotenv

load_dotenv()


def openrouter_chat(prompt, model="deepseek/deepseek-chat:free"):
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    if OPENROUTER_API_KEY:
        OPENROUTER_API_KEY = OPENROUTER_API_KEY.strip()
    if not OPENROUTER_API_KEY:
        raise RuntimeError("OpenRouter API key missing")

    print(f"using api key {repr(OPENROUTER_API_KEY)} ")
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        print("Status code:", response.status_code)
        print("Raw response:", repr(response.text))
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print("Error communicating with OpenRouter:", e)
        print("Response content:", getattr(e.response, "text", None))
        raise
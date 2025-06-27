import os
from dotenv import load_dotenv
import requests

load_dotenv()
key = os.getenv("OPENROUTER_API_KEY")
print("Key loaded:", repr(key))
url = "https://openrouter.ai/api/v1/models"
headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
response = requests.get(url, headers=headers)
print(response.status_code)
print(response.text)
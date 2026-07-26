import os

from google.colab import userdata  # In case you are running it on Google Colab

try:  # B
    OPENAI_API_KEY = userdata.get("OPENAI_API_KEY")
except Exception:
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

USE_REAL_LLM = bool(OPENAI_API_KEY)
print(f"Using real LLM: {USE_REAL_LLM}")

from haystack.telemetry import tutorial_running

tutorial_running(24)

import os
from getpass import getpass

model_api_key = os.getenv("HF_API_KEY", None) or getpass("Enter HF API key:")
print(f"Using model API key: {model_api_key}")

import requests
from config import (
    BASE_URL,
    GENERATE_ENDPOINT,
    MODEL,
    TEMPERATURE,
    TOP_P,
)

URL = f"{BASE_URL}{GENERATE_ENDPOINT}"


class Agent:
    def __init__(self, model: str = MODEL):
        self.model = model

    def call(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "temperature": TEMPERATURE,
            "top_p": TOP_P,
            "stream": False,
        }

        response = requests.post(URL, json=payload, timeout=60)
        response.raise_for_status()

        return response.json()["response"].strip()

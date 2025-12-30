import requests
from librarian.llm.config import (
    BASE_URL,
    GENERATE_ENDPOINT,
    MODEL,
    TEMPERATURE,
    TOP_P,
)

URL = f"{BASE_URL}{GENERATE_ENDPOINT}"


class Agent:
    def __init__(self, model: str | None = MODEL, url: str = URL):
        self.model = model
        self.url = url

    def call(self, prompt: str) -> str:
    # if self.model:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "temperature": TEMPERATURE,
            "top_p": TOP_P,
            "stream": False,
        }
    # else:
    #     raise AttributeError("model not set")

    # if URL:
        response = requests.post(self.url, json=payload, timeout=60)
        response.raise_for_status()
    # else:
    #     raise AttributeError("URL not set")
        print(response)
        return response.json()["response"].strip()

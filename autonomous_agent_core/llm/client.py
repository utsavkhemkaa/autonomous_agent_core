# llm/client.py

from openai import OpenAI
from config.settings import OPENAI_MODEL, TEMPERATURE

class LLMClient:
    """
    Thin wrapper over OpenAI client.
    Exposes a stable interface for Planner.
    """

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def generate(self, prompt: str) -> str:
        """
        Generate a completion for the given prompt.
        This is the ONLY method Planner relies on.
        """
        response = self.client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are a precise planner."},
                {"role": "user", "content": prompt},
            ],
            temperature=TEMPERATURE,
        )

        return response.choices[0].message.content.strip()
from __future__ import annotations

import json
import os
from typing import TypeVar

from google import genai
from pydantic import BaseModel, ValidationError
from tenacity import retry, stop_after_attempt, wait_exponential

from app.config import get_settings

T = TypeVar("T", bound=BaseModel)


class GeminiAgent:
    model = "gemini-2.5-flash"

    def __init__(self) -> None:
        api_key = get_settings().gemini_api_key or os.getenv("GEMINI_API_KEY", "")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is required for Gemini agents")
        self.client = genai.Client(api_key=api_key)

    @retry(wait=wait_exponential(multiplier=1, min=1, max=8), stop=stop_after_attempt(3))
    def generate_json(self, prompt: str, output_model: type[T]) -> T:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config={"response_mime_type": "application/json"},
        )
        text = getattr(response, "text", "") or "{}"
        try:
            payload = json.loads(text)
            return output_model.model_validate(payload)
        except (json.JSONDecodeError, ValidationError) as exc:
            raise ValueError(f"Gemini returned invalid JSON: {text}") from exc


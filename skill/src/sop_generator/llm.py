from __future__ import annotations

import json
import os
import urllib.request
from dataclasses import dataclass
from typing import Optional


@dataclass
class LLMClient:
    api_base: str
    api_key: str
    model: str

    @classmethod
    def from_env(cls) -> Optional["LLMClient"]:
        api_base = os.getenv("OPENAI_API_BASE", "").rstrip("/")
        api_key = os.getenv("OPENAI_API_KEY", "")
        model = os.getenv("OPENAI_MODEL", "")
        if not api_base or not api_key or not model:
            return None
        return cls(api_base=api_base, api_key=api_key, model=model)

    def complete_json(self, system_prompt: str, user_prompt: str) -> dict:
        body = json.dumps(
            {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "temperature": 0.2,
                "response_format": {"type": "json_object"},
            }
        ).encode("utf-8")
        req = urllib.request.Request(
            f"{self.api_base}/chat/completions",
            data=body,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        content = payload["choices"][0]["message"]["content"]
        return json.loads(content)

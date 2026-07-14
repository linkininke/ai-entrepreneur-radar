import json

import httpx

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger("ai_agent")


class LLMServiceError(Exception):
    pass


class LLMService:
    def __init__(self) -> None:
        self.settings = get_settings()

    def analyze_information(self, title: str, url: str | None, content: str | None) -> dict:
        if not self.settings.llm_api_key:
            raise LLMServiceError("LLM_API_KEY is not configured")

        prompt = self._build_prompt(title=title, url=url, content=content)
        payload = {
            "model": self.settings.llm_model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are an entrepreneurship intelligence analyst. "
                        "Return strict JSON with keys: summary, key_topics, relevance_score, commercial_potential."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
            "response_format": {"type": "json_object"},
        }

        headers = {
            "Authorization": f"Bearer {self.settings.llm_api_key}",
            "Content-Type": "application/json",
        }

        with httpx.Client(timeout=60.0) as client:
            response = client.post(
                f"{self.settings.llm_base_url.rstrip('/')}/chat/completions",
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

        content_text = data["choices"][0]["message"]["content"]
        parsed = json.loads(content_text)
        logger.info("LLM analysis completed for title=%s", title[:80])
        return {
            "summary": parsed.get("summary", ""),
            "key_topics": parsed.get("key_topics", []),
            "relevance_score": float(parsed.get("relevance_score", 0)),
            "commercial_potential": parsed.get("commercial_potential", "unknown"),
            "raw_response": data,
        }

    def _build_prompt(self, title: str, url: str | None, content: str | None) -> str:
        return (
            "Analyze this item for entrepreneurship signals.\n\n"
            f"Title: {title}\n"
            f"URL: {url or 'N/A'}\n"
            f"Content: {content or 'N/A'}\n\n"
            "Return JSON:\n"
            "{\n"
            '  "summary": "2-3 sentence business insight",\n'
            '  "key_topics": ["topic1", "topic2"],\n'
            '  "relevance_score": 0-100,\n'
            '  "commercial_potential": "low|medium|high"\n'
            "}"
        )

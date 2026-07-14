import json
import time

import httpx

from app.core.config import get_settings
from app.core.logging import get_logger
from app.i18n.locale import locale_language_name, normalize_locale

logger = get_logger("ai_agent")


class LLMServiceError(Exception):
    pass


class LLMService:
    def __init__(self) -> None:
        self.settings = get_settings()

    def analyze_information(
        self,
        title: str,
        url: str | None,
        content: str | None,
        locale: str | None = None,
    ) -> dict:
        if not self.settings.llm_api_key:
            raise LLMServiceError("LLM_API_KEY is not configured")

        target_locale = normalize_locale(locale or self.settings.llm_default_locale)
        language = locale_language_name(target_locale)
        prompt = self._build_prompt(title=title, url=url, content=content, language=language)
        payload = {
            "model": self.settings.llm_model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are an entrepreneurship intelligence analyst. "
                        f"Write all natural-language fields in {language}. "
                        "Return strict JSON with keys: summary, key_topics, relevance_score, commercial_potential. "
                        "commercial_potential must remain one of: low, medium, high, unknown."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
            "response_format": {"type": "json_object"},
        }

        data = self._chat_completion(payload)
        content_text = data["choices"][0]["message"]["content"]
        parsed = json.loads(content_text)
        logger.info("LLM analysis completed for title=%s locale=%s", title[:80], target_locale)
        return {
            "summary": parsed.get("summary", ""),
            "key_topics": parsed.get("key_topics", []),
            "relevance_score": float(parsed.get("relevance_score", 0)),
            "commercial_potential": parsed.get("commercial_potential", "unknown"),
            "raw_response": data,
            "locale": target_locale,
        }

    def generate_opportunity(
        self,
        information_title: str,
        analysis_summary: str,
        key_topics: list,
        commercial_potential: str,
        locale: str | None = None,
    ) -> dict:
        if not self.settings.llm_api_key:
            raise LLMServiceError("LLM_API_KEY is not configured")

        target_locale = normalize_locale(locale or self.settings.llm_default_locale)
        language = locale_language_name(target_locale)
        prompt = (
            f"Based on the signal below, generate one concrete startup opportunity for a solo founder. "
            f"Write all natural-language fields in {language}.\n\n"
            f"Signal title: {information_title}\n"
            f"Analysis summary: {analysis_summary}\n"
            f"Key topics: {', '.join(key_topics)}\n"
            f"Commercial potential: {commercial_potential}\n\n"
            "Return JSON:\n"
            "{\n"
            '  "title": "short opportunity name",\n'
            '  "description": "what the opportunity is",\n'
            '  "target_audience": "who would pay",\n'
            '  "problem_statement": "pain point being solved",\n'
            '  "suggested_action": "first step a founder can take this week",\n'
            '  "confidence_score": 0-100\n'
            "}"
        )

        payload = {
            "model": self.settings.llm_model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a startup opportunity generator for individual entrepreneurs. "
                        f"Write all natural-language fields in {language}. "
                        "Return strict JSON with keys: title, description, target_audience, "
                        "problem_statement, suggested_action, confidence_score."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.3,
            "response_format": {"type": "json_object"},
        }

        data = self._chat_completion(payload)
        content_text = data["choices"][0]["message"]["content"]
        parsed = json.loads(content_text)
        logger.info(
            "LLM opportunity generated for title=%s locale=%s",
            information_title[:80],
            target_locale,
        )
        return {
            "title": parsed.get("title", ""),
            "description": parsed.get("description", ""),
            "target_audience": parsed.get("target_audience", ""),
            "problem_statement": parsed.get("problem_statement", ""),
            "suggested_action": parsed.get("suggested_action", ""),
            "confidence_score": float(parsed.get("confidence_score", 0)),
            "raw_response": data,
            "locale": target_locale,
        }

    def translate_analysis_fields(
        self,
        summary: str,
        key_topics: list[str],
        source_locale: str,
        target_locale: str,
    ) -> dict:
        if not self.settings.llm_api_key:
            raise LLMServiceError("LLM_API_KEY is not configured")

        target = normalize_locale(target_locale)
        source = normalize_locale(source_locale)
        if target == source:
            return {"summary": summary, "key_topics": key_topics}

        language = locale_language_name(target)
        prompt = (
            f"Translate the entrepreneurship analysis fields from {locale_language_name(source)} "
            f"to {language}. Keep meaning precise and business-friendly.\n\n"
            f"summary: {summary}\n"
            f"key_topics: {json.dumps(key_topics, ensure_ascii=False)}\n\n"
            'Return JSON: {"summary": "...", "key_topics": ["...", "..."]}'
        )
        payload = {
            "model": self.settings.llm_model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a professional translator for startup intelligence content. "
                        f"Write output in {language}. Return strict JSON only."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.1,
            "response_format": {"type": "json_object"},
        }
        data = self._chat_completion(payload)
        parsed = json.loads(data["choices"][0]["message"]["content"])
        return {
            "summary": parsed.get("summary", summary),
            "key_topics": parsed.get("key_topics", key_topics),
        }

    def translate_opportunity_fields(
        self,
        fields: dict[str, str],
        source_locale: str,
        target_locale: str,
    ) -> dict:
        if not self.settings.llm_api_key:
            raise LLMServiceError("LLM_API_KEY is not configured")

        target = normalize_locale(target_locale)
        source = normalize_locale(source_locale)
        if target == source:
            return fields

        language = locale_language_name(target)
        prompt = (
            f"Translate the startup opportunity fields from {locale_language_name(source)} "
            f"to {language}. Keep meaning precise and actionable.\n\n"
            f"{json.dumps(fields, ensure_ascii=False)}\n\n"
            "Return JSON with keys: title, description, target_audience, problem_statement, suggested_action"
        )
        payload = {
            "model": self.settings.llm_model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a professional translator for startup opportunity briefs. "
                        f"Write output in {language}. Return strict JSON only."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.1,
            "response_format": {"type": "json_object"},
        }
        data = self._chat_completion(payload)
        parsed = json.loads(data["choices"][0]["message"]["content"])
        return {
            "title": parsed.get("title", fields.get("title", "")),
            "description": parsed.get("description", fields.get("description", "")),
            "target_audience": parsed.get("target_audience", fields.get("target_audience", "")),
            "problem_statement": parsed.get(
                "problem_statement",
                fields.get("problem_statement", ""),
            ),
            "suggested_action": parsed.get("suggested_action", fields.get("suggested_action", "")),
        }

    def _chat_completion(self, payload: dict) -> dict:
        headers = {
            "Authorization": f"Bearer {self.settings.llm_api_key}",
            "Content-Type": "application/json",
        }
        url = f"{self.settings.llm_base_url.rstrip('/')}/chat/completions"
        proxy = self.settings.llm_proxy_url()
        retries = max(1, self.settings.llm_request_retries)
        last_error: Exception | None = None

        for attempt in range(1, retries + 1):
            try:
                with httpx.Client(timeout=90.0, proxy=proxy) as client:
                    response = client.post(url, headers=headers, json=payload)
                    response.raise_for_status()
                    return response.json()
            except httpx.HTTPStatusError as exc:
                detail = exc.response.text[:300]
                raise LLMServiceError(
                    f"LLM API returned {exc.response.status_code}: {detail}"
                ) from exc
            except (httpx.ConnectError, httpx.ReadTimeout, httpx.WriteTimeout, httpx.PoolTimeout) as exc:
                last_error = exc
                logger.warning(
                    "LLM request failed attempt=%s/%s url=%s proxy=%s error=%s",
                    attempt,
                    retries,
                    url,
                    proxy or "direct",
                    exc,
                )
                if attempt < retries:
                    time.sleep(attempt * 2)
                    continue
            except httpx.HTTPError as exc:
                raise LLMServiceError(f"LLM request failed: {exc}") from exc

        hint = (
            " Check HTTP_PROXY/HTTPS_PROXY if running inside Docker "
            "(e.g. http://host.docker.internal:7890)."
        )
        raise LLMServiceError(f"LLM request failed after {retries} attempts: {last_error}.{hint}") from last_error

    def _build_prompt(
        self,
        title: str,
        url: str | None,
        content: str | None,
        language: str,
    ) -> str:
        return (
            f"Analyze this item for entrepreneurship signals. "
            f"Write summary and key_topics in {language}.\n\n"
            f"Title: {title}\n"
            f"URL: {url or 'N/A'}\n"
            f"Content: {content or 'N/A'}\n\n"
            "Return JSON:\n"
            "{\n"
            '  "summary": "2-3 sentence business insight",\n'
            '  "key_topics": ["topic1", "topic2"],\n'
            '  "relevance_score": 0-100,\n'
            '  "commercial_potential": "low|medium|high|unknown"\n'
            "}"
        )

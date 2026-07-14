from typing import Final

SUPPORTED_LOCALES: Final[frozenset[str]] = frozenset(
    {"zh-CN", "en", "ja", "ko", "es", "fr", "de", "pt-BR"}
)

DEFAULT_LOCALE: Final[str] = "zh-CN"

LOCALE_LABELS: Final[dict[str, str]] = {
    "zh-CN": "Simplified Chinese",
    "en": "English",
    "ja": "Japanese",
    "ko": "Korean",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "pt-BR": "Brazilian Portuguese",
}


def normalize_locale(locale: str | None) -> str:
    if not locale:
        return DEFAULT_LOCALE
    value = locale.strip()
    if value in SUPPORTED_LOCALES:
        return value
    if value.startswith("zh"):
        return "zh-CN"
    if value.startswith("pt"):
        return "pt-BR"
    prefix = value.split("-", 1)[0]
    if prefix in SUPPORTED_LOCALES:
        return prefix
    return DEFAULT_LOCALE


def locale_language_name(locale: str | None) -> str:
    normalized = normalize_locale(locale)
    return LOCALE_LABELS.get(normalized, "English")

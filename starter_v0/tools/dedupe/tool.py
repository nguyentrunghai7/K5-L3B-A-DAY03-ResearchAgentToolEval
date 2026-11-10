from __future__ import annotations

from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit

VALID_KEYS = ("url", "title")


def _normalize_url(url: str) -> str:
    """Same page written differently must give the same key: ignore scheme, www., fragment,
    trailing slash, host case and utm_* tracking params."""
    parts = urlsplit(url.strip())
    host = parts.netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    path = parts.path.rstrip("/")
    query = sorted((k, v) for k, v in parse_qsl(parts.query) if not k.lower().startswith("utm_"))
    return f"{host}{path}" + (f"?{urlencode(query)}" if query else "")


def _normalize_title(title: str) -> str:
    return " ".join(title.casefold().split())


def _error(exc: Exception) -> dict[str, Any]:
    return {"tool": "dedupe", "error": type(exc).__name__, "message": str(exc)}


def dedupe_items(items: list[dict[str, Any]] | None = None, key: str = "url") -> dict[str, Any]:
    """Remove duplicate items from an already-collected list. First occurrence wins, order is kept.

    Items with no value for `key` cannot be compared, so they are always kept.
    Bad input returns an error dict instead of raising.
    """
    try:
        if key not in VALID_KEYS:
            raise ValueError(f"key must be one of {list(VALID_KEYS)}, got {key!r}")
        if items is None:
            items = []
        if not isinstance(items, list):
            raise TypeError(f"items must be a list of objects, got {type(items).__name__}")

        normalize = _normalize_url if key == "url" else _normalize_title
        seen: set[str] = set()
        kept: list[dict[str, Any]] = []
        skipped_invalid = 0
        removed = 0
        for item in items:
            if not isinstance(item, dict):
                skipped_invalid += 1
                continue
            raw = item.get(key)
            value = normalize(raw) if isinstance(raw, str) and raw.strip() else ""
            if value and value in seen:
                removed += 1
                continue
            if value:
                seen.add(value)
            kept.append(item)
        return {
            "tool": "dedupe",
            "key": key,
            "items": kept,
            "item_count": len(kept),
            "removed_count": removed,
            "skipped_invalid": skipped_invalid,
        }
    except Exception as exc:  # tools return an error dict so the agent loop can keep going
        return _error(exc)

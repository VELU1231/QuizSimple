import logging
import os
from typing import Any
from urllib.parse import urljoin

import requests

logger = logging.getLogger(__name__)

SCORES_TABLE = "quiz_scores"


def _get_env() -> tuple[str, str]:
    url = os.getenv("SUPABASE_URL", "").strip()
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "").strip() or os.getenv(
        "SUPABASE_KEY", ""
    ).strip()
    return url, key


def _base_rest_url() -> str | None:
    url, _ = _get_env()
    if not url:
        return None
    return urljoin(url.rstrip("/") + "/", "rest/v1/")


def _headers() -> dict[str, str] | None:
    _, key = _get_env()
    if not key:
        return None
    return {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }


def supabase_enabled() -> bool:
    url, key = _get_env()
    return bool(url and key)


def save_score_row(payload: dict[str, Any]) -> bool:
    base = _base_rest_url()
    headers = _headers()
    if base is None or headers is None:
        return False

    try:
        headers = {**headers, "Prefer": "return=minimal"}
        endpoint = urljoin(base, SCORES_TABLE)
        res = requests.post(endpoint, json=payload, headers=headers, timeout=8)
        if 200 <= res.status_code < 300:
            return True
        logger.warning("Supabase insert failed (%s): %s", res.status_code, res.text)
        return False
    except Exception as exc:  # pragma: no cover - network/database runtime guard
        logger.warning("Supabase insert failed, falling back to memory: %s", exc)
        return False


def fetch_top_scores(quiz_id: str | None = None, limit: int = 10) -> list[dict[str, Any]]:
    base = _base_rest_url()
    headers = _headers()
    if base is None or headers is None:
        return []

    params = {
        "select": "quiz_id,name,score,max_score,created_at",
        "order": "score.desc,created_at.asc",
        "limit": str(limit),
    }
    if quiz_id:
        params["quiz_id"] = f"eq.{quiz_id}"

    try:
        endpoint = urljoin(base, SCORES_TABLE)
        res = requests.get(endpoint, params=params, headers=headers, timeout=8)
        if 200 <= res.status_code < 300:
            data = res.json()
            return data if isinstance(data, list) else []
        logger.warning("Supabase select failed (%s): %s", res.status_code, res.text)
        return []
    except Exception as exc:  # pragma: no cover - network/database runtime guard
        logger.warning("Supabase select failed, using fallback leaderboard: %s", exc)
        return []

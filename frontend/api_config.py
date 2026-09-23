import os

import requests

API_BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")

# Render's free tier sleeps idle services after ~15 min. Waking one takes 30+s,
# so requests must be patient and must tolerate non-JSON (HTML) responses.
REQUEST_TIMEOUT = int(os.environ.get("API_REQUEST_TIMEOUT", "90"))
WAKE_ATTEMPTS = int(os.environ.get("API_WAKE_ATTEMPTS", "3"))


def ensure_backend() -> bool:
    """Ping /health until it responds, waking a sleeping backend."""
    for _ in range(WAKE_ATTEMPTS):
        try:
            response = requests.get(f"{API_BASE_URL}/health", timeout=REQUEST_TIMEOUT)
            if response.status_code == 200:
                return True
        except requests.RequestException:
            continue
    return False


def api_request(method: str, path: str, headers: dict | None = None, json_body=None):
    """Call the API with cold-start handling. Returns a response, or None."""
    ensure_backend()
    try:
        return requests.request(
            method,
            f"{API_BASE_URL}{path}",
            headers=headers,
            json=json_body,
            timeout=REQUEST_TIMEOUT,
        )
    except requests.RequestException:
        return None


def error_detail(response, fallback: str = "Request failed") -> str:
    """Extract a readable message from a response, even if the body is HTML."""
    try:
        data = response.json()
    except ValueError:
        text = (response.text or "").strip()
        return text[:200] if text else f"{fallback} (HTTP {response.status_code})"
    if isinstance(data, dict) and "detail" in data:
        return str(data["detail"])
    return str(data)

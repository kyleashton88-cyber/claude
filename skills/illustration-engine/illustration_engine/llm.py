"""Optional helper that returns a JSON spec and nothing else.

The helper never receives a request to draw, and its reply is rejected unless
it is a spec this package already knows how to draw locally.
"""

from __future__ import annotations

import json
import os
import re
import urllib.request

from .parser import ParseError, spec_from_dict
from .spec import TYPES, Spec

SYSTEM = (
    "You convert one lesson sentence into a single JSON object for a local diagram program. "
    "Return one JSON object and nothing else. Do not return pixels, SVG, markdown, "
    "image URLs, or base64. Do not describe a picture for an image model. "
    "The object must use one allowed type and a params object. "
    "Labels are 2 to 5 short items, each at most three words. "
    "Do not include company names, email addresses, phone numbers, currency symbols, or profit claims. "
    "When the sentence needs a figure, put a plain number in params. "
    f"Allowed types: {', '.join(TYPES)}."
)


class LlmUnavailable(RuntimeError):
    pass


def endpoint(base_url: str | None = None) -> str:
    base = (base_url or os.environ.get("ILLUSTRATION_LLM_BASE_URL") or "https://api.openai.com/v1").rstrip("/")
    url = base + "/chat/completions"
    if "/images" in url:
        raise LlmUnavailable("the helper URL must be a chat endpoint, not an image endpoint")
    return url


def build_request(prompt: str, model: str | None = None) -> dict:
    return {
        "model": model or os.environ.get("ILLUSTRATION_LLM_MODEL") or "gpt-4o-mini",
        "temperature": 0,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": prompt},
        ],
    }


def _default_transport(url: str, payload: dict, headers: dict) -> dict:
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers=headers,
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as response:
        return json.loads(response.read().decode())


def spec_from_llm(prompt: str, transport=None, base_url: str | None = None) -> Spec:
    """Ask for a JSON spec. The caller renders it with the local engine."""
    key = os.environ.get("ILLUSTRATION_LLM_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if transport is None and not key:
        raise LlmUnavailable(
            "No ILLUSTRATION_LLM_API_KEY or OPENAI_API_KEY is set. "
            "The rule-based parser does not need a key."
        )
    url = endpoint(base_url)
    payload = build_request(prompt)
    headers = {"Content-Type": "application/json"}
    if key:
        headers["Authorization"] = f"Bearer {key}"
    send = transport or _default_transport
    body = send(url, payload, headers)
    try:
        content = body["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise ParseError("the helper did not return a chat message") from exc
    if not isinstance(content, str):
        raise ParseError("the helper reply was not text")
    if re.search(r"data:image|<svg|https?://", content, re.I):
        raise ParseError("the helper returned drawing data; only a JSON spec is accepted")
    try:
        data = json.loads(content)
    except json.JSONDecodeError as exc:
        raise ParseError("the helper did not return JSON") from exc
    return spec_from_dict(data)

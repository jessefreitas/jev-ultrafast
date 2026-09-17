"""Authenticated client for the OmniForge Workers AI decision gateway."""

import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


def request_decision(payload):
    """Send a minimal, pre-sanitized decision contract to the internal gateway."""
    endpoint = os.environ.get("JEV_WORKERS_AI_GATEWAY_URL", "")
    token = os.environ.get("JEV_WORKERS_AI_GATEWAY_TOKEN", "")
    parsed = urlparse(endpoint)
    if parsed.scheme != "https" or not parsed.netloc or not token:
        raise RuntimeError(
            "Workers AI gateway is not configured. Set the internal HTTPS gateway URL and token."
        )
    request = Request(
        endpoint,
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "omni-jev/0.1",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=20) as response:
            return json.loads(response.read())
    except (HTTPError, URLError, OSError, ValueError) as exc:
        raise RuntimeError("Internal Workers AI gateway did not return a valid decision.") from exc

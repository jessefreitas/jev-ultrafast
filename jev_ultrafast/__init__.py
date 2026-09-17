"""Jev chooses an observed action. Code owns execution. Sanitized for OmniForge."""

import os

# Desativação forçada de qualquer telemetria de browser-harness / PostHog
os.environ["BH_TELEMETRY"] = "0"
os.environ["BROWSER_HARNESS_TELEMETRY"] = "0"
os.environ["ANONYMIZED_TELEMETRY"] = "0"

from .agent import Agent
from .browser import Browser

__all__ = ["Agent", "Browser"]


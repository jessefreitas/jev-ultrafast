"""Jev chooses an observed action. Code owns execution."""

import os

# Browser Harness reads these settings when it starts.  Keep telemetry disabled
# even when a host has no per-user Browser Harness configuration.
os.environ["BH_TELEMETRY"] = "0"
os.environ["BROWSER_HARNESS_TELEMETRY"] = "0"
os.environ["ANONYMIZED_TELEMETRY"] = "0"

from .agent import Agent
from .browser import Browser

__all__ = ["Agent", "Browser"]

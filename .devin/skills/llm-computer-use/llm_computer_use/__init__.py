"""LLM Computer Use v2 - Minimal package."""
from .core import ScreenCapture, AgentSession, execute_action
from .cli import main

__version__ = "0.5.0"
__all__ = ["ScreenCapture", "AgentSession", "execute_action", "main"]

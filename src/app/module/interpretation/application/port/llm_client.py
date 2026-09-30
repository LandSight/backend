"""LLM client port."""

from __future__ import annotations

from abc import ABC, abstractmethod


class LLMClient(ABC):
    """Text completion client for an OpenAI-compatible LLM server.

    Implementations raise :class:`app.module.interpretation.application.error.LLMClientError`
    when the server cannot produce an answer.
    """

    @abstractmethod
    async def complete(self, system_prompt: str, user_prompt: str) -> str:
        """Return the model answer for the given prompts."""
        raise NotImplementedError


__all__ = ("LLMClient",)

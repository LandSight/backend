"""LLM client port and OpenAI-compatible implementation."""

from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, override

import httpx

from app.module.interpretation.application.error import InterpretationGenerationError
from app.module.interpretation.domain.value_object import Completion
from app.platform.logging import get_logger


if TYPE_CHECKING:
    from collections.abc import Mapping

    from app.module.interpretation.domain.value_object import Prompt
    from app.platform.config.models import LLMConfig


class LLMClient(ABC):
    """Text completion client for an OpenAI-compatible LLM server."""

    @abstractmethod
    async def complete(self, prompt: Prompt) -> Completion:
        """Return the model answer for the given prompt."""
        raise NotImplementedError


class OpenAICompatibleLLMClient(LLMClient):
    """Calls a llama.cpp server through its OpenAI-compatible chat API.

    Requests retry a couple of times on transport or server errors; after the
    last failure an :class:`InterpretationGenerationError` is raised so the
    interpreter can fall back to a safe text.
    """

    _MAX_ATTEMPTS = 3
    _BACKOFF_SECONDS = 0.5

    def __init__(
        self,
        config: LLMConfig,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self._config = config
        self._transport = transport
        self._logger = get_logger("app.interpretation.llm")

    @override
    async def complete(self, prompt: Prompt) -> Completion:
        """See :class:`LLMClient.complete`."""
        url = f"{self._config.base_url.rstrip('/')}/chat/completions"
        payload = {
            "model": self._config.model,
            "messages": [{"role": "user", "content": prompt.unwrap()}],
            "temperature": self._config.temperature,
            "max_tokens": self._config.max_tokens,
        }

        last_error: Exception | None = None
        for attempt in range(1, self._MAX_ATTEMPTS + 1):
            try:
                text = await self._request(url, payload)
                return Completion(text)
            except (httpx.HTTPError, KeyError, IndexError, ValueError) as error:
                last_error = error
                self._logger.warning("LLM request failed (attempt %s/%s): %s", attempt, self._MAX_ATTEMPTS, error)
                if attempt < self._MAX_ATTEMPTS:
                    await asyncio.sleep(self._BACKOFF_SECONDS * attempt)

        reason = f"LLM request failed after {self._MAX_ATTEMPTS} attempts: {last_error}"
        raise InterpretationGenerationError(reason)

    async def _request(self, url: str, payload: Mapping[str, object]) -> str:
        """Perform one HTTP request and extract the answer text."""
        async with httpx.AsyncClient(timeout=self._config.timeout_seconds, transport=self._transport) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
        return str(data["choices"][0]["message"]["content"])


__all__ = ("LLMClient", "OpenAICompatibleLLMClient")

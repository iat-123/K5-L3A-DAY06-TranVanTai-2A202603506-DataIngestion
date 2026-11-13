"""Real embedding provider adapters. No mock / random fallback: errors propagate."""
import os
from typing import Protocol

from dotenv import load_dotenv


class Embedder(Protocol):
    model_name: str
    dimensions: int

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Return one vector per input text, in the same order."""
        ...

    def embed_query(self, question: str) -> list[float]:
        """Return a query vector compatible with the stored document vectors."""
        ...


class OpenAICompatibleEmbedder:
    """OpenAI embeddings API (also works for OpenRouter via its OpenAI-compatible base URL).

    text-embedding-3-* models are symmetric: queries and documents are embedded the
    same way, with no instruction prefix.
    """

    BATCH_SIZE = 128

    def __init__(self, model_name: str, api_key: str, base_url: str | None = None) -> None:
        from openai import OpenAI

        if not api_key:
            raise RuntimeError("Embedding API key is empty; fill it in starter/.env.")
        self.model_name = model_name
        self.provider = "openrouter" if base_url else "openai"
        self._client = OpenAI(api_key=api_key, base_url=base_url, max_retries=3, timeout=60)
        self.total_tokens = 0
        # Probe once so dimensions come from the real model, not an assumption.
        self.dimensions = len(self._embed(["dimension probe"])[0])

    def _embed(self, texts: list[str]) -> list[list[float]]:
        vectors: list[list[float]] = []
        for start in range(0, len(texts), self.BATCH_SIZE):
            batch = texts[start:start + self.BATCH_SIZE]
            response = self._client.embeddings.create(model=self.model_name, input=batch)
            if response.usage:
                self.total_tokens += response.usage.total_tokens
            ordered = sorted(response.data, key=lambda item: item.index)
            if len(ordered) != len(batch):
                raise RuntimeError(f"Provider returned {len(ordered)} vectors for {len(batch)} inputs")
            vectors.extend(item.embedding for item in ordered)
        return vectors

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self._embed(texts)

    def embed_query(self, question: str) -> list[float]:
        return self._embed([question])[0]


def build_embedder() -> OpenAICompatibleEmbedder:
    """Create the embedder configured in starter/.env."""
    load_dotenv()
    provider = (os.getenv("EMBEDDING_PROVIDER") or "").strip().lower()
    model = (os.getenv("EMBEDDING_MODEL") or "").strip()
    if not model:
        raise RuntimeError("EMBEDDING_MODEL is empty in starter/.env.")
    if provider == "openai":
        return OpenAICompatibleEmbedder(model, os.getenv("OPENAI_API_KEY", ""))
    if provider == "openrouter":
        return OpenAICompatibleEmbedder(model, os.getenv("OPENROUTER_API_KEY", ""),
                                        base_url="https://openrouter.ai/api/v1")
    raise RuntimeError(f"Unsupported EMBEDDING_PROVIDER={provider!r}; use openai or openrouter.")

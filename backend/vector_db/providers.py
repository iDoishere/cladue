from typing import Protocol, List
import os


class EmbeddingProvider(Protocol):
    def embed(self, text: str) -> List[float]: ...


class GeminiEmbeddingProvider:
    def __init__(self, api_key: str):
        from google import genai
        self._client = genai.Client(api_key=api_key)

    def embed(self, text: str) -> List[float]:
        try:
            result = self._client.models.embed_content(
                model="text-embedding-004",
                contents=text
            )
            return result.embeddings[0].values
        except Exception as e:
            print(f"Embedding error: {e}")
            return [0.0] * 768


class NullEmbeddingProvider:
    """Used when no API key is configured — returns zero vectors."""
    def embed(self, text: str) -> List[float]:
        return [0.0] * 768


def get_default_provider() -> EmbeddingProvider:
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        return GeminiEmbeddingProvider(api_key)
    print("⚠️  Warning: GOOGLE_API_KEY not set - semantic search disabled")
    return NullEmbeddingProvider()

"""All configuration lives here. Never read os.environ anywhere else."""
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# repo-root/.env (works whether you start the API from backend/ or the repo root)
ROOT_ENV = Path(__file__).resolve().parents[3] / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=(str(ROOT_ENV), ".env"), extra="ignore")

    app_name: str = "Forge Starter"
    domain: str = "example"  # which module in app/domain/ to load
    cors_origins: str = "http://localhost:5173"

    # --- LLM providers (any OpenAI-compatible endpoint) -----------------
    # Primary: Groq (fast + free tier). Fallback: any second provider.
    llm_base_url: str = "https://api.groq.com/openai/v1"
    llm_api_key: str = ""
    llm_model: str = "llama-3.3-70b-versatile"
    llm_fast_model: str = "llama-3.1-8b-instant"  # router / cheap calls
    llm_vision_model: str = "meta-llama/llama-4-scout-17b-16e-instruct"
    stt_model: str = "whisper-large-v3-turbo"

    fallback_base_url: str = ""  # e.g. https://openrouter.ai/api/v1
    fallback_api_key: str = ""
    fallback_model: str = ""

    llm_timeout_s: float = 25.0
    llm_temperature: float = 0.3

    # --- Memory ----------------------------------------------------------
    qdrant_url: str = ""  # empty => in-process memory (zero setup)
    qdrant_api_key: str = ""
    embeddings: str = "hash"  # "hash" (offline, no download) | "fastembed"
    embed_dim: int = 256  # only for "hash"
    rag_top_k: int = 4
    rag_min_score: float = 0.05

    # --- Agents ----------------------------------------------------------
    max_self_corrections: int = 1
    history_turns: int = 6


@lru_cache
def get_settings() -> Settings:
    return Settings()

"""Application configuration loaded from environment / .env file."""
from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

# backend/app/core/config.py -> parents[0]=core, [1]=app, [2]=backend
BACKEND_DIR = Path(__file__).resolve().parents[2]
ROOT_DIR = BACKEND_DIR.parent

load_dotenv(BACKEND_DIR / ".env")


def _as_bool(value: str | None, default: bool = False) -> bool:
    if value is None or value == "":
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _resolve_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return (BACKEND_DIR / path).resolve()


class Settings:
    """Central application settings."""

    def __init__(self) -> None:
        self.APP_NAME = os.getenv("APP_NAME", "DecodeGene")
        self.APP_VERSION = os.getenv("APP_VERSION", "0.1.0")
        self.APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
        self.APP_PORT = int(os.getenv("APP_PORT", "8000"))
        self.DEBUG = _as_bool(os.getenv("DEBUG", "True"), True)
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

        # DeepSeek AI configuration
        self.DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
        self.DEEPSEEK_BASE_URL = os.getenv(
            "DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1"
        ).rstrip("/")
        self.DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
        self.DEEPSEEK_REASONER_MODEL = os.getenv(
            "DEEPSEEK_REASONER_MODEL", "deepseek-reasoner"
        )
        self.DEEPSEEK_TIMEOUT = float(os.getenv("DEEPSEEK_TIMEOUT", "60"))

        # Data directories
        self.DATA_DIR = _resolve_path(os.getenv("DATA_DIR", "../data"))
        self.SAMPLE_DATA_PATH = _resolve_path(
            os.getenv("SAMPLE_DATA_PATH", "../data/sample/demo_associations.json")
        )
        self.PROCESSED_DATA_PATH = _resolve_path(
            os.getenv(
                "PROCESSED_DATA_PATH", "../data/processed/sample_associations.json"
            )
        )
        self.BULK_DATA_PATH = _resolve_path(
            os.getenv(
                "BULK_DATA_PATH", "../data/processed/bulk_associations.json"
            )
        )
        self.BULK_NARRATIVES_PATH = _resolve_path(
            os.getenv(
                "BULK_NARRATIVES_PATH", "../data/processed/bulk_narratives.json"
            )
        )
        self.BULK_NARRATIVES_EN_PATH = _resolve_path(
            os.getenv(
                "BULK_NARRATIVES_EN_PATH", "../data/processed/bulk_narratives_en.json"
            )
        )
        self.SAMPLE_NARRATIVES_EN_PATH = _resolve_path(
            os.getenv(
                "SAMPLE_NARRATIVES_EN_PATH", "../data/processed/sample_narratives_en.json"
            )
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

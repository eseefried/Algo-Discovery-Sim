"""Explicit configuration; credentials are never included in run artifacts."""

import os
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlsplit

from dotenv import load_dotenv


class ConfigurationError(ValueError):
    pass


@dataclass(frozen=True)
class Settings:
    api_key: str = field(repr=False)
    model: str = "claude-haiku-5-5"
    base_url: str = "https://api.anthropic.com"
    max_tokens: int = 8192
    effort: str = "medium"
    timeout_seconds: float = 180
    artifact_dir: Path = Path("artifacts")
    backend: str = "anthropic"

    def __post_init__(self):
        if self.backend not in {"anthropic", "local"}:
            raise ConfigurationError("Model backend must be anthropic or local.")
        if self.backend == "anthropic" and not self.api_key.strip():
            raise ConfigurationError("Set CLAUDE_HACKATHON_API in the environment or .env.")
        if not self.model.strip():
            raise ConfigurationError("CLAUDE_MODEL must not be empty.")
        if not 1024 <= self.max_tokens <= 32768:
            raise ConfigurationError("CLAUDE_MAX_TOKENS must be between 1024 and 32768.")
        if self.effort not in {"low", "medium", "high", "xhigh", "max"}:
            raise ConfigurationError("CLAUDE_EFFORT must be low, medium, high, xhigh, or max.")
        if not 1 <= self.timeout_seconds <= 600:
            raise ConfigurationError("CLAUDE_TIMEOUT_SECONDS must be between 1 and 600.")
        url = urlsplit(self.base_url)
        schemes = {"http", "https"} if self.backend == "local" else {"https"}
        if url.scheme not in schemes or not url.hostname or url.username or url.password:
            raise ConfigurationError("ANTHROPIC_BASE_URL must be an HTTPS URL without credentials.")
        if url.query or url.fragment:
            raise ConfigurationError("ANTHROPIC_BASE_URL must not contain a query or fragment.")

    @classmethod
    def from_env(cls, *, backend: str | None = None, model: str | None = None,
                 base_url: str | None = None) -> "Settings":
        # Read only the current project's .env; existing environment values win.
        load_dotenv(Path.cwd() / ".env", override=False)
        backend = backend or os.getenv("MODEL_BACKEND", "anthropic")
        local = backend == "local"
        try:
            return cls(
                api_key=os.getenv("NEMOTRON_API_KEY" if local else "CLAUDE_HACKATHON_API", ""),
                model=model or (os.getenv("NEMOTRON_MODEL", "nemotron-quantum") if local
                                else os.getenv("CLAUDE_MODEL", "claude-haiku-5-5")),
                base_url=base_url or (os.getenv("NEMOTRON_BASE_URL", "http://127.0.0.1:8000/v1")
                                     if local else os.getenv("ANTHROPIC_BASE_URL", "https://api.anthropic.com")),
                backend=backend,
                max_tokens=int(os.getenv("CLAUDE_MAX_TOKENS", "8192")),
                effort=os.getenv("CLAUDE_EFFORT", "medium"),
                timeout_seconds=float(os.getenv("CLAUDE_TIMEOUT_SECONDS", "180")),
                artifact_dir=Path(os.getenv("ARTIFACT_DIR", "artifacts")),
            )
        except ConfigurationError:
            raise
        except ValueError:
            raise ConfigurationError("Token and timeout settings must be numeric.") from None

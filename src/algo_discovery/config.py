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

    def __post_init__(self):
        if not self.api_key.strip():
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
        if url.scheme != "https" or not url.hostname or url.username or url.password:
            raise ConfigurationError("ANTHROPIC_BASE_URL must be an HTTPS URL without credentials.")
        if url.query or url.fragment:
            raise ConfigurationError("ANTHROPIC_BASE_URL must not contain a query or fragment.")

    @classmethod
    def from_env(cls) -> "Settings":
        # Read only the current project's .env; existing environment values win.
        load_dotenv(Path.cwd() / ".env", override=False)
        try:
            return cls(
                api_key=os.getenv("CLAUDE_HACKATHON_API", ""),
                model=os.getenv("CLAUDE_MODEL", "claude-haiku-5-5"),
                base_url=os.getenv("ANTHROPIC_BASE_URL", "https://api.anthropic.com"),
                max_tokens=int(os.getenv("CLAUDE_MAX_TOKENS", "8192")),
                effort=os.getenv("CLAUDE_EFFORT", "medium"),
                timeout_seconds=float(os.getenv("CLAUDE_TIMEOUT_SECONDS", "180")),
                artifact_dir=Path(os.getenv("ARTIFACT_DIR", "artifacts")),
            )
        except ConfigurationError:
            raise
        except ValueError:
            raise ConfigurationError("Token and timeout settings must be numeric.") from None

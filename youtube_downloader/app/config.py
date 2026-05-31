"""Application configuration assembled from Home Assistant add-on options."""

from __future__ import annotations

import secrets
from dataclasses import dataclass
from pathlib import Path

from .services.ha_options import load_options


@dataclass(frozen=True)
class AppConfig:
    """Validated runtime settings."""

    download_dir: Path
    jobs_dir: Path
    history_file: Path
    max_concurrent_jobs: int
    update_ytdlp_on_start: bool
    allow_external_port: bool
    external_port: int
    debug: bool
    preferred_format: str
    secret_key: str

    @classmethod
    def load(cls) -> "AppConfig":
        """Load validated settings from /data/options.json."""

        options = load_options()
        jobs_dir = Path("/data/jobs")
        jobs_dir.mkdir(parents=True, exist_ok=True)
        options.download_dir.mkdir(parents=True, exist_ok=True)
        return cls(
            download_dir=options.download_dir,
            jobs_dir=jobs_dir,
            history_file=jobs_dir / "history.json",
            max_concurrent_jobs=options.max_concurrent_jobs,
            update_ytdlp_on_start=options.update_ytdlp_on_start,
            allow_external_port=options.allow_external_port,
            external_port=options.external_port,
            debug=options.debug,
            preferred_format=options.preferred_format,
            secret_key=secrets.token_hex(32),
        )

"""Read and validate Home Assistant add-on options."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

LOGGER = logging.getLogger(__name__)
OPTIONS_FILE = Path("/data/options.json")
DEFAULT_DOWNLOAD_DIR = Path("/share/youtube_downloader")
ALLOWED_DOWNLOAD_ROOTS = (Path("/share"), Path("/media"))
PREFERRED_FORMATS = {"best", "audio", "video"}

DEFAULT_OPTIONS: dict[str, Any] = {
    "download_dir": str(DEFAULT_DOWNLOAD_DIR),
    "max_concurrent_jobs": 2,
    "update_ytdlp_on_start": True,
    "allow_external_port": False,
    "external_port": 8099,
    "debug": False,
    "preferred_format": "best",
}


@dataclass(frozen=True)
class HomeAssistantOptions:
    """Validated options provided by Supervisor."""

    download_dir: Path
    max_concurrent_jobs: int
    update_ytdlp_on_start: bool
    allow_external_port: bool
    external_port: int
    debug: bool
    preferred_format: str


def _read_json() -> dict[str, Any]:
    if not OPTIONS_FILE.exists():
        LOGGER.info("Brak %s. Używam wartości domyślnych.", OPTIONS_FILE)
        return {}
    try:
        with OPTIONS_FILE.open("r", encoding="utf-8") as file_handle:
            payload = json.load(file_handle)
        if not isinstance(payload, dict):
            raise ValueError("główny element JSON nie jest obiektem")
        return payload
    except (OSError, ValueError, json.JSONDecodeError) as error:
        LOGGER.error(
            "Nie można odczytać %s: %s. Używam wartości domyślnych.",
            OPTIONS_FILE,
            error,
        )
        return {}


def _validated_download_dir(value: Any) -> Path:
    candidate = Path(str(value)).expanduser()
    if not candidate.is_absolute():
        LOGGER.warning(
            "Katalog pobrań musi być ścieżką bezwzględną. Używam wartości domyślnej."
        )
        return DEFAULT_DOWNLOAD_DIR
    resolved = candidate.resolve()
    if not any(
        resolved == root or root in resolved.parents for root in ALLOWED_DOWNLOAD_ROOTS
    ):
        LOGGER.warning(
            "Katalog pobrań musi znajdować się w /share lub /media. Używam wartości domyślnej."
        )
        return DEFAULT_DOWNLOAD_DIR
    return resolved


def _validated_int(value: Any, default: int, minimum: int, maximum: int) -> int:
    if isinstance(value, bool):
        return default
    try:
        number = int(value)
    except (TypeError, ValueError):
        return default
    return number if minimum <= number <= maximum else default


def _validated_bool(value: Any, default: bool) -> bool:
    return value if isinstance(value, bool) else default


def load_options() -> HomeAssistantOptions:
    """Load options.json and safely fall back for malformed values."""

    provided = _read_json()
    values = {**DEFAULT_OPTIONS, **provided}
    preferred_format = str(values["preferred_format"])
    if preferred_format not in PREFERRED_FORMATS:
        preferred_format = str(DEFAULT_OPTIONS["preferred_format"])

    return HomeAssistantOptions(
        download_dir=_validated_download_dir(values["download_dir"]),
        max_concurrent_jobs=_validated_int(values["max_concurrent_jobs"], 2, 1, 5),
        update_ytdlp_on_start=_validated_bool(values["update_ytdlp_on_start"], True),
        allow_external_port=_validated_bool(values["allow_external_port"], False),
        external_port=_validated_int(values["external_port"], 8099, 1, 65535),
        debug=_validated_bool(values["debug"], False),
        preferred_format=preferred_format,
    )

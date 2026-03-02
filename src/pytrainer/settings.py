"""User settings loader — reads from ~/.config/pytrainer/settings.yaml."""

import logging
from dataclasses import dataclass
from pathlib import Path

import yaml
from platformdirs import user_config_dir

log = logging.getLogger(__name__)

_SETTINGS_DIR = Path(user_config_dir("pytrainer"))
_SETTINGS_FILE = _SETTINGS_DIR / "settings.yaml"


@dataclass
class SessionSettings:
    """Time-limit and warning thresholds for competition sessions."""

    time_limit_minutes: int = 180
    warn_yellow_minutes: int = 30
    warn_red_minutes: int = 10
    beep_last_seconds: int = 10

    @property
    def time_limit_secs(self) -> int:
        return self.time_limit_minutes * 60

    @property
    def warn_yellow_secs(self) -> int:
        return self.warn_yellow_minutes * 60

    @property
    def warn_red_secs(self) -> int:
        return self.warn_red_minutes * 60


@dataclass
class AppSettings:
    """Top-level application settings."""

    session: SessionSettings


def load_settings() -> AppSettings:
    """Load settings from YAML file, falling back to defaults for missing keys."""
    session_kwargs: dict = {}

    if _SETTINGS_FILE.is_file():
        try:
            raw = yaml.safe_load(_SETTINGS_FILE.read_text()) or {}
            session_raw = raw.get("session", {})
            if isinstance(session_raw, dict):
                for field_name in (
                    "time_limit_minutes",
                    "warn_yellow_minutes",
                    "warn_red_minutes",
                    "beep_last_seconds",
                ):
                    if field_name in session_raw:
                        val = session_raw[field_name]
                        if isinstance(val, int) and val >= 0:
                            session_kwargs[field_name] = val
            log.info("Loaded settings from %s", _SETTINGS_FILE)
        except Exception:
            log.warning("Failed to parse %s — using defaults", _SETTINGS_FILE, exc_info=True)
    else:
        log.debug("No settings file at %s — using defaults", _SETTINGS_FILE)

    return AppSettings(session=SessionSettings(**session_kwargs))

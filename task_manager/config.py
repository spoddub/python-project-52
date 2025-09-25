from __future__ import annotations

import logging
import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv


class Config:
    def __init__(self) -> None:
        load_dotenv()
        self.secret_key: str = (
            os.getenv("SECRET_KEY") or "dev-insecure-secret-key"
        )
        debug_env = os.getenv("DJANGO_DEBUG", "").lower()
        env_name = os.getenv("ENV", "").lower()
        self.is_production: bool = (
            debug_env in {"0", "false"} or env_name == "production"
        )
        self.hosts: str = os.getenv("ALLOWED_HOSTS", "")
        self.rollbar_token: str = os.getenv("ROLLBAR_TOKEN", "")

    def setup_database(self, base_dir: Path) -> dict:
        db_url = os.getenv("DATABASE_URL")
        if db_url:
            return dj_database_url.parse(
                db_url,
                conn_max_age=600,
                ssl_require=False,
            )
        logging.warning(
            "No DATABASE_URL environment variable set, falling back to sqlite."
        )
        return {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": str(base_dir / "db.sqlite3"),
        }

    @property
    def allowed_hosts(self) -> list[str]:
        hosts = [h.strip() for h in self.hosts.split(",") if h.strip()]
        if self.is_production:
            return ["webserver", *hosts]
        return hosts or ["*"]

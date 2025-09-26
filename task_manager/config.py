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

        debug_env = (os.getenv("DJANGO_DEBUG") or "").lower()
        env_name = (os.getenv("ENV") or "").lower()
        self.is_production: bool = (
            debug_env in {"0", "false"} or env_name == "production"
        )

        self.hosts: str = os.getenv("ALLOWED_HOSTS", "")
        csrf_env = os.getenv("CSRF_TRUSTED_ORIGINS", "")
        self.csrf_trusted_origins: list[str] = [
            x.strip() for x in csrf_env.split(",") if x.strip()
        ]

        self.rollbar_token: str = os.getenv(
            "ROLLBAR_ACCESS_TOKEN"
        ) or os.getenv("ROLLBAR_TOKEN", "")

    def setup_database(self, base_dir: Path) -> dict:
        db_url = os.getenv("DATABASE_URL")
        if db_url:
            cfg = dj_database_url.parse(
                db_url,
                conn_max_age=600,
                ssl_require=self.is_production,
            )

            engine = cfg.get("ENGINE", "")
            is_postgres = "postgresql" in engine or "postgres" in engine
            if is_postgres and not self.is_production:
                opts = cfg.setdefault("OPTIONS", {})
                opts["sslmode"] = "disable"

            return cfg

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

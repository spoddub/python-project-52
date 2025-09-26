from __future__ import annotations

import logging
import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv


class Config:
    def __init__(self) -> None:
        load_dotenv()

        # --- Secrets/flags ---------------------------------------------------
        self.secret_key: str = (
            os.getenv("SECRET_KEY") or "dev-insecure-secret-key"
        )

        debug_env = (os.getenv("DJANGO_DEBUG", "")).lower()
        env_name = (os.getenv("ENV", "")).lower()
        self.is_production: bool = (
            debug_env in {"0", "false", "no"} or env_name == "production"
        )

        # allow both ALLOWED_HOSTS and legacy HOSTS
        self.hosts_raw: str = (
            os.getenv("ALLOWED_HOSTS") or os.getenv("HOSTS") or ""
        )

        self.rollbar_token: str = os.getenv("ROLLBAR_TOKEN", "")

    # --- Database ------------------------------------------------------------
    def setup_database(self, base_dir: Path) -> dict:
        db_url = os.getenv("DATABASE_URL")
        if db_url:
            # On Render/managed Postgres SSL is required; safe to turn on.
            return dj_database_url.parse(
                db_url, conn_max_age=600, ssl_require=True
            )

        logging.warning(
            "No DATABASE_URL environment variable set, falling back to sqlite."
        )
        return {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": str(base_dir / "db.sqlite3"),
        }

    # --- Hosts/CSRF ----------------------------------------------------------
    @property
    def allowed_hosts(self) -> list[str]:
        # parse env list
        hosts = [h.strip() for h in self.hosts_raw.split(",") if h.strip()]

        # Render provides its public hostname here
        render_host = os.getenv("RENDER_EXTERNAL_HOSTNAME")
        if render_host:
            hosts.append(render_host)

        # dedupe while keeping order
        seen: set[str] = set()
        hosts = [h for h in hosts if not (h in seen or seen.add(h))]

        if self.is_production:
            return ["webserver", *hosts]

        # sensible defaults for local/dev
        return hosts or ["localhost", "127.0.0.1"]

    @property
    def csrf_trusted_origins(self) -> list[str]:
        origins: list[str] = []
        for host in self.allowed_hosts:
            # skip wildcards — they are invalid for CSRF origins
            if host == "*" or host.startswith("*"):
                continue
            origins.append(f"https://{host.lstrip('.')}")
        return origins

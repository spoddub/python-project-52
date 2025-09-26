from __future__ import annotations

import os
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from task_manager.config import Config


class ConfigTests(TestCase):
    def _base_dir(self) -> Path:
        return Path(__file__).resolve().parents[3]

    def test_secret_key_defaults_when_missing(self) -> None:
        with patch.dict(os.environ, {"SECRET_KEY": ""}, clear=False):
            cfg = Config()
            self.assertTrue(cfg.secret_key)

    def test_allowed_hosts_dev_no_hosts_gives_wildcard(self) -> None:
        with patch.dict(
            os.environ, {"DJANGO_DEBUG": "1", "ALLOWED_HOSTS": ""}, clear=False
        ):
            cfg = Config()
            self.assertEqual(cfg.allowed_hosts, ["*"])

    def test_allowed_hosts_dev_list(self) -> None:
        with patch.dict(
            os.environ,
            {"DJANGO_DEBUG": "1", "ALLOWED_HOSTS": "a.com, b.com  "},
            clear=False,
        ):
            cfg = Config()
            self.assertEqual(cfg.allowed_hosts, ["a.com", "b.com"])

    def test_allowed_hosts_prod_prefix_webserver(self) -> None:
        with patch.dict(
            os.environ,
            {"DJANGO_DEBUG": "0", "ALLOWED_HOSTS": "example.com"},
            clear=False,
        ):
            cfg = Config()
            self.assertTrue(cfg.is_production)
            self.assertEqual(cfg.allowed_hosts, ["webserver", "example.com"])

    def test_database_fallback_sqlite_when_url_missing(self) -> None:
        with patch.dict(
            os.environ, {"DATABASE_URL": "", "DJANGO_DEBUG": "1"}, clear=False
        ):
            cfg = Config()
            db = cfg.setup_database(self._base_dir())
            self.assertEqual(db["ENGINE"], "django.db.backends.sqlite3")
            self.assertTrue(
                str(self._base_dir() / "db.sqlite3").endswith(db["NAME"])
            )

    def test_database_postgres_dev_forces_sslmode_disable(self) -> None:
        with patch.dict(
            os.environ,
            {
                "DJANGO_DEBUG": "1",
                "DATABASE_URL": "postgresql://user:pass@localhost:5432/appdb",
            },
            clear=False,
        ):
            cfg = Config()
            db = cfg.setup_database(self._base_dir())
            self.assertIn("postgresql", db["ENGINE"])
            self.assertIn("OPTIONS", db)
            self.assertEqual(db["OPTIONS"].get("sslmode"), "disable")

    def test_database_postgres_prod_keeps_ssl(self) -> None:
        with patch.dict(
            os.environ,
            {
                "DJANGO_DEBUG": "0",  # prod
                "DATABASE_URL": "postgresql://user:pass@localhost:5432/appdb",
            },
            clear=False,
        ):
            cfg = Config()
            db = cfg.setup_database(self._base_dir())
            self.assertIn("postgresql", db["ENGINE"])
            self.assertTrue(
                "OPTIONS" not in db or db["OPTIONS"].get("sslmode") != "disable"
            )

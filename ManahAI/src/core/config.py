from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Mapping


_PRODUCTION_REQUIREMENTS = (
    "DATABASE_URL",
    "PII_ENCRYPTION_KEY",
    "CRISIS_RESOURCES_FILE",
    "COORDINATOR_ALERT_URL",
)


@dataclass(frozen=True)
class Settings:
    app_env: str
    safety_classifier_provider: str
    database_url: str | None
    pii_encryption_key: str | None
    crisis_resources_file: str | None
    coordinator_alert_url: str | None
    whatsapp_access_token: str | None
    whatsapp_verify_token: str | None
    whatsapp_app_secret: str | None

    @classmethod
    def from_environment(cls, environ: Mapping[str, str] | None = None) -> Settings:
        values = os.environ if environ is None else environ
        app_env = values.get("APP_ENV", "development").strip().lower()
        if app_env not in {"development", "test", "production"}:
            raise ValueError("APP_ENV must be development, test, or production.")

        safety_classifier_provider = values.get(
            "SAFETY_CLASSIFIER_PROVIDER",
            "development_rules",
        ).strip()
        if not safety_classifier_provider:
            raise ValueError("SAFETY_CLASSIFIER_PROVIDER must not be empty.")

        settings = cls(
            app_env=app_env,
            safety_classifier_provider=safety_classifier_provider,
            database_url=values.get("DATABASE_URL") or None,
            pii_encryption_key=values.get("PII_ENCRYPTION_KEY") or None,
            crisis_resources_file=values.get("CRISIS_RESOURCES_FILE") or None,
            coordinator_alert_url=values.get("COORDINATOR_ALERT_URL") or None,
            whatsapp_access_token=values.get("WHATSAPP_ACCESS_TOKEN") or None,
            whatsapp_verify_token=values.get("WHATSAPP_VERIFY_TOKEN") or None,
            whatsapp_app_secret=values.get("WHATSAPP_APP_SECRET") or None,
        )
        settings.validate_for_environment()
        return settings

    def validate_for_environment(self) -> None:
        if self.app_env != "production":
            return

        configured_values = {
            "DATABASE_URL": self.database_url,
            "PII_ENCRYPTION_KEY": self.pii_encryption_key,
            "CRISIS_RESOURCES_FILE": self.crisis_resources_file,
            "COORDINATOR_ALERT_URL": self.coordinator_alert_url,
        }
        missing = [name for name in _PRODUCTION_REQUIREMENTS if not configured_values[name]]
        if missing:
            raise ValueError(
                "Production configuration is incomplete: " + ", ".join(missing)
            )
        if self.safety_classifier_provider == "development_rules":
            raise ValueError(
                "The development-only keyword classifier cannot be used in production."
            )

import unittest

from src.core.config import Settings


class SettingsTests(unittest.TestCase):
    def test_development_defaults_to_nonproduction_classifier(self) -> None:
        settings = Settings.from_environment({})

        self.assertEqual(settings.app_env, "development")
        self.assertEqual(settings.safety_classifier_provider, "development_rules")

    def test_production_rejects_missing_integrations(self) -> None:
        with self.assertRaisesRegex(ValueError, "Production configuration is incomplete"):
            Settings.from_environment({"APP_ENV": "production"})

    def test_production_rejects_development_classifier(self) -> None:
        values = {
            "APP_ENV": "production",
            "DATABASE_URL": "postgresql+asyncpg://configured",
            "PII_ENCRYPTION_KEY": "configured",
            "CRISIS_RESOURCES_FILE": "configured",
            "COORDINATOR_ALERT_URL": "configured",
            "SAFETY_CLASSIFIER_PROVIDER": "development_rules",
        }

        with self.assertRaisesRegex(ValueError, "development-only keyword classifier"):
            Settings.from_environment(values)

    def test_production_requires_explicit_classifier_provider(self) -> None:
        values = {
            "APP_ENV": "production",
            "DATABASE_URL": "postgresql+asyncpg://configured",
            "PII_ENCRYPTION_KEY": "configured",
            "CRISIS_RESOURCES_FILE": "configured",
            "COORDINATOR_ALERT_URL": "configured",
            "SAFETY_CLASSIFIER_PROVIDER": "approved_provider",
        }

        settings = Settings.from_environment(values)

        self.assertEqual(settings.safety_classifier_provider, "approved_provider")


if __name__ == "__main__":
    unittest.main()

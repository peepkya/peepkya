import unittest

from src.core.privacy import (
    PrivacyRedactionError,
    mask_pii,
    redact_for_external_llm,
)


class PrivacyTests(unittest.TestCase):
    def test_masks_email_phone_and_indian_pan_identifiers(self) -> None:
        redacted = mask_pii(
            "Contact anita@example.org or +91 98765 43210; PAN ABCDE1234F."
        )

        self.assertNotIn("anita@example.org", redacted)
        self.assertNotIn("98765 43210", redacted)
        self.assertNotIn("ABCDE1234F", redacted)
        self.assertIn("[REDACTED_EMAIL]", redacted)
        self.assertIn("[REDACTED_PHONE]", redacted)
        self.assertIn("[REDACTED_ID]", redacted)

    def test_masks_common_us_identifiers(self) -> None:
        redacted = mask_pii("SSN 123-45-6789")

        self.assertNotIn("123-45-6789", redacted)
        self.assertIn("[REDACTED_ID]", redacted)

    def test_rejects_non_text_input(self) -> None:
        with self.assertRaises(PrivacyRedactionError):
            mask_pii(None)  # type: ignore[arg-type]

    def test_external_llm_redaction_fails_closed_on_empty_result(self) -> None:
        class EmptyRedactor:
            def redact(self, text: str) -> str:
                del text
                return " "

        with self.assertRaises(PrivacyRedactionError):
            redact_for_external_llm("private context", EmptyRedactor())

    def test_external_llm_redaction_returns_masked_context(self) -> None:
        class RegexRedactor:
            def redact(self, text: str) -> str:
                return mask_pii(text)

        redacted = redact_for_external_llm(
            "Email anita@example.org",
            RegexRedactor(),
        )

        self.assertNotIn("anita@example.org", redacted)


if __name__ == "__main__":
    unittest.main()

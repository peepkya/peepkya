from __future__ import annotations

import re
from typing import Protocol


class PrivacyRedactionError(Exception):
    """Raised when input cannot be safely prepared for an external LLM."""


class PIIRedactor(Protocol):
    def redact(self, text: str) -> str:
        """Return text with detected identifiers removed or masked."""


_PATTERNS = (
    (re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE), "[REDACTED_EMAIL]"),
    (
        re.compile(
            r"(?<!\w)(?:\+\d{1,3}[\s().-]*)?(?:\(?\d{2,5}\)?[\s().-]*)?"
            r"\d{3,5}[\s().-]*\d{3,5}(?!\w)"
        ),
        "[REDACTED_PHONE]",
    ),
    (re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), "[REDACTED_ID]"),
    (re.compile(r"\b[A-Z]{5}\d{4}[A-Z]\b", re.IGNORECASE), "[REDACTED_ID]"),
)


def mask_pii(text: str) -> str:
    if not isinstance(text, str):
        raise PrivacyRedactionError("Only text can be scrubbed for PII.")

    redacted = text
    for pattern, replacement in _PATTERNS:
        redacted = pattern.sub(replacement, redacted)
    return redacted


def redact_for_external_llm(text: str, redactor: PIIRedactor) -> str:
    """Fail closed if a configured redactor does not produce usable text."""
    if not isinstance(text, str):
        raise PrivacyRedactionError("Only text can be prepared for an external LLM.")
    redacted = redactor.redact(text)
    if not isinstance(redacted, str) or not redacted.strip():
        raise PrivacyRedactionError("PII redaction did not produce safe text.")
    return redacted

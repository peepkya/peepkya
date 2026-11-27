"""Safety assessment primitives.

The keyword classifier is a development aid, not a clinically validated or
multilingual production classifier. Production wiring must use an approved
classifier and retain the same fail-closed routing behavior.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from enum import Enum
from typing import Protocol


class AssessmentStatus(str, Enum):
    CLEAR = "clear"
    DETECTED = "detected"
    UNCERTAIN = "uncertain"


class RiskCategory(str, Enum):
    SELF_HARM = "self_harm"
    SUICIDAL_IDEATION = "suicidal_ideation"
    VIOLENCE = "violence"
    ACUTE_MEDICAL_EMERGENCY = "acute_medical_emergency"


@dataclass(frozen=True)
class SafetyAssessment:
    status: AssessmentStatus
    categories: tuple[RiskCategory, ...] = ()
    reason: str | None = None


class SafetyCheckUnavailable(Exception):
    """Raised when a configured safety assessment provider cannot respond."""


class SafetyClassifier(Protocol):
    def assess(self, text: str) -> SafetyAssessment:
        """Return a safety assessment without generating user-facing advice."""


class KeywordSafetyClassifier:
    """Conservative English-only keyword detector for local development and tests."""

    _PATTERNS: dict[RiskCategory, tuple[re.Pattern[str], ...]] = {
        RiskCategory.SELF_HARM: (
            re.compile(r"\bself[\s-]?harm(?:ing)?\b", re.IGNORECASE),
            re.compile(r"\bhurt(?:ing)? myself\b", re.IGNORECASE),
            re.compile(r"\bcut(?:ting)? myself\b", re.IGNORECASE),
            re.compile(r"\bharm myself\b", re.IGNORECASE),
            re.compile(r"\binjure myself\b", re.IGNORECASE),
        ),
        RiskCategory.SUICIDAL_IDEATION: (
            re.compile(r"\bsuicid(?:e|al)\b", re.IGNORECASE),
            re.compile(r"\bkill myself\b", re.IGNORECASE),
            re.compile(r"\bend my life\b", re.IGNORECASE),
            re.compile(r"\bwant to die\b", re.IGNORECASE),
            re.compile(r"\bwish i were dead\b", re.IGNORECASE),
            re.compile(r"\bnot worth living\b", re.IGNORECASE),
        ),
        RiskCategory.VIOLENCE: (
            re.compile(r"\bhurt someone\b", re.IGNORECASE),
            re.compile(r"\bkill (?:him|her|them|someone)\b", re.IGNORECASE),
            re.compile(r"\bharm (?:him|her|them|someone)\b", re.IGNORECASE),
            re.compile(r"\bthreatening someone\b", re.IGNORECASE),
            re.compile(r"\bviolent\b", re.IGNORECASE),
            re.compile(r"\battacking someone\b", re.IGNORECASE),
        ),
        RiskCategory.ACUTE_MEDICAL_EMERGENCY: (
            re.compile(r"\bcan(?:not|'t) breathe\b", re.IGNORECASE),
            re.compile(r"\bnot breathing\b", re.IGNORECASE),
            re.compile(r"\bunconscious\b", re.IGNORECASE),
            re.compile(r"\boverdose\b", re.IGNORECASE),
            re.compile(r"\bseizure\b", re.IGNORECASE),
            re.compile(r"\bchest pain\b", re.IGNORECASE),
            re.compile(r"\bsevere bleeding\b", re.IGNORECASE),
            re.compile(r"\bmedical emergency\b", re.IGNORECASE),
        ),
    }

    def assess(self, text: str) -> SafetyAssessment:
        normalized = unicodedata.normalize("NFKC", text).strip()
        if not normalized:
            return SafetyAssessment(AssessmentStatus.UNCERTAIN, reason="empty_input")

        if self._contains_unsupported_script(normalized):
            return SafetyAssessment(
                AssessmentStatus.UNCERTAIN,
                reason="unsupported_language",
            )

        categories = tuple(
            category
            for category, patterns in self._PATTERNS.items()
            if any(pattern.search(normalized) for pattern in patterns)
        )
        if categories:
            return SafetyAssessment(AssessmentStatus.DETECTED, categories)

        words = re.findall(r"\b[\w'-]+\b", normalized)
        if len(words) < 4:
            return SafetyAssessment(AssessmentStatus.UNCERTAIN, reason="ambiguous_input")

        return SafetyAssessment(AssessmentStatus.CLEAR)

    @staticmethod
    def _contains_unsupported_script(text: str) -> bool:
        for character in text:
            if not character.isalpha() or character.isascii():
                continue
            if "LATIN" not in unicodedata.name(character, ""):
                return True
        return False


class SafetyGuard:
    def __init__(self, classifier: SafetyClassifier) -> None:
        self._classifier = classifier

    def assess(self, text: str) -> SafetyAssessment:
        try:
            return self._classifier.assess(text)
        except SafetyCheckUnavailable:
            return SafetyAssessment(
                AssessmentStatus.UNCERTAIN,
                reason="assessment_unavailable",
            )

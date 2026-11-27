import unittest

from src.agents.safety_guard import (
    AssessmentStatus,
    KeywordSafetyClassifier,
    RiskCategory,
    SafetyCheckUnavailable,
    SafetyAssessment,
    SafetyGuard,
)


class SafetyGuardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.guard = SafetyGuard(KeywordSafetyClassifier())

    def test_detects_self_harm_and_suicidal_ideation(self) -> None:
        assessment = self.guard.assess("I want to hurt myself and end my life")

        self.assertEqual(assessment.status, AssessmentStatus.DETECTED)
        self.assertIn(RiskCategory.SELF_HARM, assessment.categories)
        self.assertIn(RiskCategory.SUICIDAL_IDEATION, assessment.categories)

    def test_detects_violence(self) -> None:
        assessment = self.guard.assess("He is threatening someone and may hurt them")

        self.assertEqual(assessment.status, AssessmentStatus.DETECTED)
        self.assertIn(RiskCategory.VIOLENCE, assessment.categories)

    def test_detects_acute_medical_emergency(self) -> None:
        assessment = self.guard.assess("She is unconscious and not breathing")

        self.assertEqual(assessment.status, AssessmentStatus.DETECTED)
        self.assertIn(RiskCategory.ACUTE_MEDICAL_EMERGENCY, assessment.categories)

    def test_short_or_unsupported_input_is_uncertain(self) -> None:
        self.assertEqual(
            self.guard.assess("help").status,
            AssessmentStatus.UNCERTAIN,
        )
        self.assertEqual(
            self.guard.assess("मला मदत हवी आहे").status,
            AssessmentStatus.UNCERTAIN,
        )

    def test_classifier_outage_fails_closed_to_uncertain(self) -> None:
        class UnavailableClassifier:
            def assess(self, text: str) -> SafetyAssessment:
                del text
                raise SafetyCheckUnavailable("assessment service unavailable")

        assessment = SafetyGuard(UnavailableClassifier()).assess("A sufficiently long message")

        self.assertEqual(assessment.status, AssessmentStatus.UNCERTAIN)
        self.assertEqual(assessment.reason, "assessment_unavailable")

    def test_benign_message_is_clear(self) -> None:
        assessment = self.guard.assess(
            "The afternoon was quiet and we watched a movie together"
        )

        self.assertEqual(assessment.status, AssessmentStatus.CLEAR)
        self.assertEqual(assessment.categories, ())


if __name__ == "__main__":
    unittest.main()

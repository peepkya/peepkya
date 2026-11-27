import unittest
from datetime import date

from src.agents.crisis_flow import (
    AssessmentStatus,
    CrisisFlow,
    DefaultCrisisCoach,
    EscalationStatus,
    Strategy,
)
from src.agents.safety_guard import KeywordSafetyClassifier, SafetyGuard
from src.agents.safety_guard import RiskCategory
from src.models.crisis import CrisisPlan, VerifiedHelpline
from src.services.coordinator_alerts import AlertOutcome
from src.services.crisis_resources import CrisisResourceDirectory


class FakeCoordinatorAlerter:
    def __init__(self, outcome: AlertOutcome) -> None:
        self.outcome = outcome
        self.calls: list[tuple[str, tuple[RiskCategory, ...]]] = []

    def alert(
        self,
        *,
        region: str,
        categories: tuple[RiskCategory, ...],
    ) -> AlertOutcome:
        self.calls.append((region, categories))
        return self.outcome


class SpyCoach(DefaultCrisisCoach):
    def __init__(self) -> None:
        self.calls = 0

    def respond(self, plan: CrisisPlan) -> tuple[str, str, str]:
        self.calls += 1
        return super().respond(plan)


class CrisisFlowTests(unittest.TestCase):
    def setUp(self) -> None:
        helpline = VerifiedHelpline(
            region="IN-MH",
            name="Test crisis line",
            phone_number="+999000000001",
            verified=True,
            active=True,
            verified_at=date(2026, 11, 27),
        )
        self.resources = CrisisResourceDirectory([helpline])
        self.coordinator = FakeCoordinatorAlerter(AlertOutcome.SENT)
        self.coach = SpyCoach()
        self.flow = CrisisFlow(
            safety_guard=SafetyGuard(KeywordSafetyClassifier()),
            resources=self.resources,
            coordinator=self.coordinator,
            coach=self.coach,
        )
        self.plan = CrisisPlan(
            calming_strategies=(
                Strategy.REDUCE_STIMULATION,
                Strategy.SPEAK_CALMLY,
                Strategy.GIVE_SPACE,
            )
        )

    def test_detected_danger_escalates_without_calling_coach(self) -> None:
        response = self.flow.handle(
            "I want to kill myself",
            region="IN-MH",
            plan=self.plan,
        )

        self.assertEqual(response.status, AssessmentStatus.DETECTED)
        self.assertEqual(response.escalation_status, EscalationStatus.ALERT_SENT)
        self.assertEqual(len(response.helplines), 1)
        self.assertIn("+999000000001", response.text)
        self.assertEqual(self.coach.calls, 0)
        self.assertEqual(len(self.coordinator.calls), 1)

    def test_unverified_resource_is_never_displayed(self) -> None:
        directory = CrisisResourceDirectory(
            [
                VerifiedHelpline(
                    region="IN-MH",
                    name="Unverified line",
                    phone_number="+999000000002",
                    verified=False,
                    active=True,
                    verified_at=date(2026, 11, 27),
                )
            ]
        )
        flow = CrisisFlow(
            safety_guard=SafetyGuard(KeywordSafetyClassifier()),
            resources=directory,
            coordinator=self.coordinator,
            coach=self.coach,
        )

        response = flow.handle(
            "She is unconscious and not breathing",
            region="IN-MH",
            plan=self.plan,
        )

        self.assertEqual(response.helplines, ())
        self.assertNotIn("+999000000002", response.text)
        self.assertIn("local emergency services", response.text)

    def test_coordinator_failure_is_reported_without_hiding_helplines(self) -> None:
        coordinator = FakeCoordinatorAlerter(AlertOutcome.FAILED)
        flow = CrisisFlow(
            safety_guard=SafetyGuard(KeywordSafetyClassifier()),
            resources=self.resources,
            coordinator=coordinator,
            coach=self.coach,
        )

        response = flow.handle(
            "He is threatening someone and may hurt them",
            region="IN-MH",
            plan=self.plan,
        )

        self.assertEqual(response.escalation_status, EscalationStatus.ALERT_FAILED)
        self.assertIn("+999000000001", response.text)
        self.assertIn("could not be delivered", response.text)

    def test_emergency_response_respects_fifty_word_limit(self) -> None:
        helplines = [
            VerifiedHelpline(
                region="IN-MH",
                name=f"Test crisis line {index}",
                phone_number=f"+999000000{index:03d}",
                verified=True,
                active=True,
                verified_at=date(2026, 11, 27),
            )
            for index in range(1, 21)
        ]
        flow = CrisisFlow(
            safety_guard=SafetyGuard(KeywordSafetyClassifier()),
            resources=CrisisResourceDirectory(helplines),
            coordinator=self.coordinator,
            coach=self.coach,
        )

        response = flow.handle(
            "I want to kill myself",
            region="IN-MH",
            plan=self.plan,
        )

        self.assertLessEqual(len(response.text.split()), 50)
        self.assertTrue(response.helplines)
        self.assertLess(len(response.helplines), len(helplines))

    def test_uncertain_input_asks_a_physical_safety_question(self) -> None:
        response = self.flow.handle("help", region="IN-MH", plan=self.plan)

        self.assertEqual(response.status, AssessmentStatus.UNCERTAIN)
        self.assertIn("physically safe", response.text)
        self.assertEqual(self.coach.calls, 0)
        self.assertEqual(self.coordinator.calls, [])

    def test_plan_response_has_three_steps_and_at_most_fifty_words(self) -> None:
        response = self.flow.handle(
            "The room has been quiet and we are sitting together safely",
            region="IN-MH",
            plan=self.plan,
        )

        self.assertEqual(response.status, AssessmentStatus.CLEAR)
        self.assertEqual(len(response.steps), 3)
        self.assertLessEqual(len(response.text.split()), 50)
        self.assertEqual(self.coach.calls, 1)

    def test_missing_plan_uses_safety_check_instead_of_inventing_personalization(self) -> None:
        response = self.flow.handle(
            "The room has been quiet and we are sitting together safely",
            region="IN-MH",
            plan=None,
        )

        self.assertEqual(response.status, AssessmentStatus.CLEAR)
        self.assertIn("physically safe", response.text)
        self.assertEqual(response.steps, ())
        self.assertEqual(self.coach.calls, 0)


if __name__ == "__main__":
    unittest.main()

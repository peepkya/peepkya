"""Deterministic crisis routing that always evaluates safety before coaching."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Protocol

from src.agents.safety_guard import AssessmentStatus, RiskCategory, SafetyGuard
from src.models.crisis import CrisisPlan, Strategy, VerifiedHelpline
from src.services.coordinator_alerts import AlertOutcome
from src.services.crisis_resources import CrisisResourceDirectory


class EscalationStatus(str, Enum):
    ALERT_SENT = "alert_sent"
    ALERT_FAILED = "alert_failed"
    ALERT_NOT_CONFIGURED = "alert_not_configured"


@dataclass(frozen=True)
class CrisisResponse:
    status: AssessmentStatus
    text: str
    steps: tuple[str, ...] = ()
    helplines: tuple[VerifiedHelpline, ...] = ()
    escalation_status: EscalationStatus | None = None


class CoordinatorAlerter(Protocol):
    def alert(
        self,
        *,
        region: str,
        categories: tuple[RiskCategory, ...],
    ) -> AlertOutcome:
        """Queue a coordinator alert and report its delivery state."""


class CrisisCoach(Protocol):
    def respond(self, plan: CrisisPlan) -> tuple[str, str, str]:
        """Return three concise, non-clinical steps from an approved plan."""


class DefaultCrisisCoach:
    _TEMPLATES: dict[Strategy, str] = {
        Strategy.REDUCE_STIMULATION: "Reduce noise and other stimulation.",
        Strategy.SPEAK_CALMLY: "Speak slowly in short, calm sentences.",
        Strategy.GIVE_SPACE: "Give them space and keep a clear exit.",
        Strategy.OFFER_GROUNDING: "Ask whether they would like a simple grounding exercise.",
        Strategy.CONTACT_TRUSTED_SUPPORT: "Ask whether they want a trusted support person.",
    }
    _FALLBACKS = (
        Strategy.SPEAK_CALMLY,
        Strategy.REDUCE_STIMULATION,
        Strategy.GIVE_SPACE,
    )

    def respond(self, plan: CrisisPlan) -> tuple[str, str, str]:
        selected: list[Strategy] = []
        for strategy in (*plan.calming_strategies, *self._FALLBACKS):
            if strategy not in selected:
                selected.append(strategy)
            if len(selected) == 3:
                break

        if len(selected) != 3:
            raise ValueError("A crisis response requires three approved strategies.")
        return (
            self._TEMPLATES[selected[0]],
            self._TEMPLATES[selected[1]],
            self._TEMPLATES[selected[2]],
        )


class CrisisFlow:
    def __init__(
        self,
        *,
        safety_guard: SafetyGuard,
        resources: CrisisResourceDirectory,
        coordinator: CoordinatorAlerter,
        coach: CrisisCoach,
    ) -> None:
        self._safety_guard = safety_guard
        self._resources = resources
        self._coordinator = coordinator
        self._coach = coach

    def handle(
        self,
        message: str,
        *,
        region: str,
        plan: CrisisPlan | None,
    ) -> CrisisResponse:
        assessment = self._safety_guard.assess(message)

        if assessment.status is AssessmentStatus.DETECTED:
            return self._escalate(region=region, categories=assessment.categories)

        if assessment.status is AssessmentStatus.UNCERTAIN:
            return CrisisResponse(
                status=assessment.status,
                text=(
                    "Are you and your loved one physically safe right now? "
                    "If anyone is in immediate danger, contact local emergency services."
                ),
            )

        if plan is None:
            return CrisisResponse(
                status=assessment.status,
                text=(
                    "I don't have a confirmed crisis plan to personalize these steps. "
                    "Are you and your loved one physically safe right now?"
                ),
            )

        steps = self._coach.respond(plan)
        if len(steps) != 3:
            raise ValueError("The crisis coach must return exactly three steps.")
        text = "\n".join(f"{index}. {step}" for index, step in enumerate(steps, start=1))
        if len(text.split()) > 50:
            raise ValueError("Crisis-mode response exceeds the 50-word limit.")

        return CrisisResponse(
            status=assessment.status,
            text=text,
            steps=steps,
        )

    def _escalate(
        self,
        *,
        region: str,
        categories: tuple[RiskCategory, ...],
    ) -> CrisisResponse:
        available_helplines = self._resources.for_region(region)
        alert_outcome = self._coordinator.alert(region=region, categories=categories)
        escalation_status = {
            AlertOutcome.SENT: EscalationStatus.ALERT_SENT,
            AlertOutcome.FAILED: EscalationStatus.ALERT_FAILED,
            AlertOutcome.NOT_CONFIGURED: EscalationStatus.ALERT_NOT_CONFIGURED,
        }[alert_outcome]

        alert_text = {
            EscalationStatus.ALERT_SENT: "The coordinator has been alerted.",
            EscalationStatus.ALERT_FAILED: "The coordinator alert could not be delivered.",
            EscalationStatus.ALERT_NOT_CONFIGURED: "Coordinator alerting is not configured.",
        }[escalation_status]

        if available_helplines:
            prefix = "This may be an emergency. Contact a verified local helpline now."
            displayed_helplines: list[VerifiedHelpline] = []
            for helpline in available_helplines:
                candidate_helplines = (*displayed_helplines, helpline)
                resource_text = " ".join(
                    f"{item.name}: {item.phone_number}." for item in candidate_helplines
                )
                candidate_text = f"{prefix} {resource_text} {alert_text}"
                if len(candidate_text.split()) > 50:
                    break
                displayed_helplines.append(helpline)
            helplines = tuple(displayed_helplines)
            text = (
                f"{prefix} "
                f"{' '.join(f'{item.name}: {item.phone_number}.' for item in helplines)} "
                f"{alert_text}"
            )
        else:
            helplines = ()
            text = (
                "No verified local crisis helpline is configured. "
                f"If anyone is in immediate danger, contact local emergency services now. {alert_text}"
            )

        if len(text.split()) > 50:
            raise ValueError("Emergency response exceeds the 50-word limit.")

        return CrisisResponse(
            status=AssessmentStatus.DETECTED,
            text=text,
            helplines=helplines,
            escalation_status=escalation_status,
        )

from enum import Enum

from src.agents.safety_guard import RiskCategory


class AlertOutcome(str, Enum):
    SENT = "sent"
    FAILED = "failed"
    NOT_CONFIGURED = "not_configured"


class UnconfiguredCoordinatorAlerter:
    """Explicit local-development adapter; it never claims an alert was sent."""

    def alert(
        self,
        *,
        region: str,
        categories: tuple[RiskCategory, ...],
    ) -> AlertOutcome:
        _ = (region, categories)
        return AlertOutcome.NOT_CONFIGURED

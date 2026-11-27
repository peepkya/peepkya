from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from enum import Enum


class Strategy(str, Enum):
    REDUCE_STIMULATION = "reduce_stimulation"
    SPEAK_CALMLY = "speak_calmly"
    GIVE_SPACE = "give_space"
    OFFER_GROUNDING = "offer_grounding"
    CONTACT_TRUSTED_SUPPORT = "contact_trusted_support"


@dataclass(frozen=True)
class CrisisPlan:
    calming_strategies: tuple[Strategy, ...]


@dataclass(frozen=True)
class VerifiedHelpline:
    region: str
    name: str
    phone_number: str
    verified: bool
    active: bool
    verified_at: date

    def __post_init__(self) -> None:
        if not self.region.strip():
            raise ValueError("Helpline region must not be empty.")
        if not self.name.strip():
            raise ValueError("Helpline name must not be empty.")
        if not re.fullmatch(r"\+[1-9]\d{2,14}", self.phone_number):
            raise ValueError("Helpline phone number must use international E.164 format.")

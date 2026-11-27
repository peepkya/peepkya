from collections.abc import Iterable

from src.models.crisis import VerifiedHelpline


class CrisisResourceDirectory:
    def __init__(self, helplines: Iterable[VerifiedHelpline]) -> None:
        self._helplines = tuple(helplines)

    def for_region(self, region: str) -> tuple[VerifiedHelpline, ...]:
        normalized_region = region.strip().casefold()
        if not normalized_region:
            return ()
        return tuple(
            helpline
            for helpline in self._helplines
            if helpline.region.strip().casefold() == normalized_region
            and helpline.verified
            and helpline.active
        )

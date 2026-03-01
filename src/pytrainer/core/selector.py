"""Tier-based random exercise selection."""

import logging
import random

from pytrainer.models.exercise import Exercise, ExerciseIndex

log = logging.getLogger(__name__)

DEFAULT_DISTRIBUTION: dict[int, int] = {1: 8, 2: 8, 3: 6, 4: 5, 5: 3}


def select_session(
    exercise_index: ExerciseIndex,
    distribution: dict[int, int] | None = None,
) -> list[Exercise]:
    """Select exercises from the index according to tier distribution.

    Returns exercises in ascending tier order.
    """
    dist = distribution or DEFAULT_DISTRIBUTION
    selected: list[Exercise] = []

    for tier in sorted(dist):
        needed = dist[tier]
        available = exercise_index.get(tier, [])

        if len(available) < needed:
            if available:
                log.warning(
                    "Tier %d has %d exercises but %d requested — selecting all",
                    tier,
                    len(available),
                    needed,
                )
            else:
                log.warning("Tier %d has no exercises — skipping", tier)
            selected.extend(available)
        else:
            selected.extend(random.sample(available, needed))

    return selected

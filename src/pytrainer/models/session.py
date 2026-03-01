"""Session-related data models and enums."""

from dataclasses import dataclass, field
from enum import Enum

from pytrainer.models.exercise import Exercise


class ProblemStatus(Enum):
    """Status of a problem within a session."""

    UNSOLVED = "unsolved"
    ATTEMPTED = "attempted"
    SOLVED = "solved"


class DifficultyMode(Enum):
    """Session difficulty mode."""

    BEGINNER = "beginner"
    MEDIUM = "medium"
    DIFFICULT = "difficult"


@dataclass
class ProblemState:
    """Mutable state of a single problem during a session."""

    exercise: Exercise
    code: str = ""
    status: ProblemStatus = ProblemStatus.UNSOLVED
    attempts: int = 0
    time_spent: float = 0.0
    score: int = 0
    hint_viewed: bool = False
    solution_viewed: bool = False


@dataclass
class SessionConfig:
    """Configuration for a competition session."""

    mode: DifficultyMode
    total_time: int = 10800
    tier_distribution: dict[int, int] = field(
        default_factory=lambda: {1: 8, 2: 8, 3: 6, 4: 5, 5: 3}
    )


@dataclass
class SessionResult:
    """Results from a completed session."""

    session_id: str
    date: str
    config: SessionConfig
    problems: list[ProblemState]
    total_score: int
    max_score: int = 925
    time_used: float = 0.0
    time_paused: float = 0.0

# E1-S03: Define Core Data Models

## Status
Done

## Epic
E1 - Project Foundation & Dev Environment

## Priority
Critical

## Estimate
S

## Description
[PCT] Implement all dataclasses and enums that form the data layer: Exercise, TestCase, ExerciseIndex type alias, ProblemState, ProblemStatus, DifficultyMode, SessionConfig, SessionResult. These models are the shared vocabulary used by every module in the system.

## Acceptance Criteria
- [x] models/exercise.py contains Exercise and TestCase dataclasses with all fields from architecture spec
- [x] TestCase has lazy-loading properties for input_text and expected_output
- [x] models/session.py contains ProblemState, SessionConfig, SessionResult dataclasses
- [x] ProblemStatus enum has UNSOLVED, ATTEMPTED, SOLVED values
- [x] DifficultyMode enum has BEGINNER, MEDIUM, DIFFICULT values
- [x] All models are importable from pytrainer.models

## Tasks
- **T1: Implement exercise models** — Create models/exercise.py with TestCase (lazy file loading via @property), Exercise (all fields: id, title, tier, topic, description, time_estimate, test_cases, hint, solution, source, validation, tolerance), and ExerciseIndex = dict[int, list[Exercise]] type alias.
- **T2: Implement session models** — Create models/session.py with ProblemStatus enum, DifficultyMode enum, ProblemState dataclass, SessionConfig dataclass (with default tier_distribution {1:8, 2:8, 3:6, 4:5, 5:3}), and SessionResult dataclass.

## Technical Notes
- Use @dataclass(frozen=False) — ProblemState is mutable during session
- TestCase lazy loading: store file paths, read content only on first property access
- SessionConfig default tier_distribution uses field(default_factory=lambda: {1:8,2:8,3:6,4:5,5:3})
- Use Python 3.10+ union syntax: str | None instead of Optional[str]

## Dependencies
- E1-S01 (Initialize Project Structure) -- provides the models/ package directory.

## Implementation Summary

**Files Created/Modified:**
- `src/pytrainer/models/exercise.py` — TestCase, Exercise, ExerciseIndex (~47 lines)
- `src/pytrainer/models/session.py` — ProblemStatus, DifficultyMode, ProblemState, SessionConfig, SessionResult (~55 lines)
- `src/pytrainer/models/__init__.py` — Re-exports all models (~20 lines)
- `tests/core/test_models.py` — Comprehensive model tests (23 tests)

**Key Decisions:**
- TestCase uses @property for lazy file loading with private `_input_text`/`_expected_output` fields
- ProblemState is mutable (frozen=False default) for in-session updates
- SessionConfig.tier_distribution uses default_factory for independent instances

**Tests:** 23 new tests, all passing (50 total)
**Branch:** hive/E1-project-foundation
**Date:** 2026-03-01

# E2-S02: Tier-Based Random Exercise Selection

## Status
Done

## Epic
E2 - Exercise Engine

## Priority
Critical

## Estimate
S

## Description
[PCT] Implement the random selection algorithm that picks 30 exercises from the pool, distributed across 5 difficulty tiers (8 Tier-1, 8 Tier-2, 6 Tier-3, 5 Tier-4, 3 Tier-5). When a tier has fewer exercises than required, select all available and log a warning.

## Acceptance Criteria
- [x] Selects exactly 30 exercises: 8 tier-1, 8 tier-2, 6 tier-3, 5 tier-4, 3 tier-5
- [x] Selection is random within each tier (different results on repeated calls)
- [x] No exercise is repeated within a session
- [x] If a tier has fewer exercises than required, selects all available and logs warning
- [x] Returns exercises ordered by ascending tier (easy first)

## Tasks
- **T1: Implement selection algorithm** — Add select_session(exercise_index: ExerciseIndex, distribution: dict) -> list[Exercise] function. Use random.sample() per tier. Concatenate results in tier order.
- **T2: Write unit tests** — Test: correct distribution counts, no repeats, insufficient tier handling (e.g., tier with 2 exercises when 8 needed), ascending tier ordering. Use seeded random for reproducible tests.

## Technical Notes
- random.sample() for without-replacement selection within each tier
- Default distribution: {1: 8, 2: 8, 3: 6, 4: 5, 5: 3} — stored in SessionConfig
- Consider placing this in core/session_mgr.py or core/loader.py

## Dependencies
- E2-S01 (Exercise Loader) -- provides ExerciseIndex with loaded exercises per tier.

## Implementation Summary

**Files Created/Modified:**
- `src/pytrainer/core/selector.py` — select_session() with random.sample() per tier (~45 lines)
- `tests/core/test_selector.py` — 11 tests covering all 5 AC (distribution, randomness, no repeats, insufficient, ordering)

**Key Decisions:**
- Placed in dedicated `core/selector.py` rather than loader.py for single-responsibility
- Accepts optional distribution dict for flexibility, defaults to {1:8, 2:8, 3:6, 4:5, 5:3}

**Tests:** 11 new tests, all passing
**Branch:** hive/E2-exercise-engine
**Date:** 2026-03-01

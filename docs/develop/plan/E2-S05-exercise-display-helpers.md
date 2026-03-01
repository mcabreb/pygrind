# E2-S05: Exercise Display Data Preparation

## Status
Done

## Epic
E2 - Exercise Engine

## Priority
High

## Estimate
S

## Description
[PCT] Create helper functions that format exercise data for UI consumption: formatted description text, sample I/O extracted from the first test case, and tier badge text with associated color. These helpers bridge the data models and the UI layer.

## Acceptance Criteria
- [x] Provides formatted description text for the problem panel
- [x] Extracts first test case as sample input/output for display
- [x] Returns tier badge text ('Tier 1 — Easy', 'Tier 2 — Basic', etc.) and associated color
- [x] Handles exercises with no test cases gracefully (shows "No sample available")

## Tasks
- **T1: Implement display helpers** — Create helper functions (in core/ or as Exercise methods): get_sample_io(exercise) -> tuple[str, str], get_tier_badge(tier) -> tuple[str, str], format_description(exercise) -> str.
- **T2: Write unit tests** — Test display helpers with fixture exercises. Verify tier badge text/color mapping. Test edge case of exercise with no test cases.

## Technical Notes
- Tier badge colors: T1=green, T2=blue, T3=orange, T4=red, T5=purple (or similar contrast palette)
- Tier names: {1: 'Easy', 2: 'Basic', 3: 'Medium', 4: 'Hard', 5: 'Expert'}
- Sample I/O reads the first test case's .in and .out file contents

## Dependencies
- E2-S01 (Exercise Loader) -- provides loaded Exercise objects with test case data.

## Implementation Summary

**Files Created/Modified:**
- `src/pytrainer/core/display.py` — format_description(), get_sample_io(), get_tier_badge() (~50 lines)
- `tests/core/test_display.py` — 11 tests covering all 4 AC (description, sample I/O, tier badge, no test cases)

**Key Decisions:**
- Standalone functions rather than Exercise methods — keeps models clean, core/ has the logic
- Tier badge format: "Tier N — Name" with em dash per spec

**Tests:** 11 new tests, all passing
**Branch:** hive/E2-exercise-engine
**Date:** 2026-03-01

# E2-S01: Exercise Loader — YAML Discovery & Parsing

## Status
Done

## Epic
E2 - Exercise Engine

## Priority
Critical

## Estimate
M

## Description
[PCT] Implement ExerciseLoader that scans the exercises/ directory tree, parses problem.yaml files with PyYAML, validates required fields (id, title, tier, topic, description, time_estimate), loads test case file paths, and builds an ExerciseIndex grouped by tier. Invalid exercises are skipped with log warnings — the system never crashes on bad data.

## Acceptance Criteria
- [x] Discovers exercises in tier-{1..5}-*/ directories recursively
- [x] Parses problem.yaml using PyYAML and maps to Exercise dataclass
- [x] Validates required fields (id, title, tier, topic, description, time_estimate) — skips invalid with log warning
- [x] Loads test case file paths (tests/*.in, tests/*.out) paired by number
- [x] Returns ExerciseIndex (dict[int, list[Exercise]]) keyed by tier
- [x] Exercises with missing test files are skipped with log warning
- [x] Unit tests cover: valid exercise, missing fields, missing test files, empty directory

## Tasks
- **T1: Implement ExerciseLoader class** — Create core/loader.py with ExerciseLoader(exercises_dir: Path). Implement load_all() that globs tier-*/*/ directories, reads problem.yaml, pairs test case files, and returns ExerciseIndex.
- **T2: Add schema validation** — Validate required fields on each exercise. Log warnings for invalid exercises using Python logging module. Handle yaml.YAMLError gracefully.
- **T3: Write unit tests** — Create tests/core/test_loader.py with parametrized tests: valid exercise loads correctly, missing required field skips, missing test files skips, empty tier directory returns empty list.

## Technical Notes
- Use glob pattern: exercises/tier-*/*/problem.yaml for discovery
- Test case pairing: match NN.in with NN.out files by number prefix
- Fail-soft design: log.warning() for invalid exercises, never raise
- Architecture ref: core/loader.py section 3.2

## Dependencies
- E1-S03 (Define Core Data Models) -- provides Exercise, TestCase, ExerciseIndex types.
- E1-S04 (Create Test Fixtures) -- provides test exercises for unit tests.

## Implementation Summary

**Files Created/Modified:**
- `src/pytrainer/core/loader.py` — ExerciseLoader class with load_all(), _load_exercise(), _load_test_cases() (~80 lines)
- `tests/core/test_loader.py` — 17 tests covering all 7 AC (discovery, parsing, validation, pairing, index, missing files, empty dir)

**Key Decisions:**
- Glob pattern `tier-*/*/problem.yaml` for discovery (flexible tier naming)
- Set intersection for .in/.out pairing — unpaired files silently ignored, exercise skipped if no pairs
- Fail-soft: all errors caught and logged, never raised

**Tests:** 17 new tests, all passing
**Branch:** hive/E2-exercise-engine
**Date:** 2026-03-01

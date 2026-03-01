# E1-S04: Create Test Exercise Fixtures

## Status
Done

## Epic
E1 - Project Foundation & Dev Environment

## Priority
High

## Estimate
S

## Description
[PCT] Create 5 small test exercises (1 per tier) in tests/fixtures/exercises/ for use by all subsequent test suites. Each exercise has a valid problem.yaml and at least 2 test cases. Also create the shared conftest.py with reusable fixtures.

## Acceptance Criteria
- [x] tests/fixtures/exercises/ contains tier-1-easy/ through tier-5-expert/ with 1 exercise each
- [x] Each exercise has a valid problem.yaml with all required fields
- [x] Each exercise has at least 2 test case pairs (01.in/01.out, 02.in/02.out)
- [x] conftest.py provides fixture_exercises_dir fixture returning the fixtures path

## Tasks
- **T1: Create fixture exercises** — Write 5 exercises: tier-1 (print sum of two numbers), tier-2 (reverse a string), tier-3 (find duplicates in list), tier-4 (binary search variant), tier-5 (shortest path in grid). Include problem.yaml with hints and solutions, plus 2-3 test cases each.
- **T2: Create shared conftest.py** — Write tests/conftest.py with fixture_exercises_dir (returns Path to fixtures), sample_exercise (returns a loaded Exercise object), sample_session_config (returns SessionConfig with defaults).

## Technical Notes
- Fixture exercises should be minimal but valid — just enough to test the loader
- Use realistic topics matching the production exercise categories
- conftest.py fixtures will be inherited by all test subdirectories

## Dependencies
- E1-S03 (Define Core Data Models) -- provides Exercise and TestCase dataclasses used by fixtures.

## Implementation Summary

**Files Created/Modified:**
- `tests/fixtures/exercises/tier-1-easy/sum-two-numbers/` — Arithmetic exercise (2 test cases)
- `tests/fixtures/exercises/tier-2-basic/reverse-string/` — String exercise (2 test cases)
- `tests/fixtures/exercises/tier-3-medium/find-duplicates/` — List exercise (2 test cases)
- `tests/fixtures/exercises/tier-4-hard/binary-search/` — Search exercise (2 test cases)
- `tests/fixtures/exercises/tier-5-expert/shortest-path/` — Graph exercise (2 test cases)
- `tests/conftest.py` — Shared fixtures: fixture_exercises_dir, sample_exercise, sample_session_config
- `tests/test_fixtures.py` — Fixture validation tests (12 tests)

**Key Decisions:**
- Exercises cover diverse topics (arithmetic, strings, lists, searching, graphs)
- Each problem.yaml includes hint and solution for downstream testing

**Tests:** 12 new tests, all passing (62 total)
**Branch:** hive/E1-project-foundation
**Date:** 2026-03-01

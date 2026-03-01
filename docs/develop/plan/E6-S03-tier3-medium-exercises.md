# E6-S03: Tier 3 — Medium Exercises

## Status
Done

## Epic
E6 - Starter Exercise Content

## Priority
High

## Estimate
M

## Description
[PCT] Create 4-6 medium exercises involving sorting, searching, recursion, and data structure usage. These require more thought and typically 5-6 minutes to solve.

## Acceptance Criteria
- [x] 4-6 exercises in exercises/tier-3-medium/
- [x] Each has valid problem.yaml with hint and solution
- [x] Each has at least 3 test case pairs including edge cases
- [x] Topics covered: sorting, searching, recursion, data structures

## Tasks
- **T1: Write exercises** — Create: binary search, balanced parentheses checker, merge sorted lists, Caesar cipher encoder/decoder, matrix transposition, anagram grouping.
- **T2: Validate** — Loader validation + solution testing + edge case verification.

## Technical Notes
- IDs: t3-001 through t3-006. Some may use "unordered" validation (e.g., anagram grouping).
- 3+ test cases with edge cases (empty input, single element, large input).

## Dependencies
- E2-S01 (Exercise Loader) -- for format validation.

## Implementation Summary

**Files Created/Modified:**
- `exercises/tier-3-medium/binary-search/` — t3-001: Binary search first occurrence (3 test cases)
- `exercises/tier-3-medium/balanced-parens/` — t3-002: Balanced parentheses checker (4 test cases)
- `exercises/tier-3-medium/merge-sorted/` — t3-003: Merge two sorted lists (3 test cases)
- `exercises/tier-3-medium/caesar-cipher/` — t3-004: Caesar cipher encoder (3 test cases)
- `exercises/tier-3-medium/matrix-transpose/` — t3-005: Matrix transposition (3 test cases)
- `exercises/tier-3-medium/anagram-groups/` — t3-006: Anagram grouping (3 test cases)
- `tests/exercises/test_tier3_medium.py` — 8 tests validating all AC

**Key Decisions:**
- Topics: searching (1), data structures (2), sorting (2), recursion (1) — all 4 required areas covered
- Edge cases: empty inputs, single elements, full rotations, minimal matrices

**Tests:** 8 new tests, all passing
**Branch:** hive/E6-starter-exercises
**Date:** 2026-03-01

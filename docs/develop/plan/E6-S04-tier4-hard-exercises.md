# E6-S04: Tier 4 — Hard Exercises

## Status
Done

## Epic
E6 - Starter Exercise Content

## Priority
High

## Estimate
M

## Description
[PCT] Create 3-5 hard exercises covering dynamic programming, graph traversal, and complex algorithms. These are the differentiators in competition scoring. Solve time: 8-10 minutes.

## Acceptance Criteria
- [x] 3-5 exercises in exercises/tier-4-hard/
- [x] Each has valid problem.yaml with hint and solution
- [x] Each has at least 3 test case pairs including large inputs
- [x] Topics covered: DP, graphs, complex algorithms

## Tasks
- **T1: Write exercises** — Create: longest common subsequence, shortest path BFS, coin change DP, knapsack 0/1, topological sort.
- **T2: Validate** — Loader + solution testing + verify solutions complete within 10s timeout on large inputs.

## Technical Notes
- IDs: t4-001 through t4-005. Solutions must run within 10s even on large test cases.
- Include stress tests with larger input sizes.

## Dependencies
- E2-S01 (Exercise Loader) -- for format validation.

## Implementation Summary

**Files Created/Modified:**
- `exercises/tier-4-hard/longest-common-subseq/` — t4-001: LCS length via 2D DP (5 test cases incl. large)
- `exercises/tier-4-hard/coin-change/` — t4-002: Minimum coins via bottom-up DP (4 test cases incl. large)
- `exercises/tier-4-hard/shortest-path-bfs/` — t4-003: Unweighted shortest path via BFS (4 test cases incl. large)
- `exercises/tier-4-hard/knapsack/` — t4-004: 0/1 knapsack via 1D DP (4 test cases incl. large)
- `exercises/tier-4-hard/topological-sort/` — t4-005: Kahn's algorithm with min-heap (4 test cases incl. large)
- `tests/exercises/test_tier4_hard.py` — 8 tests validating all AC

**Key Decisions:**
- Topics: dp (3), graphs (2) — covers all required areas
- Large input stress tests included for all exercises (500+ elements / 50K nodes)
- All solutions run well under 1s on large inputs (far below 10s limit)
- Topological sort uses min-heap for deterministic output

**Tests:** 8 new tests, all passing
**Branch:** hive/E6-starter-exercises
**Date:** 2026-03-01

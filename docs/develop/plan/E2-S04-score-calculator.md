# E2-S04: Score Calculator

## Status
Done

## Epic
E2 - Exercise Engine

## Priority
Critical

## Estimate
S

## Description
[PCT] Implement the Scorer that calculates points for a solved problem. Base points depend on tier (10/20/35/50/75). Time bonus (+10%) rewards fast solvers. Wrong attempt penalty (-10% each, max -50%) discourages guessing. Viewing the solution in Beginner mode gives 0 points.

## Acceptance Criteria
- [x] Base points: T1=10, T2=20, T3=35, T4=50, T5=75
- [x] Time bonus: +10% if time_spent < (time_estimate_minutes * 60) / 2
- [x] Wrong attempt penalty: -10% per attempt, minimum 50% of base score
- [x] Solution viewed: returns 0 regardless of other factors
- [x] Returns integer score (truncated, not rounded)
- [x] Boundary case tests for all rules (0 attempts, 5 attempts, exact threshold)

## Tasks
- **T1: Implement Scorer class** — Create core/scorer.py with Scorer.calculate(tier, time_spent, time_estimate, attempts, solution_viewed) -> int. Follow scoring formula from architecture doc.
- **T2: Write boundary tests** — tests/core/test_scorer.py: base score per tier, time bonus at exact threshold, 1/2/3/5 wrong attempts, solution viewed overrides all, combined bonus + penalty, max penalty cap at 50%.

## Technical Notes
- Max possible session score: 925 points (8*10 + 8*20 + 6*35 + 5*50 + 3*75)
- Penalty formula: penalty = min(attempts * 0.10, 0.50); score = int(base * (1 - penalty))
- Time bonus applied before penalty: score = int(base * 1.1) then apply penalty
- Pure function — no side effects, no dependencies on Qt

## Dependencies
- E1-S01 (Initialize Project Structure) -- provides the core/ package.

## Implementation Summary

**Files Created/Modified:**
- `src/pytrainer/core/scorer.py` — Scorer.calculate() pure function (~40 lines)
- `tests/core/test_scorer.py` — 22 tests covering all 6 AC (base, bonus, penalty, solution, int, boundary)

**Key Decisions:**
- Time bonus applied first (int(base * 1.1)), then penalty applied to bonused value
- Pure static method — no state, no side effects

**Tests:** 22 new tests, all passing
**Branch:** hive/E2-exercise-engine
**Date:** 2026-03-01

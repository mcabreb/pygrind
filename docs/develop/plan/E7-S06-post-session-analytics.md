# E7-S06: Post-Session Analytics

## Status
To Do

## Epic
E7 - Learning Features & Analytics

## Priority
High

## Estimate
M

## Description
[PCT] Analyze session results and historical data to generate actionable improvement recommendations. Shows topic performance breakdown, tier solve rates, time management analysis, and comparison to previous sessions. Helps users focus their practice where it matters most.

## Acceptance Criteria
- [x] Topic performance: per-topic solve percentage across last N sessions
- [x] Tier performance: solve rate per tier for current session
- [x] Time analysis: average time vs estimate per tier
- [x] Comparison to previous sessions if history exists (score trend)
- [x] Top 3 specific recommendations (e.g., 'Focus on tier-3 dynamic programming')
- [x] Analytics section displayed in ResultsScreen below score summary

## Tasks
- **T1: Implement analytics queries** -- Add analytics methods to Database or create core/analytics.py. Query: per-topic solve rate (GROUP BY topic), per-tier performance, time averages.
- **T2: Implement recommendation engine** -- Rank topics by weakness (lowest solve rate with >=3 data points). Generate 3 text recommendations combining topic + tier suggestions.
- **T3: Integrate with results UI** -- Add collapsible 'Analytics' section to ResultsScreen. Show topic breakdown as a simple table/list, recommendations as bullet points.

## Technical Notes
- Minimum data threshold: only recommend topics with >=3 attempted problems across sessions. Score trend: simple list of last 5 session scores. Keep analytics simple -- no charts in Phase 2 (charts come in Phase 3).

## Dependencies
- E7-S05 (SQLite Persistence) -- provides Database.get_topic_stats() and historical data.

## Implementation Summary

**Files Created/Modified:**
- `src/pytrainer/core/analytics.py` — SessionAnalytics class with tier_performance, time_analysis, topic_performance, score_trend, recommendations (~110 lines)
- `src/pytrainer/ui/results.py` — Added analytics label widget and set_analytics() method (~35 lines added)
- `tests/core/test_analytics.py` — 10 tests covering tier/topic/time analysis, trend, recommendations (new file)
- `tests/ui/test_results_analytics.py` — 4 tests for analytics section in ResultsScreen (new file)

**Key Decisions:**
- SessionAnalytics takes optional Database for historical queries — works without DB for current-session-only analysis
- Recommendations ranked by weakness: lowest solve rate topics first, then weak tiers
- Analytics displayed as styled text in a QLabel — no charts in this phase per ticket notes

**Tests:** 14 new tests, all passing
**Branch:** hive/E7-learning-analytics
**Date:** 2026-03-01

# E3-S01: AST Safety Scanner

## Status
Done

## Epic
E3 - Code Execution Pipeline

## Priority
Critical

## Estimate
M

## Description
[PCT] Implement SafetyScanner using Python's ast.NodeVisitor to detect blocked imports and builtin calls before code execution. This is the first line of defense preventing user code from accessing the filesystem, network, or system operations. Security-critical module requiring comprehensive parametrized tests for every blocked and every allowed construct.

## Acceptance Criteria
- [x] Blocks imports: os, sys, shutil, subprocess, socket, http, urllib, ctypes, signal, pathlib, importlib
- [x] Blocks builtins: eval(), exec(), compile(), __import__(), open()
- [x] Allows: math, string, collections, itertools, functools, heapq, bisect, re, decimal, fractions, statistics, random, copy, operator, typing
- [x] Returns ScanResult(safe=bool, violations=list[str]) with specific violation messages
- [x] Handles both 'import os' and 'from os import path' forms
- [x] Handles aliased imports (import os as o) and nested imports
- [x] Syntax errors in user code return ScanResult with parse error (not a crash)
- [x] Parametrized tests for every blocked and every allowed module

## Tasks
- **T1: Implement SafetyVisitor** — Create core/scanner.py with _SafetyVisitor(ast.NodeVisitor) implementing visit_Import(), visit_ImportFrom(), visit_Call(). Collect violations in a list as strings.
- **T2: Implement SafetyScanner** — SafetyScanner(blocked_imports: set, blocked_builtins: set) with check(code: str) -> ScanResult. Wrap ast.parse() in try/except SyntaxError. Return ScanResult(safe, violations).
- **T3: Write comprehensive tests** — tests/core/test_scanner.py: parametrize over every blocked import (both 'import X' and 'from X import Y'), every blocked builtin, every allowed import. Test aliased imports ('import os as o'), nested imports, syntax errors, empty code. This must be the most thoroughly tested module.

## Technical Notes
- AST visitor pattern: subclass ast.NodeVisitor, override visit_Import, visit_ImportFrom, visit_Call
- For Call nodes: check if func is ast.Name with id in blocked_builtins
- Also check ast.Attribute for things like builtins.open()
- Default blocklists defined as module-level constants BLOCKED_IMPORTS and BLOCKED_BUILTINS
- Architecture ref: section 3.3 Safety Scanner

## Dependencies
- E1-S01 (Initialize Project Structure) -- provides the core/ package directory.

## Implementation Summary

**Files Created/Modified:**
- `src/pytrainer/core/scanner.py` — SafetyScanner, _SafetyVisitor, ScanResult, BLOCKED_IMPORTS, BLOCKED_BUILTINS (~65 lines)
- `tests/core/test_scanner.py` — Comprehensive parametrized tests (83 tests)

**Key Decisions:**
- Used frozenset for blocklists (immutable, O(1) lookup)
- Top-level module extraction via `.split(".")[0]` handles submodule imports (e.g. `http.server`)
- `ast.Attribute` check catches `builtins.open()` pattern

**Tests:** 83 new tests, all passing
**Branch:** hive/E3-execution-pipeline
**Date:** 2026-03-01

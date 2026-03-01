"""Comprehensive tests for AST Safety Scanner."""

import pytest

from pytrainer.core.scanner import (
    BLOCKED_BUILTINS,
    BLOCKED_IMPORTS,
    SafetyScanner,
    ScanResult,
)


@pytest.fixture
def scanner():
    """Return a SafetyScanner with default blocklists."""
    return SafetyScanner()


# --- ScanResult dataclass ---


class TestScanResult:
    def test_safe_result(self):
        r = ScanResult(safe=True, violations=[])
        assert r.safe is True
        assert r.violations == []

    def test_unsafe_result(self):
        r = ScanResult(safe=False, violations=["import os"])
        assert r.safe is False
        assert r.violations == ["import os"]


# --- Blocked imports ---

BLOCKED_IMPORT_LIST = [
    "os",
    "sys",
    "shutil",
    "subprocess",
    "socket",
    "http",
    "urllib",
    "ctypes",
    "signal",
    "pathlib",
    "importlib",
]


class TestBlockedImports:
    @pytest.mark.parametrize("module", BLOCKED_IMPORT_LIST)
    def test_blocks_import_statement(self, scanner, module):
        result = scanner.check(f"import {module}")
        assert result.safe is False
        assert len(result.violations) >= 1

    @pytest.mark.parametrize("module", BLOCKED_IMPORT_LIST)
    def test_blocks_from_import(self, scanner, module):
        result = scanner.check(f"from {module} import something")
        assert result.safe is False
        assert len(result.violations) >= 1

    @pytest.mark.parametrize("module", BLOCKED_IMPORT_LIST)
    def test_blocks_aliased_import(self, scanner, module):
        result = scanner.check(f"import {module} as m")
        assert result.safe is False
        assert len(result.violations) >= 1

    def test_blocks_multi_import(self, scanner):
        result = scanner.check("import os, sys")
        assert result.safe is False
        assert len(result.violations) >= 2

    def test_blocks_nested_from_import(self, scanner):
        result = scanner.check("from os.path import join")
        assert result.safe is False
        assert len(result.violations) >= 1

    def test_blocks_submodule_import(self, scanner):
        result = scanner.check("import http.server")
        assert result.safe is False
        assert len(result.violations) >= 1


# --- Blocked builtins ---

BLOCKED_BUILTIN_LIST = ["eval", "exec", "compile", "__import__", "open"]


class TestBlockedBuiltins:
    @pytest.mark.parametrize("builtin", BLOCKED_BUILTIN_LIST)
    def test_blocks_builtin_call(self, scanner, builtin):
        result = scanner.check(f"{builtin}('test')")
        assert result.safe is False
        assert len(result.violations) >= 1

    def test_blocks_builtins_dot_open(self, scanner):
        result = scanner.check("builtins.open('file')")
        assert result.safe is False
        assert len(result.violations) >= 1


# --- Allowed imports ---

ALLOWED_IMPORT_LIST = [
    "math",
    "string",
    "collections",
    "itertools",
    "functools",
    "heapq",
    "bisect",
    "re",
    "decimal",
    "fractions",
    "statistics",
    "random",
    "copy",
    "operator",
    "typing",
]


class TestAllowedImports:
    @pytest.mark.parametrize("module", ALLOWED_IMPORT_LIST)
    def test_allows_safe_import(self, scanner, module):
        result = scanner.check(f"import {module}")
        assert result.safe is True
        assert result.violations == []

    @pytest.mark.parametrize("module", ALLOWED_IMPORT_LIST)
    def test_allows_safe_from_import(self, scanner, module):
        result = scanner.check(f"from {module} import something")
        assert result.safe is True
        assert result.violations == []


# --- Edge cases ---


class TestEdgeCases:
    def test_empty_code(self, scanner):
        result = scanner.check("")
        assert result.safe is True
        assert result.violations == []

    def test_syntax_error_returns_scan_result(self, scanner):
        result = scanner.check("def foo(")
        assert result.safe is False
        assert len(result.violations) == 1
        assert "syntax" in result.violations[0].lower() or "parse" in result.violations[0].lower()

    def test_plain_code_is_safe(self, scanner):
        code = "x = 1 + 2\nprint(x)\nfor i in range(10):\n    print(i)"
        result = scanner.check(code)
        assert result.safe is True

    def test_mixed_safe_and_unsafe(self, scanner):
        code = "import math\nimport os\nprint('hello')"
        result = scanner.check(code)
        assert result.safe is False
        assert len(result.violations) >= 1

    def test_allowed_builtin_calls(self, scanner):
        code = "print('hello')\nlen([1,2,3])\nrange(10)"
        result = scanner.check(code)
        assert result.safe is True

    def test_custom_blocklists(self):
        s = SafetyScanner(blocked_imports={"json"}, blocked_builtins={"print"})
        assert s.check("import json").safe is False
        assert s.check("print('hi')").safe is False
        assert s.check("import os").safe is True  # not in custom blocklist

    def test_violation_messages_are_descriptive(self, scanner):
        result = scanner.check("import os")
        assert result.violations[0]  # non-empty string
        assert "os" in result.violations[0]


# --- Constants ---


class TestConstants:
    def test_blocked_imports_contains_required(self):
        for mod in BLOCKED_IMPORT_LIST:
            assert mod in BLOCKED_IMPORTS

    def test_blocked_builtins_contains_required(self):
        for b in BLOCKED_BUILTIN_LIST:
            assert b in BLOCKED_BUILTINS

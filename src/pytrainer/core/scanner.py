"""AST Safety Scanner — blocks dangerous imports and builtins before code execution."""

import ast
from dataclasses import dataclass, field

BLOCKED_IMPORTS: frozenset[str] = frozenset(
    {
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
    }
)

BLOCKED_BUILTINS: frozenset[str] = frozenset(
    {
        "eval",
        "exec",
        "compile",
        "__import__",
        "open",
    }
)


@dataclass
class ScanResult:
    """Result of a safety scan."""

    safe: bool
    violations: list[str] = field(default_factory=list)


class _SafetyVisitor(ast.NodeVisitor):
    """AST visitor that collects safety violations."""

    def __init__(self, blocked_imports: frozenset[str], blocked_builtins: frozenset[str]):
        self.blocked_imports = blocked_imports
        self.blocked_builtins = blocked_builtins
        self.violations: list[str] = []

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            top_module = alias.name.split(".")[0]
            if top_module in self.blocked_imports:
                self.violations.append(f"Blocked import: {alias.name}")
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module:
            top_module = node.module.split(".")[0]
            if top_module in self.blocked_imports:
                self.violations.append(f"Blocked import: from {node.module}")
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        if isinstance(node.func, ast.Name):
            if node.func.id in self.blocked_builtins:
                self.violations.append(f"Blocked builtin: {node.func.id}()")
        elif isinstance(node.func, ast.Attribute) and node.func.attr in self.blocked_builtins:
            self.violations.append(f"Blocked builtin: {node.func.attr}()")
        self.generic_visit(node)


class SafetyScanner:
    """Scans user code for dangerous constructs using AST analysis."""

    def __init__(
        self,
        blocked_imports: frozenset[str] | set[str] | None = None,
        blocked_builtins: frozenset[str] | set[str] | None = None,
    ):
        self._blocked_imports = frozenset(blocked_imports) if blocked_imports else BLOCKED_IMPORTS
        self._blocked_builtins = (
            frozenset(blocked_builtins) if blocked_builtins else BLOCKED_BUILTINS
        )

    def check(self, code: str) -> ScanResult:
        """Scan code and return a ScanResult."""
        if not code.strip():
            return ScanResult(safe=True)

        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return ScanResult(safe=False, violations=[f"Syntax error: {e}"])

        visitor = _SafetyVisitor(self._blocked_imports, self._blocked_builtins)
        visitor.visit(tree)

        if visitor.violations:
            return ScanResult(safe=False, violations=visitor.violations)
        return ScanResult(safe=True)

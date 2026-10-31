"""Static pre-filter for candidate code. Cheap rejection of obvious escapes, not a security
boundary: isolation comes from the sandbox profile."""

from __future__ import annotations

import ast

FORBIDDEN_CALLS = {"open", "exec", "eval", "compile", "__import__", "input", "breakpoint",
                   "globals", "locals", "vars"}
FORBIDDEN_ATTRS = {"__dict__", "__globals__", "__builtins__", "__subclasses__", "__code__",
                   "__closure__", "f_globals", "f_locals"}


def scan(code: str, allowed_imports: list[str]) -> list[str]:
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return [f"syntax error: {e}"]
    allowed = set(allowed_imports) | {"a2m_task"}
    problems = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            names = [node.module or ""] if node.level == 0 else ["<relative>"]
        else:
            names = []
        for name in names:
            if name.split(".")[0] not in allowed:
                problems.append(f"import not allowed: {name}")
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id in FORBIDDEN_CALLS):
            problems.append(f"call not allowed: {node.func.id}()")
        if isinstance(node, ast.Attribute) and node.attr in FORBIDDEN_ATTRS:
            problems.append(f"attribute not allowed: {node.attr}")
    return sorted(set(problems))

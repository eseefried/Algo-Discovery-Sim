"""Static guardrails only. These are NOT an execution security boundary."""

import ast

ALLOWED_IMPORTS = {
    "__future__",
    "math",
    "numpy",
    "qiskit",
    "qiskit.circuit",
    "qiskit.circuit.library",
}
FORBIDDEN_NAMES = {
    "eval",
    "exec",
    "compile",
    "open",
    "__import__",
    "getattr",
    "setattr",
    "delattr",
    "globals",
    "locals",
    "vars",
    "input",
    "help",
    "breakpoint",
    "print",
    "exit",
    "quit",
    "Operator",
    "Statevector",
    "DensityMatrix",
    "UnitaryGate",
    "Isometry",
    "StatePreparation",
}
FORBIDDEN_ATTRIBUTES = {
    "unitary",
    "initialize",
    "reset",
    "measure",
    "measure_all",
    "tofile",
    "dump",
    "dumps",
    "save",
    "load",
    "savetxt",
    "savez",
    "savez_compressed",
    "loadtxt",
    "fromfile",
    "memmap",
    "draw",
    "qasm",
    "to_matrix",
    "synth_unitary",
    "setflags",
    "ctypes",
}


def check_constant_expression(expression: ast.expr) -> None:
    try:
        ast.literal_eval(expression)
        return
    except (ValueError, TypeError):
        pass
    # Accept small numeric expressions such as 2 ** 20 without evaluating them here.
    nodes = list(ast.walk(expression))
    allowed = (
        ast.Constant,
        ast.BinOp,
        ast.UnaryOp,
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.FloorDiv,
        ast.Mod,
        ast.Pow,
        ast.USub,
        ast.UAdd,
    )
    if len(nodes) > 32 or any(not isinstance(node, allowed) for node in nodes):
        raise ValueError("Module constants must be literals or small numeric expressions.")
    if any(
        isinstance(node, ast.Constant)
        and (type(node.value) not in {int, float} or abs(node.value) > 2**32)
        for node in nodes
    ):
        raise ValueError("Numeric constant exceeds the static limit.")
    for node in nodes:
        if (
            isinstance(node, ast.BinOp)
            and isinstance(node.op, ast.Pow)
            and (not isinstance(node.right, ast.Constant) or not 0 <= node.right.value <= 64)
        ):
            raise ValueError("Constant exponents must be small nonnegative numbers.")


def check_source(source: str) -> None:
    tree = ast.parse(source)
    compile(tree, "<generated-circuit>", "exec")  # Compiles without executing.
    functions = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            functions.append(node)
            if node.decorator_list or node.args.defaults or any(node.args.kw_defaults):
                raise ValueError("Decorators and default arguments are not allowed.")
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            pass
        elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant):
            if not isinstance(node.value.value, str):
                raise TypeError("Only docstring expressions are allowed at module level.")
        elif isinstance(node, ast.Assign):
            check_constant_expression(node.value)
            if any(not isinstance(target, ast.Name) for target in node.targets):
                raise ValueError("Module constants must use simple variable names.")
        else:
            raise TypeError("Module-level executable statements are not allowed.")
    builders = [f for f in functions if f.name == "build_circuit"]
    if len(builders) != 1:
        raise ValueError("Source must define exactly one build_circuit(instance) function.")
    args = builders[0].args
    if len(args.posonlyargs) + len(args.args) != 1 or args.vararg or args.kwarg or args.kwonlyargs:
        raise ValueError("build_circuit must accept exactly one instance argument.")
    top_level = {id(node) for node in tree.body}
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            if id(node) not in top_level:
                raise ValueError("Runtime imports are not allowed.")
            modules = (
                [a.name for a in node.names] if isinstance(node, ast.Import) else [node.module]
            )
            if any(module not in ALLOWED_IMPORTS for module in modules):
                raise ValueError("Source imports a module outside the permitted Qiskit API.")
            if isinstance(node, ast.ImportFrom) and (
                node.level or any(a.name == "*" for a in node.names)
            ):
                raise ValueError("Relative and wildcard imports are not allowed.")
            if any(alias.name in FORBIDDEN_NAMES for alias in node.names):
                raise ValueError("Source imports a prohibited operation.")
        if isinstance(node, ast.Name) and (node.id in FORBIDDEN_NAMES or node.id.startswith("__")):
            raise ValueError("Source contains a prohibited name.")
        if isinstance(node, ast.Attribute) and (
            node.attr.startswith("_")
            or node.attr in FORBIDDEN_ATTRIBUTES
            or node.attr in FORBIDDEN_NAMES
        ):
            raise ValueError("Source contains a prohibited operation or private attribute.")
        if isinstance(node, (ast.ClassDef, ast.AsyncFunctionDef)):
            raise TypeError("Classes and async definitions are not allowed.")

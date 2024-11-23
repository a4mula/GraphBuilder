import os
import ast
import networkx as nx


def get_function_metrics(function_node):
    """Analyze a function and return its metrics."""
    # Line count: Count the lines of code in the function
    line_count = function_node.end_lineno - function_node.lineno + 1

    # Argument count: Number of arguments
    arg_count = len(function_node.args.args)

    # Cyclomatic complexity: Number of branching statements
    cyclomatic_complexity = sum(
        isinstance(node, (ast.If, ast.For, ast.While, ast.Try, ast.With))
        for node in ast.walk(function_node)
    )

    # Docstring presence: Check if the first body element is a docstring
    has_docstring = (
        isinstance(function_node.body[0], ast.Expr)
        and isinstance(function_node.body[0].value, ast.Str)
    )

    # Nesting depth: Calculate the max depth of nested blocks
    def max_depth(node, depth=0):
        if not isinstance(
            node, (ast.FunctionDef, ast.If, ast.For, ast.While, ast.Try, ast.With)
        ):
            return depth
        return max(
            (max_depth(child, depth + 1) for child in ast.iter_child_nodes(node)),
            default=depth,
        )

    nesting_depth = max_depth(function_node)

    return {
        "line_count": line_count,
        "arg_count": arg_count,
        "cyclomatic_complexity": cyclomatic_complexity,
        "has_docstring": has_docstring,
        "nesting_depth": nesting_depth,
    }


def extract_functions_from_file(file_path):
    """Extract all function names and metrics from a Python file."""
    with open(file_path, "r") as file:
        try:
            tree = ast.parse(file.read(), filename=file_path)
        except SyntaxError as e:
            print(f"SyntaxError in {file_path}: {e}")
            return {}

    functions = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            metrics = get_function_metrics(node)
            functions[node.name] = metrics
    return functions


def find_modules_and_functions(project_root):
    """Walk the project directory and extract all modules and their functions."""
    project_structure = {}
    for root, _, files in os.walk(project_root):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                module_name = (
                    os.path.relpath(file_path, project_root)
                    .replace(os.sep, ".")
                    .removesuffix(".py")
                )
                functions = extract_functions_from_file(file_path)
                project_structure[module_name] = functions
    return project_structure


def display_project_structure(project_structure):
    """Print the project structure with metrics in a readable format."""
    for module, functions in project_structure.items():
        print(f"{module}:")
        if functions:
            for func, metrics in functions.items():
                print(f"  - {func}:")
                print(f"      Lines: {metrics['line_count']}")
                print(f"      Args: {metrics['arg_count']}")
                print(f"      Cyclomatic Complexity: {metrics['cyclomatic_complexity']}")
                print(f"      Has Docstring: {'Yes' if metrics['has_docstring'] else 'No'}")
                print(f"      Nesting Depth: {metrics['nesting_depth']}")
        else:
            print("    (No functions found)")


def find_function_calls(module_path, functions=None):
    """
    Analyze the AST of a module to identify function calls and relationships.
    """
    with open(module_path, "r") as f:
        tree = ast.parse(f.read())

    relationships = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            source_function = node.name
            for child in ast.walk(node):
                if isinstance(child, ast.Call):
                    # Detect the called function
                    if isinstance(child.func, ast.Name):
                        target_function = child.func.id
                        # Intra-module call
                        relationships.append(
                            {
                                "from": source_function,
                                "to": target_function,
                                "frequency": 1,  # Increment frequency (you can refine this)
                            }
                        )
                    elif isinstance(child.func, ast.Attribute):
                        # Handle inter-module calls (e.g., module.function)
                        if isinstance(child.func.value, ast.Name):
                            module_name = child.func.value.id
                            function_name = child.func.attr
                            relationships.append(
                                {
                                    "from": source_function,
                                    "to": f"{module_name}.{function_name}",
                                    "frequency": 1,
                                }
                            )
    return relationships


def build_graph_from_relationships(relationships):
    """
    Build a graph from function call relationships.
    """
    G = nx.DiGraph()
    for rel in relationships:
        source = rel["from"]
        target = rel["to"]
        frequency = rel["frequency"]
        amplitude = rel.get("amplitude", 1)  # Default to 1 if not provided
        weight = frequency * amplitude
        G.add_edge(source, target, weight=weight)
    return G


if __name__ == "__main__":
    project_root = "src"  # Adjust to your project's root directory
    project_structure = find_modules_and_functions(project_root)
    display_project_structure(project_structure)


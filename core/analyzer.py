"""
===============================================================================
Project: LegacyLift
File: analyzer.py

Author: Samuel Raymond Kwibe
Education: B.S. Computer Science Student, Southern New Hampshire University (SNHU)

Professional Focus:
- Software Engineering
- Artificial Intelligence (AI)
- Cloud Engineering
- Full-Stack Development

LinkedIn:
https://www.linkedin.com/in/samuel-kwibe-371633249/

GitHub:
https://github.com/Samkwibe

Description:
Static code analyzer that detects basic code smells and bad practices.

Copyright © 2026 Samuel Raymond Kwibe.
All Rights Reserved.
===============================================================================
"""
import ast

def analyze_code(source_code):
    """Analyzes the given Python source code for code smells.
    
    Args:
        source_code: The Python source code as a string.
        
    Returns:
        A list of dictionaries representing code smells.
    """
    smells = []
    
    try:
        tree = ast.parse(source_code)
    except SyntaxError as e:
        return [{"type": "err", "message": f"SyntaxError: {e.msg} at line {e.lineno}"}]

    # Walk the AST
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Check docstring
            if not ast.get_docstring(node):
                smells.append({
                    "type": "err",
                    "message": f"Missing docstring — function `{node.name}` has no documentation",
                    "line": node.lineno
                })
            
            # Check function length
            # Note: node.end_lineno is available in Python 3.8+
            if hasattr(node, "end_lineno") and node.end_lineno and node.lineno:
                length = node.end_lineno - node.lineno
                if length > 30:
                    smells.append({
                        "type": "warn",
                        "message": f"Long function — `{node.name}` is {length} lines long (max 30)",
                        "line": node.lineno
                    })
            
            # Check parameters
            if len(node.args.args) > 5:
                smells.append({
                    "type": "warn",
                    "message": f"Too many parameters — function `{node.name}` has {len(node.args.args)} parameters (max 5)",
                    "line": node.lineno
                })
                
            # Check type hints
            has_unannotated_args = any(arg.annotation is None for arg in node.args.args if arg.arg != 'self')
            if has_unannotated_args or node.returns is None:
                smells.append({
                    "type": "info",
                    "message": f"No type hints — parameters or return type in `{node.name}` are unannotated",
                    "line": node.lineno
                })

        # Deep nesting check
        if isinstance(node, (ast.If, ast.For, ast.While)):
            # Helper to calculate max depth
            def get_depth(n, current_depth=1):
                max_depth = current_depth
                for child in ast.iter_child_nodes(n):
                    if isinstance(child, (ast.If, ast.For, ast.While, ast.With)):
                        max_depth = max(max_depth, get_depth(child, current_depth + 1))
                    else:
                        max_depth = max(max_depth, get_depth(child, current_depth))
                return max_depth
            
            # We only check from the top-level block statements within a function
            # To avoid double counting, we'll implement a simpler visitor pattern below
            pass

    # A better way to check deep nesting is by keeping track of the current depth
    class NestingVisitor(ast.NodeVisitor):
        def __init__(self):
            self.current_depth = 0
            self.max_depth_recorded = {}
            
        def generic_visit(self, node):
            is_block = isinstance(node, (ast.If, ast.For, ast.While, ast.With))
            if is_block:
                self.current_depth += 1
                
            if self.current_depth > 2:
                # Use the line number of the block that pushes it over the edge
                line = getattr(node, 'lineno', None)
                if line and line not in self.max_depth_recorded:
                    self.max_depth_recorded[line] = self.current_depth

            super().generic_visit(node)
            
            if is_block:
                self.current_depth -= 1

    visitor = NestingVisitor()
    visitor.visit(tree)
    
    # We only report once per deep nest to avoid spam
    if visitor.max_depth_recorded:
        max_d = max(visitor.max_depth_recorded.values())
        line = [k for k, v in visitor.max_depth_recorded.items() if v == max_d][0]
        smells.append({
            "type": "warn",
            "message": f"Deep nesting — {max_d} levels of nested blocks detected",
            "line": line
        })

    # Variable name check (1 char names, except 'i', 'j', 'x', 'y' commonly used in loops, but PRD complains about 'd', 'x', 'r')
    # Let's catch any 1 char names except loop indices maybe, or just any to match the PRD
    class NameVisitor(ast.NodeVisitor):
        def __init__(self):
            self.short_names = set()
            
        def visit_Name(self, node):
            if isinstance(node.ctx, ast.Store) and len(node.id) == 1:
                self.short_names.add(node.id)
            self.generic_visit(node)
            
    name_visitor = NameVisitor()
    name_visitor.visit(tree)
    
    if name_visitor.short_names:
        names_str = ", ".join(f"`{n}`" for n in sorted(name_visitor.short_names))
        smells.append({
            "type": "warn",
            "message": f"Unclear names — variables {names_str} are not descriptive"
        })

    # Magic number check (numbers used in operations/comparisons directly)
    class MagicNumberVisitor(ast.NodeVisitor):
        def __init__(self):
            self.magic_numbers = set()
            
        def visit_Constant(self, node):
            if isinstance(node.value, (int, float)):
                if node.value not in [0, 1, -1]: # Ignore common constants
                    self.magic_numbers.add(node.value)
            self.generic_visit(node)
            
    magic_visitor = MagicNumberVisitor()
    magic_visitor.visit(tree)
    
    if magic_visitor.magic_numbers:
        nums_str = ", ".join(f"`{n}`" for n in sorted(magic_visitor.magic_numbers))
        smells.append({
            "type": "warn",
            "message": f"Magic number — {nums_str} used directly, should be a named constant"
        })

    return smells

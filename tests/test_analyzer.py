"""
===============================================================================
Project: LegacyLift
File: test_analyzer.py

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
Unit tests to verify the functionality of the static code analyzer.

Copyright © 2026 Samuel Raymond Kwibe.
All Rights Reserved.
===============================================================================
"""
import pytest
from core.analyzer import analyze_code

def test_missing_docstring():
    code = "def foo(): pass"
    smells = analyze_code(code)
    assert any(s["type"] == "err" and "Missing docstring" in s["message"] for s in smells)

def test_long_function():
    # Construct a function longer than 30 lines
    code = "def foo():\n" + "\n".join(f"    x = {i}" for i in range(35))
    smells = analyze_code(code)
    assert any(s["type"] == "warn" and "Long function" in s["message"] for s in smells)

def test_too_many_parameters():
    code = "def foo(a, b, c, d, e, f): pass"
    smells = analyze_code(code)
    assert any(s["type"] == "warn" and "Too many parameters" in s["message"] for s in smells)

def test_deep_nesting():
    code = """
def foo():
    if True:
        for i in range(10):
            while True:
                pass
"""
    smells = analyze_code(code)
    assert any(s["type"] == "warn" and "Deep nesting" in s["message"] for s in smells)

def test_magic_numbers():
    code = """
def foo():
    return 2.5 * 10
"""
    smells = analyze_code(code)
    assert any(s["type"] == "warn" and "Magic number" in s["message"] for s in smells)

def test_unclear_names():
    code = """
def foo():
    x = 10
    d = 5
    return x * d
"""
    smells = analyze_code(code)
    assert any(s["type"] == "warn" and "Unclear names" in s["message"] for s in smells)

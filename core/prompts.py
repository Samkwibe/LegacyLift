"""
===============================================================================
Project: LegacyLift
File: prompts.py

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
Stores all the LLM prompt templates used throughout the application.

Copyright © 2026 Samuel Raymond Kwibe.
All Rights Reserved.
===============================================================================
"""
"""
Prompt templates for LegacyLift LLM interactions.
"""

REFACTOR_PROMPT = """You are an expert software engineer and clean code advocate. Your task is to refactor the provided {language} code to make it clean, readable, and maintainable.

Apply the following clean code principles:
1. Use descriptive and meaningful variable/function names.
2. Resolve deep nesting by extracting helper functions or using early returns (guard clauses).
3. Add appropriate type hints.
4. Replace magic numbers with named constants.
5. Ensure functions do only one thing (Single Responsibility Principle).
6. Do not remove any core business logic; the refactored code must behave exactly identically to the original.

Output format:
You MUST respond using the following XML structure. Do not include any explanations outside of these tags.

<refactored_code>
[Insert the fully refactored code here]
</refactored_code>

<changelog>
- [Summarize the first major change]
- [Summarize the second major change]
</changelog>

Source Code:
{source_code}
"""

DOCS_PROMPT = """You are a senior technical writer and software engineer.
I will provide you with a refactored {language} code snippet. 
Your goal is to generate documentation for this code.

Please provide your output exactly within these three XML tags:
1. <documented_code> 
   The exact same refactored code, but with professional docstrings (e.g. Google-style for Python, JSDoc for JS) added to every function and class. 
2. <readme_section>
   A high-level markdown overview of what the module does, its inputs/outputs, and how to use it.
3. <openapi_schema>
   If the code contains REST API endpoints (like Flask, FastAPI, Express), generate a valid OpenAPI 3.0 YAML schema for it. If there are no endpoints, just output "N/A".

Here is the refactored code:
<refactored_code>
{refactored_code}
</refactored_code>
"""

NVIDIA_EXPLANATION_PROMPT = """You are an expert Senior Code Reviewer.
I will provide you with two code snippets: the Original Spaghetti Code, and the Refactored Clean Code.

Your task is to review the ORIGINAL code and explain what was wrong with it.
Specifically, identify:
- Bugs and missing logic
- Bad practices and anti-patterns
- Security vulnerabilities
- Performance problems

Provide your feedback in a clear, concise Markdown format under a "Code Review Feedback" heading. Use bullet points for readability. Do not provide a changelog, just focus on the flaws in the original code.

Original Code:
<original>
{source_code}
</original>

Refactored Code:
<refactored>
{refactored_code}
</refactored>
"""

TEST_PROMPT = """You are an expert QA automation engineer.
I will provide you with a refactored {language} code snippet.

Your task is to write a comprehensive suite of Unit Tests for this code.
- If the language is Python, use the `pytest` framework.
- If the language is JavaScript, use the `jest` framework.

Identify edge cases, happy paths, and error states. 
Provide the complete test file code exactly within these XML tags:
<unit_tests>
[YOUR TEST CODE HERE]
</unit_tests>

Here is the refactored code to test:
<refactored_code>
{refactored_code}
</refactored_code>
"""

PROJECT_WALKTHROUGH_PROMPT = """You are an expert Senior Software Engineer and Mentor.
I am providing you with the entire source code of a project.

Your task is to analyze the entire project and generate a comprehensive, beginner-friendly "Project Walkthrough". 
Explain concepts in plain English, using examples where necessary. You must output a detailed Markdown report containing EXACTLY the following sections:

## 1. Project Overview
Explain what the project is, its main goal, and what it does from a user's perspective.

## 2. Architecture Overview
Explain the high-level architecture (Frontend, Backend, APIs, etc.). Generate a text-based visual project map or dependency diagram (using Markdown or Mermaid).

## 3. Folder Structure Explanation
List the key directories and files and explain their purpose.

## 4. File-by-File Explanation
Briefly explain the role of each file provided in the context. Describe the classes, functions, and components within them.

## 5. Data Flow & Entry Points
Explain the flow of data from user input to final output. Identify key startup files (e.g., app.py) and entry points.

## 6. Database & APIs
If applicable, explain the database models, API endpoints, services, and business logic. If not applicable, explain how data is managed in memory or state.

## 7. Security & Performance Analysis
Provide a security analysis and performance analysis of the codebase.

## 8. Learning Mode: Deep Mentorship
As a senior mentor, explain:
- **Why** the code was written this way.
- **Alternative approaches** that could have been used.
- **Best practices** that were implemented.
- **Common mistakes** to avoid when building something like this.
- **Difficulties and Problems**: Carefully analyze the codebase and explain the specific difficulties, problems, and architectural challenges the developer likely faced while building this project. Help the developer learn from these challenges to become more advanced.

Here is the entire codebase:
<codebase>
{codebase_content}
</codebase>
"""

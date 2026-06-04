"""
===============================================================================
Project: LegacyLift
File: project_analyzer.py

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
Scans local codebases to generate comprehensive project walkthroughs.

Copyright © 2026 Samuel Raymond Kwibe.
All Rights Reserved.
===============================================================================
"""
import os
import time
import requests
from anthropic import Anthropic
from core.prompts import PROJECT_WALKTHROUGH_PROMPT
from core.gemini_client import call_gemini

def scan_local_codebase(directory="."):
    """Scans the local directory and aggregates all relevant code files into a single string."""
    ignore_dirs = {".git", "venv", "__pycache__", ".vscode", "node_modules", "tests", "build", "dist"}
    ignore_exts = {".pyc", ".png", ".jpg", ".jpeg", ".ico", ".svg", ".zip", ".tar", ".gz", ".sqlite3"}
    
    codebase_content = []
    
    for root, dirs, files in os.walk(directory):
        # Modify dirs in-place to prevent os.walk from traversing ignored directories
        dirs[:] = [d for d in dirs if d not in ignore_dirs and not d.startswith('.')]
        
        for file in files:
            # Ignore environment variables, hidden files, and lock files
            if file.startswith('.') or file == ".env" or file == "package-lock.json":
                continue
            
            ext = os.path.splitext(file)[1].lower()
            if ext in ignore_exts:
                continue
                
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    codebase_content.append(f"--- FILE: {filepath} ---\n{content}\n")
            except Exception:
                pass # Skip files that cannot be read as utf-8 (e.g. binaries)
                
    return "\n".join(codebase_content)

def generate_project_walkthrough(codebase_content, provider= "Claude (Anthropic)"):
    """Sends the codebase string to the LLM to generate the Walkthrough report."""
    if "Mock" in provider:
        time.sleep(2)
        return """## 1. Project Overview
This is a mock project walkthrough for testing the UI!

## 2. Architecture Overview
```mermaid
graph TD;
    A[app.py] --> B[core/analyzer.py];
    A --> C[core/project_analyzer.py];
```

## 8. Learning Mode: Deep Mentorship
**Difficulties and Problems**: 
Building a tool that wraps LLMs means dealing with context window limits, prompt engineering complexities, and handling unexpected outputs. You likely struggled with creating dynamic UI states in Streamlit to accommodate a multi-step pipeline!
"""

    prompt = PROJECT_WALKTHROUGH_PROMPT.format(codebase_content=codebase_content)

    if "Claude" in provider:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("Anthropic API Key is not set in environment.")
        client = Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=4000,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    elif "Gemini" in provider:
        return call_gemini(prompt)
    else:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API Key is not set in environment.")
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        data = {
            "model": "gpt-4o",
            "messages": [
                {"role": "system", "content": "You are a Senior Software Engineer and Mentor."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3
        }
        resp = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
        if resp.status_code != 200:
            raise Exception(f"OpenAI API Error: {resp.text}")
        return resp.json()["choices"][0]["message"]["content"]

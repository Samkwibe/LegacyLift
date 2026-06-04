"""
===============================================================================
Project: LegacyLift
File: security.py

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
LLM logic for hunting security vulnerabilities (OWASP Top 10) in code.

Copyright © 2026 Samuel Raymond Kwibe.
All Rights Reserved.
===============================================================================
"""
import time
from core.refactor import call_gemini
import requests
import os

SECURITY_PROMPT = """You are a Principal Application Security Engineer.
Your task is to review the following codebase and find security vulnerabilities.
Focus ONLY on security issues (SQL Injection, XSS, insecure cryptography, hardcoded secrets, etc.).
Do not complain about code style or performance unless it poses a security risk.

Provide your output in a clear Markdown format. Include:
1. A summary of the security posture.
2. A table of vulnerabilities with columns: [Severity, Vulnerability Type, File/Line, Description, Remediation].
3. Specific code snippets showing how to fix the critical issues.

Code to review:
{code}
"""

def run_security_audit(source_code, provider="Gemini 3.5 Flash (Google) - FREE"):
    """Runs a dedicated security audit on the code."""
    if "Mock" in provider:
        time.sleep(2)
        return """# 🛡️ Security Audit Report
        
## Summary
The code appears mostly secure, but there are some critical issues regarding hardcoded secrets.

## Vulnerabilities
| Severity | Type | File/Line | Description | Remediation |
|---|---|---|---|---|
| **CRITICAL** | Hardcoded Secret | `db_connect.py:12` | Database password hardcoded in plaintext. | Use environment variables (e.g., `os.getenv`). |
| **MEDIUM** | SQL Injection | `app.py:45` | String interpolation used in SQL query. | Use parameterized queries. |
"""

    prompt = SECURITY_PROMPT.format(code=source_code)
    
    if "Gemini" in provider:
        return call_gemini(prompt)
    elif "Claude" in provider:
        from anthropic import Anthropic
        client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=4000,
            temperature=0.2,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
    elif "OpenAI" in provider:
        headers = {
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-4o",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2
        }
        resp = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
        if resp.status_code == 200:
            return resp.json()["choices"][0]["message"]["content"]
        else:
            raise Exception(f"OpenAI API Error: {resp.text}")
    
    return "Error: Unknown provider selected."

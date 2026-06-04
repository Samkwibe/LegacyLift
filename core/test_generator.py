"""
===============================================================================
Project: LegacyLift
File: test_generator.py

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
Generates AI-powered unit tests for refactored code.

Copyright © 2026 Samuel Raymond Kwibe.
All Rights Reserved.
===============================================================================
"""
import re
import os
import time
import requests
from anthropic import Anthropic
from core.prompts import TEST_PROMPT
from core.gemini_client import call_gemini
from core.nvidia_client import call_nvidia

def generate_tests(refactored_code, language= "Python", provider= "Claude (Anthropic)"):
    """Generates unit tests based on the refactored code.
    
    Args:
        refactored_code: The cleaned code from Step 2.
        language: The programming language (Python or JavaScript).
        provider: The LLM provider.
        
    Returns:
        A string containing the generated unit test code.
    """
    if "Mock" in provider:
        time.sleep(2)
        if language == "Python":
            mock_tests = """import pytest
from module import proc

def test_proc_active_and_above_threshold():
    data = [{'val': 10}, {'val': 5}]
    total, results = proc(data, 5, True)
    # 10 is > 5 so it becomes 25.0
    # 5 is not > 5 so it remains 5
    assert total == 30.0
    assert results == [25.0, 5]

def test_proc_inactive():
    data = [{'val': 10}, {'val': 5}]
    total, results = proc(data, 5, False)
    assert total == 0
    assert results == []
"""
            return mock_tests
        else:
            return """// Mock JS test using Jest
const { proc } = require('./module');

test('proc filters correctly when active', () => {
  const data = [{val: 10}, {val: 5}];
  const [total, results] = proc(data, 5, true);
  expect(total).toBe(30.0);
  expect(results).toEqual([25.0, 5]);
});
"""

    prompt = TEST_PROMPT.format(language=language, refactored_code=refactored_code)

    if "Claude" in provider:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("Anthropic API Key is not set in environment.")
        client = Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=2500,
            temperature=0.2,
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.content[0].text
    elif "Gemini" in provider:
        content = call_gemini(prompt)
    elif "NVIDIA" in provider:
        content = call_nvidia(prompt)
    else:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API Key is not set in environment.")
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        data = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are an expert QA automation engineer."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2
        }
        resp = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
        if resp.status_code != 200:
            raise Exception(f"OpenAI API Error: {resp.text}")
        content = resp.json()["choices"][0]["message"]["content"]
    
    test_match = re.search(r"<unit_tests>(.*?)</unit_tests>", content, re.DOTALL)
    return test_match.group(1).strip() if test_match else content

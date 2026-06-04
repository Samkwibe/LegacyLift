"""
===============================================================================
Project: LegacyLift
File: refactor.py

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
Core engine for refactoring legacy code using LLM APIs.

Copyright © 2026 Samuel Raymond Kwibe.
All Rights Reserved.
===============================================================================
"""
import requests
import os
import re
import time

from anthropic import Anthropic
from core.prompts import REFACTOR_PROMPT
from core.gemini_client import call_gemini
from core.nvidia_client import call_nvidia

def refactor_code(source_code, language="Python", provider="Claude (Anthropic)"):
    # This function takes the messy code and sends it to an AI to fix it.

    if "Mock" in provider:
        time.sleep(2)
        mock_code = """def proc(data, threshold, is_active):
    \"\"\"
    Processes data based on threshold and activity flag.
    \"\"\"
    results = []
    for item in data:
        if is_active and threshold > 0:
            if item.get('val', 0) > threshold:
                results.append(item['val'] * 2.5)
            else:
                results.append(item['val'])
                
    total_sum = sum(results)
    return total_sum, results
"""
        mock_changelog = [
            "Added Google-style docstring",
            "Renamed variables to be more descriptive (d->data, x->threshold)",
            "Flattened deep nesting using combined conditions",
            "Replaced manual summing loop with sum() builtin"
        ]
        return mock_code, mock_changelog

    # Format the prompt using the language and source code
    prompt = REFACTOR_PROMPT.format(language=language, source_code=source_code)
    
    if "Claude" in provider:
        # Get the API key for Claude
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            print("Missing Anthropic API Key")
            raise ValueError("Anthropic API Key is not set in environment.")

        # Setup Anthropic client and make request
        client = Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=2000,
            temperature=0.2,
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.content[0].text
    elif "Gemini" in provider:
        content = call_gemini(prompt)
    elif "NVIDIA" in provider:
        content = call_nvidia(prompt)
    else:
        # OpenAI Fallback
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API Key is not set in environment.")
            
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are an expert software engineer."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2
        }
        resp = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
        if resp.status_code != 200:
            raise Exception(f"OpenAI API Error: {resp.text}")
            
        content = resp.json()["choices"][0]["message"]["content"]
    
    # Parse the XML tags to get the code and changelog
    refactored_match = re.search(r"<refactored_code>(.*?)</refactored_code>", content, re.DOTALL)
    changelog_match = re.search(r"<changelog>(.*?)</changelog>", content, re.DOTALL)
    
    # Check if we found the refactored code
    if refactored_match:
        refactored_code = refactored_match.group(1).strip()
    else:
        refactored_code = "Error: Could not parse refactored code from LLM response."
    
    # Check if we found the changelog
    if changelog_match:
        changelog_raw = changelog_match.group(1).strip()
    else:
        changelog_raw = ""
        
    # Split the changelog into a list
    changelog = []
    for line in changelog_raw.split('\n'):
        line = line.strip()
        if line:
            # Remove the dash at the start of the line
            if line.startswith('- '):
                line = line[2:]
            changelog.append(line)
    
    return refactored_code, changelog

"""
===============================================================================
Project: LegacyLift
File: documenter.py

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
Generates docstrings, READMEs, and OpenAPI schemas via AI.

Copyright © 2026 Samuel Raymond Kwibe.
All Rights Reserved.
===============================================================================
"""
import time
import re
import os
import requests
from anthropic import Anthropic
from core.prompts import DOCS_PROMPT
from core.gemini_client import call_gemini
from core.nvidia_client import call_nvidia

def generate_docs(refactored_code, language= "Python", provider= "Claude (Anthropic)"):
    """Generates Docstrings, a README section, and OpenAPI schema based on the refactored code.
    
    Args:
        refactored_code: The cleaned code from Step 2.
        language: The programming language.
        provider: The LLM provider chosen in the sidebar.
        
    Returns:
        A tuple of (documented_code, readme_section, openapi_schema).
    """
    if "Mock" in provider:
        time.sleep(2)
        mock_docs = '''def proc(data, threshold, is_active):
    """
    Processes a list of dictionaries by filtering against a threshold and an active flag,
    and returns the sum of the processed values.
    
    Args:
        data (list[dict]): The input data containing 'val' keys.
        threshold (int): The threshold to filter and process values against.
        is_active (bool): Flag indicating if the process is active.
        
    Returns:
        tuple(int, list): The sum of processed values and the list of processed values.
    """
    results = []
    for item in data:
        if is_active and threshold > 0:
            if item.get('val', 0) > threshold:
                results.append(item['val'] * 2.5)
            else:
                results.append(item['val'])
                
    total_sum = sum(results)
    return total_sum, results
'''
        mock_readme = "## Module Overview\nThis module processes dictionary data and applies threshold-based transformations safely."
        mock_openapi = "N/A"
        return mock_docs, mock_readme, mock_openapi

    prompt = DOCS_PROMPT.format(language=language, refactored_code=refactored_code)

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
                {"role": "system", "content": "You are an expert technical writer and developer."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2
        }
        resp = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
        if resp.status_code != 200:
            raise Exception(f"OpenAI API Error: {resp.text}")
        content = resp.json()["choices"][0]["message"]["content"]
    
    doc_match = re.search(r"<documented_code>(.*?)</documented_code>", content, re.DOTALL)
    readme_match = re.search(r"<readme_section>(.*?)</readme_section>", content, re.DOTALL)
    openapi_match = re.search(r"<openapi_schema>(.*?)</openapi_schema>", content, re.DOTALL)

    documented_code = doc_match.group(1).strip() if doc_match else refactored_code
    readme_section = readme_match.group(1).strip() if readme_match else "Could not generate README."
    openapi_schema = openapi_match.group(1).strip() if openapi_match else "N/A"

    return documented_code, readme_section, openapi_schema

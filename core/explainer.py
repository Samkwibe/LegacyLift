"""
===============================================================================
Project: LegacyLift
File: explainer.py

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
Provides line-by-line explanations and identifies flaws in code.

Copyright © 2026 Samuel Raymond Kwibe.
All Rights Reserved.
===============================================================================
"""
import os
import requests
import time
from core.prompts import NVIDIA_EXPLANATION_PROMPT
from core.gemini_client import call_gemini

def generate_explanation(source_code, refactored_code, provider= "Claude (Anthropic)"):
    """Generates a detailed explanation and code review using the NVIDIA API.
    
    Args:
        source_code: The original spaghetti code.
        refactored_code: The newly refactored code.
        provider: Used to determine if we should return Mock data.
        
    Returns:
        A markdown string containing the explanation.
    """
    if "Mock" in provider:
        time.sleep(2)
        return """### Code Review: The Flaws
- **Terrible Naming Convention:** Variable names like `d`, `x`, `r` are meaningless and make the code unreadable.
- **Deep Nesting (Arrow Code):** Multiple layers of `if` statements create a deep nested structure that is hard to maintain.
- **Manual Loops:** Using a manual `for` loop to sum up items is an anti-pattern when Python has the built-in `sum()` function.
- **Missing Error Handling:** It assumes `val` always exists in the dictionary, which could cause a `KeyError`.

### Line-by-Line Breakdown
1. `def proc(data, threshold, is_active):` - Added descriptive parameter names.
2. `results = []` - Initialized a new list for output.
3. `for item in data:` - Iterating through the input data dictionary.
4. `if is_active and threshold > 0:` - Flattened the nesting by combining the boolean checks into a single line.
5. `if item.get('val', 0) > threshold:` - Safely accesses the `val` key with a default of 0 to prevent crashes.
6. `total_sum = sum(results)` - Uses Python's built-in sum for better performance and readability.
"""

    prompt = NVIDIA_EXPLANATION_PROMPT.format(source_code=source_code, refactored_code=refactored_code)
    
    if "Gemini" in provider:
        return call_gemini(prompt)
        
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        return "⚠️ NVIDIA API Key not found in environment. Please add NVIDIA_API_KEY to your .env file to see the AI Explanation."
        
    headers = {
        "Authorization": f"Bearer {api_key}",
        "accept": "application/json",
        "content-type": "application/json"
    }
    
    data = {
        "model": "meta/llama3-70b-instruct",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 1500
    }
    
    try:
        response = requests.post("https://integrate.api.nvidia.com/v1/chat/completions", headers=headers, json=data)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"NVIDIA API Error: {response.text}"
    except Exception as e:
        return f"Failed to connect to NVIDIA API: {str(e)}"

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
import time
from core.prompts import NVIDIA_EXPLANATION_PROMPT
from core.gemini_client import call_gemini
from core.nvidia_client import call_nvidia

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
    elif "NVIDIA" in provider:
        return call_nvidia(prompt)
    elif "Claude" in provider:
        from anthropic import Anthropic
        client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=4000,
            temperature=0.1,
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
            "temperature": 0.1
        }
        import requests
        resp = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
        if resp.status_code == 200:
            return resp.json()["choices"][0]["message"]["content"]
        else:
            raise Exception(f"OpenAI API Error: {resp.text}")
    return "Error: Unknown provider selected."

        


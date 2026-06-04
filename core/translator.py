"""
===============================================================================
Project: LegacyLift
File: translator.py

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
Translates legacy code into modern target programming languages.

Copyright © 2026 Samuel Raymond Kwibe.
All Rights Reserved.
===============================================================================
"""
import time
import os
import requests
from core.refactor import call_gemini

TRANSLATE_PROMPT = """You are an expert polyglot software engineer.
Translate the following code into {target_language}.
Ensure the logic remains identical, but apply the modern idioms, standard libraries, and best practices of {target_language}.
Do NOT output any markdown blocks, just raw code. If you must use markdown, only use it for the code block.

Original Code:
{code}
"""

def translate_code(source_code, target_language, provider="Gemini 3.5 Flash (Google) - FREE"):
    """Translates code to a new language."""
    if "Mock" in provider:
        time.sleep(2)
        return f"// Translated to {target_language}\n\nfunction processData(data) {{\n    return data.map(item => item * 2);\n}}"

    prompt = TRANSLATE_PROMPT.format(code=source_code, target_language=target_language)
    
    if "Gemini" in provider:
        return call_gemini(prompt)
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
        resp = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
        if resp.status_code == 200:
            return resp.json()["choices"][0]["message"]["content"]
        else:
            raise Exception(f"OpenAI API Error: {resp.text}")
            
    return "Error: Unknown provider selected."

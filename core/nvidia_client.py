"""
===============================================================================
Project: LegacyLift
File: nvidia_client.py

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
Wrapper for the NVIDIA NIM API.

Copyright © 2026 Samuel Raymond Kwibe.
All Rights Reserved.
===============================================================================
"""
import os
import requests

def call_nvidia(prompt, temperature=0.2):
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        raise Exception("NVIDIA_API_KEY not found in .env file.")
        
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "meta/llama3-70b-instruct",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": 4000
    }
    resp = requests.post("https://integrate.api.nvidia.com/v1/chat/completions", headers=headers, json=data)
    
    if resp.status_code == 200:
        return resp.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"NVIDIA API Error: {resp.text}")

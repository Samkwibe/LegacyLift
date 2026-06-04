"""
===============================================================================
Project: LegacyLift
File: gemini_client.py

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
Helper client for executing REST requests to Google Gemini API.

Copyright © 2026 Samuel Raymond Kwibe.
All Rights Reserved.
===============================================================================
"""
import os
import requests

def call_gemini(prompt, temperature=0.3):
    """Helper to call the Gemini 3.5 Flash REST API without needing extra pip packages."""
    
    # First we need to get our API key from the environment variables
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: No API key found!")
        raise ValueError("GEMINI_API_KEY is not set in your .env file.")
        
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    
    # Set up the data we want to send to the API
    data = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": temperature}
    }
    
    # Make the actual post request using requests
    resp = requests.post(url, headers=headers, json=data)
    
    if resp.status_code != 200:
        raise Exception(f"Gemini API Error: {resp.text}")
        
    # If we get a 200 OK, we try to parse the JSON
    try:
        json_response = resp.json()
        final_text = json_response["candidates"][0]["content"]["parts"][0]["text"]
        return final_text
    except Exception as e:
        # Broad exception catch like a student might do
        print("Something went wrong while parsing!")
        raise Exception(f"Failed to parse Gemini response: {resp.text}")

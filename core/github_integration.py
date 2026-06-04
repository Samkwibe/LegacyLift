"""
===============================================================================
Project: LegacyLift
File: github_integration.py

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
Downloads a GitHub repository as a ZIP file in-memory using the GitHub API.

Copyright © 2026 Samuel Raymond Kwibe.
All Rights Reserved.
===============================================================================
"""
import requests
import io
import re

def download_github_repo(repo_url):
    """
    Downloads a GitHub repository as a zip file.
    Expects URL format: https://github.com/username/repo
    """
    # Clean the URL
    repo_url = repo_url.strip()
    if repo_url.endswith(".git"):
        repo_url = repo_url[:-4]
    if repo_url.endswith("/"):
        repo_url = repo_url[:-1]
        
    # Extract owner and repo
    match = re.search(r"github\.com/([^/]+)/([^/]+)", repo_url)
    if not match:
        raise ValueError("Invalid GitHub URL. Must be in format https://github.com/username/repo")
        
    owner, repo = match.groups()
    
    # Try downloading the 'main' branch zip
    zip_url = f"https://github.com/{owner}/{repo}/archive/refs/heads/main.zip"
    response = requests.get(zip_url)
    
    # If 404, try 'master' branch
    if response.status_code == 404:
        zip_url = f"https://github.com/{owner}/{repo}/archive/refs/heads/master.zip"
        response = requests.get(zip_url)
        
    if response.status_code != 200:
        raise Exception(f"Failed to download repository. HTTP {response.status_code}. Make sure it is public.")
        
    # Return as an in-memory byte stream
    return io.BytesIO(response.content)

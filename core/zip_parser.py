"""
===============================================================================
Project: LegacyLift
File: zip_parser.py

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
Extracts and parses zip files in-memory, reading all code files.

Copyright © 2026 Samuel Raymond Kwibe.
All Rights Reserved.
===============================================================================
"""
import zipfile
import os

def parse_zip_file(zip_bytes_io):
    """
    Takes an io.BytesIO zip file and extracts all text code files,
    combining them into a structured string for analysis.
    """
    valid_extensions = {
        '.py', '.js', '.ts', '.java', '.cpp', '.c', '.h', '.cs', 
        '.php', '.rb', '.go', '.rs', '.swift', '.kt', '.html', '.css', 
        '.sql', '.sh', '.bash', '.md', '.json', '.txt'
    }
    
    ignore_dirs = {
        'venv', '.git', 'node_modules', '__pycache__', '.pytest_cache', 'build', 'dist'
    }
    
    combined_code = ""
    
    try:
        with zipfile.ZipFile(zip_bytes_io, 'r') as z:
            for file_info in z.infolist():
                if file_info.is_dir():
                    continue
                    
                filename = file_info.filename
                
                # Check for ignored directories
                parts = filename.split('/')
                if any(part in ignore_dirs for part in parts):
                    continue
                    
                ext = os.path.splitext(filename)[1].lower()
                if ext not in valid_extensions:
                    continue
                    
                try:
                    with z.open(file_info) as f:
                        content = f.read().decode('utf-8')
                        combined_code += f"\n\n=======================================================\n"
                        combined_code += f"FILE: {filename}\n"
                        combined_code += f"=======================================================\n"
                        combined_code += content
                except Exception:
                    # Ignore files that fail to decode (e.g. binaries mistakenly parsed)
                    pass
    except zipfile.BadZipFile:
        raise ValueError("The uploaded file is not a valid ZIP archive.")
        
    return combined_code

"""
===============================================================================
Project: LegacyLift
File: ui_theme.py

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
Provides custom CSS styling for the Streamlit user interface.

Copyright © 2026 Samuel Raymond Kwibe.
All Rights Reserved.
===============================================================================
"""
def get_custom_css():
    return """
    <style>
        /* Import premium web fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Fira+Code:wght@400;500&display=swap');

        /* Global Font Adjustments */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif !important;
        }

        /* Code blocks */
        code, pre {
            font-family: 'Fira Code', monospace !important;
        }

        /* Subtle textured background */
        .stApp {
            background-color: #0d1117;
            background-image: radial-gradient(circle at center, rgba(255,255,255,0.03) 1px, transparent 1px);
            background-size: 20px 20px;
        }

        /* Glassmorphism Sidebar */
        [data-testid="stSidebar"] {
            background: rgba(13, 17, 23, 0.7) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }

        /* Premium Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 10px 24px !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 14px 0 rgba(99, 102, 241, 0.39) !important;
            transition: all 0.2s ease-in-out !important;
        }

        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5) !important;
        }

        .stButton > button:active {
            transform: translateY(0px) !important;
        }

        /* Cards and Columns */
        div[data-testid="column"] {
            background: rgba(22, 27, 34, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 1rem;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
            backdrop-filter: blur(4px);
        }

        /* Headers */
        h1, h2, h3, h4, h5, h6 {
            color: #f0f6fc !important;
            letter-spacing: -0.02em !important;
        }
    </style>
    """

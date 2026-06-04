# ⚡ LegacyLift: AI-Powered Code Modernization & Mentorship Engine

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Framework-FF4B4B?style=for-the-badge&logo=streamlit)
![Gemini](https://img.shields.io/badge/Google-Gemini_3.5_Flash-4285F4?style=for-the-badge&logo=google)
![Anthropic](https://img.shields.io/badge/Anthropic-Claude_3-black?style=for-the-badge&logo=anthropic)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT_4o-412991?style=for-the-badge&logo=openai)
![NVIDIA](https://img.shields.io/badge/NVIDIA-NIM_API-76B900?style=for-the-badge&logo=nvidia)

🚀 **Live Demo:** [https://legacylift-aywfjmusd5qnvevgewdynk.streamlit.app/](https://legacylift-aywfjmusd5qnvevgewdynk.streamlit.app/)

**LegacyLift** is a state-of-the-art AI-powered code modernization and mentorship tool. Designed for developers and students alike, it takes poorly written, undocumented "spaghetti code" and automatically refactors it into clean, maintainable, and fully documented production-ready code.

Not only does it fix code—it **teaches** you how to write better code. Through deep architectural analysis, visual mentorship, and line-by-line feedback, LegacyLift acts as your personal Senior Software Engineer.

---

## 👨‍💻 Author Profile

**Samuel Raymond Kwibe**  
*B.S. Computer Science Student, Southern New Hampshire University (SNHU)*

**Professional Focus:**
- Software Engineering
- Artificial Intelligence (AI)
- Cloud Engineering
- Full-Stack Development

🔗 **LinkedIn:** [samuel-kwibe-371633249](https://www.linkedin.com/in/samuel-kwibe-371633249/)  
🔗 **GitHub:** [Samkwibe](https://github.com/Samkwibe)  

---

## ✨ Key Features

- **🔍 Intelligent Static Analysis**: Automatically detects "Code Smells" (e.g., deep nesting, magic numbers, missing docstrings) using AST (Abstract Syntax Tree) parsing before AI processing.
- **🛠️ Multi-LLM Refactoring Engine**: Seamlessly switch between **Gemini 3.5 Flash**, **Claude**, **GPT-4o**, or **Llama 3.1 70B (via NVIDIA)** to rewrite legacy code according to clean-code principles. 
- **📥 GitHub & ZIP Support**: Clone entire public GitHub repositories or upload full `.zip` archives for repository-scale structural analysis.
- **🌐 Polyglot Code Translation**: Instantly translate legacy codebases into modern languages like Python, JavaScript, Go, Rust, or C++.
- **🛡️ Security Vulnerability Scanner**: Deep AI auditing to identify CVEs, injection flaws, exposed secrets, and logic bugs before they hit production.
- **📄 PDF Report Export**: Generate beautiful, formatted PDF reports of your code reviews, documentation, and security audits to share with your team.
- **📚 Automated Documentation**: Generates professional Google-style docstrings, high-level README module overviews, and OpenAPI schemas for REST endpoints.
- **🧠 NVIDIA Deep-Dive Code Review**: Leverages NVIDIA's API to perform a deep-dive code review—pointing out exactly what was wrong with the original code, including bugs, bad practices, and performance issues, with a line-by-line breakdown.
- **🗺️ Interactive Project Walkthrough**: Automatically scans entire project structures, explaining folder hierarchies, data flows, and architectures in both beginner and advanced terms.
- **🧪 Unit Test Generation**: Writes comprehensive `pytest` or `jest` test suites covering edge cases and happy paths.
- **💎 Premium Glassmorphism UI**: A stunning, modern, and highly responsive user interface featuring custom typography, gradients, and dynamic visual themes.

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.10+
- An API Key from Google Gemini (Free), Anthropic, OpenAI, or NVIDIA. (You can also use the built-in "Mock" provider for a quick demo!)

### 1. Clone the repository:
```bash
git clone https://github.com/Samkwibe/LegacyLift.git
cd LegacyLift
```

### 2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install the dependencies:
```bash
pip install -r requirements.txt
```

### 4. Configuration:
Rename `.env.example` to `.env` and add your API keys:
```text
GEMINI_API_KEY=your_gemini_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
OPENAI_API_KEY=your_openai_key_here
NVIDIA_API_KEY=your_nvidia_key_here
```

---

## 🎮 Usage

Run the application locally using Streamlit:
```bash
./venv/bin/python -m streamlit run app.py
```
Open your browser to `http://localhost:8501`. 

1. **Choose your LLM Provider** from the sleek sidebar.
2. **Paste your legacy code** into the main interface.
3. **Follow the interactive workflow** to Analyze, Refactor, Document, Review, and Test your code!

---

## 🏗️ Architecture

- **Frontend**: Streamlit with Custom CSS (Glassmorphism UI Theme)
- **Backend Core**: Python (AST Module, Regex Parsing, REST Requests)
- **AI Integration Layers**: 
  - `core/gemini_client.py`
  - `core/refactor.py` (Claude / OpenAI / Gemini Integrations)
  - `core/explainer.py` (NVIDIA Code Review Engine)

---

## 📝 License
Copyright © 2026 Samuel Raymond Kwibe.  
All Rights Reserved.

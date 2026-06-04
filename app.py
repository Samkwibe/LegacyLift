"""
===============================================================================
Project: LegacyLift
File: app.py

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
Main entry point for the LegacyLift Streamlit application.

Copyright © 2026 Samuel Raymond Kwibe.
All Rights Reserved.
===============================================================================
"""
from core.analyzer import analyze_code
from core.documenter import generate_docs
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()
from core.refactor import refactor_code
from core.explainer import generate_explanation
from core.test_generator import generate_tests
from core.project_analyzer import scan_local_codebase, generate_project_walkthrough
from core.ui_theme import get_custom_css
from core.github_integration import download_github_repo
from core.zip_parser import parse_zip_file
from core.security import run_security_audit
from core.translator import translate_code
from core.pdf_export import markdown_to_pdf

def init_state():
    # Set up our variables for Streamlit's session state so they don't get lost on refresh
    if "source_code" not in st.session_state:
        st.session_state.source_code = ""
    if "refactored_code" not in st.session_state:
        st.session_state.refactored_code = None
    if "changelog" not in st.session_state:
        st.session_state.changelog = None
    if "step3_unlocked" not in st.session_state:
        st.session_state.step3_unlocked = False
    if "docs" not in st.session_state:
        st.session_state.docs = None
    if "explanation" not in st.session_state:
        st.session_state.explanation = None
    if "step4_unlocked" not in st.session_state:
        st.session_state.step4_unlocked = False
    if "tests" not in st.session_state:
        st.session_state.tests = None
    if "mode" not in st.session_state:
        st.session_state.mode = "Single File Refactoring"
    if "walkthrough_report" not in st.session_state:
        st.session_state.walkthrough_report = None

st.set_page_config(
    page_title="LegacyLift",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

def render_sidebar():
    # This renders the left-hand menu for our application
    st.sidebar.title("⚡ LegacyLift")
    st.sidebar.markdown("**AI code refactoring tool**")
    st.sidebar.markdown("---")
    
    st.sidebar.subheader("App Mode")
    mode = st.sidebar.radio("Choose Mode", ["Single File Refactoring", "Full Project Walkthrough", "Security Audit", "Code Translation"])
    st.session_state.mode = mode
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("LLM Provider")
    provider = st.sidebar.selectbox("Choose Provider", ["Mock (Free Demo)", "Gemini 3.5 Flash (Google) - FREE", "Claude (Anthropic)", "GPT-4o (OpenAI)"])
    st.session_state.provider = provider
    
    st.sidebar.subheader("Language")
    languages = [
        "Python", "JavaScript", "TypeScript", "Java", "C++", "C#", 
        "PHP", "Ruby", "Go", "Rust", "Swift", "Kotlin", "HTML", "CSS", "SQL", "Bash"
    ]
    # Loop through a list of languages for the dropdown
    default_lang = st.session_state.get("language", "Python")
    default_idx = languages.index(default_lang) if default_lang in languages else 0
    language = st.sidebar.selectbox("Choose Language", languages, index=default_idx)
    st.session_state.language = language
    
    if mode == "Code Translation":
        st.sidebar.subheader("Target Language")
        target_language = st.sidebar.selectbox("Translate To", languages, index=0)
        st.session_state.target_language = target_language
    
    st.sidebar.subheader("Load Example")
    example = st.sidebar.selectbox("Choose Example", [
        "— choose example —",
        "Spaghetti function",
        "God class",
        "No docstrings",
        "JS callback hell"
    ])
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Workflow")
    st.sidebar.markdown("1. Input code")
    st.sidebar.markdown("2. Refactor & review")
    st.sidebar.markdown("3. Documentation")
    st.sidebar.markdown("4. Unit tests")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("[GitHub](https://github.com/Samkwibe) | About LegacyLift")

def main():
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    init_state()
    render_sidebar()
    
    if st.session_state.mode == "Full Project Walkthrough":
        st.title("📂 Full Project Walkthrough")
        st.markdown("Acting as a Senior Mentor, LegacyLift will automatically scan the entire local codebase and explain the architecture, data flow, security, and the difficulties faced during development.")
        
        if st.button("🚀 Explain This Project", type="primary", use_container_width=True):
            with st.spinner("Scanning codebase and analyzing architecture... this may take a minute."):
                try:
                    codebase_str = scan_local_codebase(".")
                    report = generate_project_walkthrough(codebase_str, st.session_state.provider)
                    st.session_state.walkthrough_report = report
                except Exception as e:
                    st.error(f"Analysis failed: {str(e)}")
                    
        if st.session_state.walkthrough_report:
            st.markdown("---")
            st.download_button("Download Report (Markdown)", st.session_state.walkthrough_report, file_name="Project_Walkthrough.md")
            try:
                pdf_bytes = markdown_to_pdf(st.session_state.walkthrough_report)
                st.download_button("Download Report (PDF)", pdf_bytes, file_name="Project_Walkthrough.pdf", mime="application/pdf")
            except Exception as e:
                st.error(f"Could not generate PDF: {e}")
            st.markdown(st.session_state.walkthrough_report)
            
    else:
        st.title(f"Step 1 — Input your code ({st.session_state.mode})")
        st.markdown("Upload a file, paste your code, or import from GitHub to begin.")
        
        github_url = st.text_input("🔗 Import from a GitHub repository URL (e.g., https://github.com/Samkwibe/LegacyLift)")
        uploaded_file = st.file_uploader("📂 Drop your file or .zip archive here", type=["py", "js", "zip"])
        
        code_input = st.text_area("✍️ Or paste your legacy code", height=300)
        current_code = ""
        
        try:
            if github_url:
                with st.spinner("Downloading and extracting GitHub repository..."):
                    zip_io = download_github_repo(github_url)
                    current_code, detected_lang = parse_zip_file(zip_io)
                    if detected_lang and st.session_state.language != detected_lang:
                        st.session_state.language = detected_lang
                        st.rerun()
            elif uploaded_file:
                if uploaded_file.name.endswith(".zip"):
                    current_code, detected_lang = parse_zip_file(uploaded_file)
                    if detected_lang and st.session_state.language != detected_lang:
                        st.session_state.language = detected_lang
                        st.rerun()
                else:
                    current_code = uploaded_file.getvalue().decode("utf-8")
            elif code_input:
                current_code = code_input
        except Exception as e:
            st.error(f"Error loading code: {str(e)}")

        col1, col2 = st.columns([1, 1])
        with col1:
            analyze_clicked = st.button("Analyze Code")
        with col2:
            refactor_clicked = st.button("Start AI Process", type="primary")

        if analyze_clicked:
            if current_code:
                st.session_state.source_code = current_code
                smells = analyze_code(current_code)
                
                if not smells:
                    st.success("No code smells detected! Great job!")
                else:
                    st.subheader("Static analysis results")
                    for smell in smells:
                        msg = smell["message"]
                        if smell["type"] == "err":
                            st.error(f"**Error**: {msg}")
                        elif smell["type"] == "warn":
                            st.warning(f"**Warning**: {msg}")
                        else:
                            st.info(f"**Info**: {msg}")
            else:
                st.error("Please provide code to analyze.")

        # Syntax mapping
        syntax_map = {
            "Python": "python", "JavaScript": "javascript", "TypeScript": "typescript", 
            "Java": "java", "C++": "cpp", "C#": "csharp", "PHP": "php", "Ruby": "ruby", 
            "Go": "go", "Rust": "rust", "Swift": "swift", "Kotlin": "kotlin", 
            "HTML": "html", "CSS": "css", "SQL": "sql", "Bash": "bash"
        }
        current_lang = st.session_state.get("language", "Python")
        syntax_lang = syntax_map.get(current_lang, "python")

        if refactor_clicked:
            if current_code:
                st.session_state.refactored_code = None
                st.session_state.changelog = None
                st.session_state.explanation = None
                st.session_state.docs = None
                st.session_state.step3_unlocked = False
                
                st.session_state.source_code = current_code
                with st.spinner(f"Refactoring code using {st.session_state.get('provider', 'Claude (Anthropic)')}..."):
                    try:
                        if st.session_state.mode == "Security Audit":
                            res = run_security_audit(current_code, provider=st.session_state.get('provider', 'Claude (Anthropic)'))
                            st.session_state.refactored_code = res
                            st.session_state.changelog = ["Security audit completed."]
                        elif st.session_state.mode == "Code Translation":
                            res = translate_code(current_code, st.session_state.target_language, provider=st.session_state.get('provider', 'Claude (Anthropic)'))
                            st.session_state.refactored_code = res
                            st.session_state.changelog = [f"Translated code to {st.session_state.target_language}."]
                        else:
                            refactored, changelog = refactor_code(current_code, provider=st.session_state.get('provider', 'Claude (Anthropic)'))
                            st.session_state.refactored_code = refactored
                            st.session_state.changelog = changelog
                    except Exception as e:
                        st.error(f"Refactoring failed: {e}")
                        
                if st.session_state.refactored_code:
                    with st.spinner("Generating code review..."):
                        explanation = generate_explanation(
                            st.session_state.source_code,
                            st.session_state.refactored_code,
                            st.session_state.get("provider", "Claude (Anthropic)")
                        )
                        st.session_state.explanation = explanation
            else:
                st.error("Please provide code to refactor.")

        if st.session_state.refactored_code:
            st.markdown("---")
            st.title("Step 2 — Review & Feedback")
            
            col_main, col_feedback = st.columns([2, 1])
            
            with col_main:
                st.markdown("#### Original Code")
                st.code(st.session_state.source_code, language=syntax_lang)
                st.markdown("#### Refactored Code")
                st.code(st.session_state.refactored_code, language=syntax_lang)
                
            with col_feedback:
                st.markdown("### Code Review Feedback")
                if st.session_state.explanation:
                    st.markdown(st.session_state.explanation)
                    
                st.markdown("### Explanation of Changes")
                if st.session_state.changelog:
                    for item in st.session_state.changelog:
                        st.markdown(f"- {item}")
                
            col_btn1, col_btn2 = st.columns([1, 1])
            with col_btn1:
                if st.button("❌ Reject & Start Over", use_container_width=True):
                    st.session_state.clear()
                    st.rerun()
            with col_btn2:
                if st.button("✅ Accept & Generate Documentation", use_container_width=True):
                    st.session_state.step3_unlocked = True
                    st.rerun()

        # Step 3
        if st.session_state.get("step3_unlocked"):
            st.markdown("---")
            st.header("Step 3: Documentation")
            
            if st.session_state.docs is None:
                with st.spinner("Generating documentation..."):
                    doc_code, readme, openapi = generate_docs(
                        st.session_state.refactored_code, 
                        st.session_state.get("language", "Python"),
                        st.session_state.get("provider", "Claude (Anthropic)")
                    )
                    st.session_state.docs = {
                        "documented_code": doc_code,
                        "readme": readme,
                        "openapi": openapi
                    }
                    st.rerun()

            tab1, tab2, tab3 = st.tabs(["Docstrings", "README", "OpenAPI Schema"])
            
            with tab1:
                st.code(st.session_state.docs["documented_code"], language=syntax_lang)
                st.download_button("Download Documented Code", st.session_state.docs["documented_code"], file_name="documented_code.txt")
                
            with tab2:
                st.markdown(st.session_state.docs["readme"])
                st.download_button("Download README", st.session_state.docs["readme"], file_name="README.md")
                
            with tab3:
                st.code(st.session_state.docs["openapi"], language="yaml")
                
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🧪 Generate Unit Tests", use_container_width=True, type="primary"):
                st.session_state.step4_unlocked = True
                st.rerun()

        # Step 4
        if st.session_state.get("step4_unlocked"):
            st.markdown("---")
            st.header("Step 4: Unit Test Generation")
            
            if st.session_state.tests is None:
                with st.spinner("Writing test cases..."):
                    st.session_state.tests = generate_tests(
                        st.session_state.refactored_code,
                        st.session_state.get("language", "Python"),
                        st.session_state.get("provider", "Claude (Anthropic)")
                    )
                    st.rerun()
                    
            st.markdown("### Test Suite")
            st.code(st.session_state.tests, language=syntax_lang)
            
            file_ext = ".py" if st.session_state.get("language", "Python") == "Python" else ".js"
            st.download_button(
                "Download Test File",
                st.session_state.tests,
                file_name=f"test_refactored{file_ext}"
            )


if __name__ == "__main__":
    main()

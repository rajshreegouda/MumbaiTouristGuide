@echo off
setlocal
cd /d "%~dp0"
set "TEMP=%~dp0.cache\tmp"
set "TMP=%~dp0.cache\tmp"
set "PIP_CACHE_DIR=%~dp0.cache\pip"
set "STREAMLIT_BROWSER_GATHER_USAGE_STATS=false"
set "PYTHONDONTWRITEBYTECODE=1"
REM Optional: enable the Claude-powered chatbot (otherwise the offline ML chatbot is used)
REM set "ANTHROPIC_API_KEY=sk-ant-xxxxxxxx"
mkdir "%TEMP%" 2>nul
call .venv\Scripts\activate.bat
python -m streamlit run app.py
pause

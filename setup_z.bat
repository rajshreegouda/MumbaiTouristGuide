@echo off
REM ===== One-time setup. Keeps EVERYTHING (venv, pip cache, temp files) inside this folder on Z: =====
setlocal
cd /d "%~dp0"
if /I not "%~d0"=="Z:" (
  echo WARNING: this folder is on %~d0 and not on Z:. Move it to Z:\MumbaiTouristGuide first.
  pause & exit /b 1
)
set "PIP_CACHE_DIR=%~dp0.cache\pip"
set "TEMP=%~dp0.cache\tmp"
set "TMP=%~dp0.cache\tmp"
mkdir "%PIP_CACHE_DIR%" 2>nul
mkdir "%TEMP%" 2>nul

where py >nul 2>nul && (set "PY=py -3") || (set "PY=python")
%PY% --version || (echo Python not found. See README step 1. & pause & exit /b 1)

%PY% -m venv .venv || (pause & exit /b 1)
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt || (echo Install failed - check internet. & pause & exit /b 1)

echo Downloading real photos for the places...
python fetch_images.py
echo.
echo Setup finished. Start the website by double-clicking run.bat
pause

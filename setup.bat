@echo off
echo.
echo ========================================================
echo    Global Regulatory Compliance Auditor - Setup
echo ========================================================
echo.

REM Check Python version
echo Checking Python version...
python --version
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python not found. Please install Python 3.8 or higher.
    pause
    exit /b 1
)
echo Python found!
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
if %ERRORLEVEL% NEQ 0 (
    echo WARNING: Could not create virtual environment. Installing globally...
) else (
    echo Virtual environment created!
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed!
echo.

REM Create directories
echo Creating directories...
if not exist "models" mkdir models
if not exist "regulations" mkdir regulations
echo Directories created!
echo.

REM Check for regulation files
echo Checking regulation configurations...
set reg_count=0
for %%f in (regulations\*.json) do set /a reg_count+=1

if %reg_count%==0 (
    echo WARNING: No regulation configurations found in regulations\
    echo Please add regulation JSON files to the regulations\ directory
) else (
    echo Found %reg_count% regulation configuration(s)
)
echo.

REM Success message
echo ========================================================
echo            Setup Complete!
echo.
echo To start the application:
echo    1. Activate environment: venv\Scripts\activate.bat
echo    2. Start backend: python app.py
echo    3. Open frontend.html in your browser
echo.
echo For more information, see README.md
echo ========================================================
echo.
pause

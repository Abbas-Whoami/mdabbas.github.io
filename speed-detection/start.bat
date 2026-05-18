@echo off
title Vehicle Speed Detection System - Setup and Run
color 0A

echo ============================================================
echo   Vehicle Speed Detection System
echo   Setup and Run Script
echo ============================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo.
    echo Please download and install Python from:
    echo https://www.python.org/downloads/
    echo.
    echo IMPORTANT: During installation, check the box that says
    echo "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo [OK] Python found:
python --version
echo.

:: Check if input video exists
if not exist "input\footage.mp4" (
    echo [ERROR] Video file not found!
    echo.
    echo Please place your video file as:
    echo   input\footage.mp4
    echo.
    echo Create the 'input' folder if it doesn't exist and
    echo copy your video file there with the name 'footage.mp4'
    echo.
    pause
    exit /b 1
)

echo [OK] Input video found: input\footage.mp4
echo.

:: Create virtual environment if it doesn't exist
if not exist "venv" (
    echo [SETUP] Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created.
    echo.
) else (
    echo [OK] Virtual environment already exists.
    echo.
)

:: Activate virtual environment
echo [SETUP] Activating virtual environment...
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated.
echo.

:: Install dependencies
echo [SETUP] Installing dependencies (this may take a few minutes)...
echo.
pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)
echo.
echo [OK] All dependencies installed.
echo.

:: Download YOLO model if not present
if not exist "models\yolov8n.pt" (
    echo [SETUP] Downloading YOLO model (~6MB)...
    python download_model.py
    if %errorlevel% neq 0 (
        echo.
        echo [WARNING] Model download failed. The system will use
        echo fallback classification (size-based detection).
        echo.
    ) else (
        echo [OK] YOLO model downloaded.
        echo.
    )
) else (
    echo [OK] YOLO model already exists.
    echo.
)

:: Create output directory
if not exist "output" mkdir output

:: Run the application
echo ============================================================
echo   Starting Vehicle Speed Detection...
echo   Press 'Q' on the video window to stop.
echo ============================================================
echo.

python run.py

echo.
echo ============================================================
echo   Processing complete!
echo   Output saved to: output\footage_processed.mp4
echo ============================================================
echo.

:: Deactivate virtual environment
call venv\Scripts\deactivate.bat >nul 2>&1

pause

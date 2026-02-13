@echo off
echo ========================================
echo Starting Daily Weather Discord Bot
echo ========================================
echo.

echo [1/3] Activating conda environment (myENV)...
call D:\miniconda\Scripts\activate.bat myENV
if errorlevel 1 (
    echo ERROR: Failed to activate environment
    pause
    exit /b 1
)

echo [2/3] Changing to project directory...
cd /d D:\DATA\Code\daily-bot-discord
if errorlevel 1 (
    echo ERROR: Failed to change directory
    pause
    exit /b 1
)

echo [3/3] Starting bot...
echo.
D:\miniconda\envs\myENV\python.exe bot/main.py

echo.
echo ========================================
echo Bot stopped
echo ========================================
pause

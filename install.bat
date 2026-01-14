@echo off
REM Installation script for Egile Investment Agent (Windows)

echo ========================================
echo Egile Investment Agent - Installation
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10 or higher
    pause
    exit /b 1
)

echo Installing egile-mcp-investment...
cd ..\egile-mcp-investment
pip install -e .
if errorlevel 1 (
    echo ERROR: Failed to install egile-mcp-investment
    pause
    exit /b 1
)

echo.
echo Installing egile-agent-investment...
cd ..\egile-agent-investment
pip install -e .
if errorlevel 1 (
    echo ERROR: Failed to install egile-agent-investment
    pause
    exit /b 1
)

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo To run the investment agent:
echo   investment              - Run both MCP server and agent
echo   investment-mcp          - Run only MCP server
echo   investment-agent        - Run only agent with web UI
echo.
echo The agent will be available at http://localhost:7674
echo.
pause

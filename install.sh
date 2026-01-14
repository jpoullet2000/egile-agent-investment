#!/bin/bash
# Installation script for Egile Investment Agent (Linux/Mac)

echo "========================================"
echo "Egile Investment Agent - Installation"
echo "========================================"
echo

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python is not installed"
    echo "Please install Python 3.10 or higher"
    exit 1
fi

echo "Installing egile-mcp-investment..."
cd ../egile-mcp-investment
pip install -e .
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install egile-mcp-investment"
    exit 1
fi

echo
echo "Installing egile-agent-investment..."
cd ../egile-agent-investment
pip install -e .
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install egile-agent-investment"
    exit 1
fi

echo
echo "========================================"
echo "Installation Complete!"
echo "========================================"
echo
echo "To run the investment agent:"
echo "  investment              - Run both MCP server and agent"
echo "  investment-mcp          - Run only MCP server"
echo "  investment-agent        - Run only agent with web UI"
echo
echo "The agent will be available at http://localhost:7674"
echo

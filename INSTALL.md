# Installation Guide - Investment Agent

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Internet connection (for stock data)

## Installation Methods

### Method 1: Quick Install (Recommended)

**Windows:**
```bash
cd egile-agent-investment
install.bat
```

**Linux/Mac:**
```bash
cd egile-agent-investment
chmod +x install.sh
./install.sh
```

This will install both the MCP server and the agent plugin.

### Method 2: Manual Installation

1. **Install MCP Server:**
   ```bash
   cd egile-mcp-investment
   pip install -e .
   ```

2. **Install Agent:**
   ```bash
   cd egile-agent-investment
   pip install -e .
   ```

### Method 3: Via Hub

If using with Egile Agent Hub:

1. **Install Hub:**
   ```bash
   cd egile-agent-hub
   pip install -e .
   ```

2. **Install Investment Agent:**
   ```bash
   cd egile-agent-investment
   pip install -e .
   ```

3. **Configure in agents.yaml:**
   The investment agent is already configured in the hub's agents.yaml

4. **Start Hub:**
   ```bash
   cd egile-agent-hub
   agent-hub
   ```

## Verification

### Verify Installation

Check that packages are installed:
```bash
pip show egile-mcp-investment
pip show egile-agent-investment
```

### Test MCP Server

```bash
cd egile-mcp-investment
python test_service.py
```

Expected output: Stock analysis for AAPL, MSFT, and portfolio summary

### Test Agent

**Start the agent:**
```bash
cd egile-agent-investment
investment
```

**Access web UI:**
Open browser to `http://localhost:7674`

**Try a query:**
```
Show me portfolio tools available
```

## Configuration

### 1. Environment Variables

Copy the example file:
```bash
cd egile-agent-investment
copy .env.example .env  # Windows
# or
cp .env.example .env    # Linux/Mac
```

Edit `.env` with your settings:
```bash
# Required if using OpenAI
OPENAI_API_KEY=your_api_key_here

# Optional: Custom ports
INVESTMENT_MCP_PORT=8004
INVESTMENT_AGENT_PORT=7674
```

### 2. Portfolio Configuration

Create a portfolio file (optional):
```bash
cd egile-agent-investment
copy portfolio.csv.example portfolio.csv  # Windows
# or
cp portfolio.csv.example portfolio.csv    # Linux/Mac
```

Edit `portfolio.csv`:
```csv
ticker,shares,purchase_price
AAPL,10,150.00
MSFT,5,300.00
GOOGL,3,140.00
```

## Starting the Agent

### Standalone Mode

**Full system (recommended):**
```bash
investment
```

**MCP server only:**
```bash
investment-mcp
```

**Agent only (requires MCP server running separately):**
```bash
investment-agent
```

### Via Start Scripts

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

### Via Hub

```bash
cd egile-agent-hub
agent-hub
```

The investment agent will start automatically if configured in `agents.yaml`.

## Troubleshooting

### Installation Issues

**Problem: pip install fails**
```bash
# Solution: Update pip
python -m pip install --upgrade pip

# Try again
pip install -e .
```

**Problem: Missing dependencies**
```bash
# Solution: Install dependencies manually
pip install yfinance pandas numpy agno mcp httpx uvicorn python-dotenv
```

### Runtime Issues

**Problem: Port already in use**
```bash
# Solution: Change port in .env
INVESTMENT_MCP_PORT=8005  # Use different port
INVESTMENT_AGENT_PORT=7675
```

**Problem: Can't connect to MCP server**
```bash
# Solution 1: Start MCP server separately
investment-mcp

# Then in another terminal:
investment-agent

# Solution 2: Use direct mode (edit run_agent.py)
# Change: use_mcp=False
```

**Problem: No stock data**
```bash
# Solution: Check internet connection
# Verify yfinance is working:
python -c "import yfinance as yf; print(yf.Ticker('AAPL').info['currentPrice'])"
```

**Problem: API key errors**
```bash
# Solution: Set API key in .env
echo "OPENAI_API_KEY=your_key_here" >> .env  # Linux/Mac
echo OPENAI_API_KEY=your_key_here >> .env    # Windows
```

### Hub Integration Issues

**Problem: Plugin not found**
```bash
# Solution: Reinstall agent
cd egile-agent-investment
pip uninstall egile-agent-investment
pip install -e .

# Verify entry points
pip show -v egile-agent-investment | grep "Entry-points"
```

**Problem: Hub doesn't start investment agent**
```bash
# Solution: Check agents.yaml
# Ensure investment is listed and plugin_type is correct

# Check hub logs for errors
agent-hub  # Look for plugin loading messages
```

## Upgrading

To upgrade to a newer version:

```bash
# Update MCP server
cd egile-mcp-investment
git pull  # if using git
pip install -e . --upgrade

# Update agent
cd egile-agent-investment
git pull  # if using git
pip install -e . --upgrade
```

## Uninstalling

```bash
pip uninstall egile-agent-investment
pip uninstall egile-mcp-investment
```

## Next Steps

After installation:

1. **Read the documentation:**
   - [README.md](README.md) - User guide
   - [QUICKREF.md](QUICKREF.md) - Quick reference
   - [ARCHITECTURE.md](ARCHITECTURE.md) - Technical details

2. **Try the example:**
   ```bash
   cd egile-agent-investment
   python example.py
   ```

3. **Start the agent:**
   ```bash
   investment
   ```
   Open `http://localhost:7674`

4. **Add some stocks:**
   ```
   Add AAPL to my portfolio, 10 shares at $150
   Show me my portfolio
   ```

5. **Explore features:**
   - Analyze stocks
   - Get sell recommendations
   - Find buy opportunities
   - Generate reports

## Getting Help

- Check [README.md](README.md) for detailed usage
- Review [QUICKREF.md](QUICKREF.md) for common tasks
- See [HUB_INTEGRATION.md](HUB_INTEGRATION.md) for hub usage
- Read troubleshooting section above

## Support

For issues or questions:
1. Check the documentation
2. Review error messages carefully
3. Check internet connection for stock data
4. Verify API keys are set correctly

---

**Happy Investing! 📈**

Remember: This tool is for informational purposes only. Not financial advice.

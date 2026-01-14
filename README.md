# Egile Investment Agent

AI-powered investment monitoring and analysis agent that helps you track your portfolio, analyze stocks, and discover investment opportunities.

## Features

- 📊 **Portfolio Monitoring**: Track your stock holdings with real-time values and profit/loss calculations
- 📈 **Stock Analysis**: Comprehensive analysis including valuation metrics, technical indicators, and analyst recommendations
- 🎯 **Sell Recommendations**: Data-driven sell signals based on technical analysis, valuation, and performance
- 💡 **Buy Opportunities**: Discover potential investment opportunities based on customizable criteria
- 📋 **Portfolio Reports**: Generate detailed reports with summaries and actionable recommendations
- 🤖 **Conversational Interface**: Interact with your investment data through natural language

## Installation

### Quick Install

**Windows:**
```bash
install.bat
```

**Linux/Mac:**
```bash
chmod +x install.sh
./install.sh
```

### Manual Installation

1. Install the MCP server:
```bash
cd egile-mcp-investment
pip install -e .
```

2. Install the agent:
```bash
cd egile-agent-investment
pip install -e .
```

## Usage

### Start the Agent

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

The web interface will be available at `http://localhost:7674`

### Command Line Options

Run different components separately:

- **Full system** (MCP + Agent): `investment`
- **MCP server only**: `investment-mcp`
- **Agent only**: `investment-agent`

### Configuration

Set environment variables to customize ports:

```bash
# MCP server port (default: 8004)
export INVESTMENT_MCP_PORT=8004

# Agent web UI port (default: 7674)
export INVESTMENT_AGENT_PORT=7674
```

## Example Usage

### Adding Stocks to Portfolio

```
You: Add AAPL to my portfolio, 10 shares at $150
Agent: Added AAPL (Apple Inc.) to portfolio: 10 shares at $150.00
```

### Viewing Portfolio

```
You: Show me my portfolio
Agent: 📊 Current Portfolio

AAPL - Apple Inc.
  • Shares: 10
  • Purchase Price: $150.00
  • Current Price: $175.50
  • Current Value: $1,755.00
  • Profit/Loss: $255.00 (+17.00%)

Total Portfolio Value: $1,755.00
Total Profit/Loss: $255.00 (+17.00%)
```

### Analyzing Stocks

```
You: Analyze Tesla stock
Agent: 📈 Analysis: TSLA - Tesla, Inc.

Sector: Consumer Cyclical | Industry: Auto Manufacturers

Price Information:
  • Current Price: $242.50
  • 52-Week High: $299.29
  • 52-Week Low: $138.80
  • 1-Month Change: +8.5%
  • 3-Month Change: +22.3%

Valuation Metrics:
  • P/E Ratio: 76.42
  • Forward P/E: 58.23
  • PEG Ratio: 2.15
...
```

### Getting Sell Recommendations

```
You: Should I sell my AAPL stock?
Agent: 🎯 Sell Analysis: AAPL

Recommendation: HOLD
Sell Score: 1/10

Analysis:
  • Stock is performing well with steady growth
  • Valuation metrics are reasonable
  • No significant sell signals detected
```

### Finding Buy Opportunities

```
You: Find me some tech stocks to buy with good value
Agent: 💡 Buy Opportunities (Found 5 stocks)

1. MSFT - Microsoft Corporation
   Sector: Technology | Price: $378.50
   Buy Score: 7/10
   Reasons:
     • Attractive P/E ratio of 32.5
     • Strong 3-month performance: +15.2%
     • Analyst recommendation: buy
     • Analyst target price implies 12.5% upside

2. GOOGL - Alphabet Inc.
   Sector: Technology | Price: $142.30
   Buy Score: 6/10
...
```

### Generating Portfolio Report

```
You: Generate a portfolio report
Agent: 📊 Portfolio Report

Summary:
  • Total Holdings: 3
  • Total Investment: $5,000.00
  • Current Value: $5,750.00
  • Total P/L: $750.00 (+15.00%)

⚠️ Sell Recommendations (1):

TSLA - SELL
  Sell Score: 6/10
    • High P/E ratio of 76.42 suggests overvaluation
    • High PEG ratio of 2.15 indicates poor value
    • High volatility of 52.3% indicates increased risk
```

## Available Tools

The agent has access to the following tools:

- **add_to_portfolio**: Add stocks to your portfolio
- **get_portfolio**: View current portfolio with real-time values
- **analyze_stock**: Get comprehensive stock analysis
- **should_sell**: Check if you should sell a stock
- **find_buy_opportunities**: Discover potential investments
- **generate_portfolio_report**: Generate detailed portfolio report

## Data Sources

Stock data is provided by Yahoo Finance via the `yfinance` library:
- Real-time and historical price data
- Company fundamentals and valuation metrics
- Analyst recommendations and target prices
- Technical indicators (moving averages, volatility, etc.)

## Integration with Egile Agent Hub

This agent can be integrated into the Egile Agent Hub for multi-agent workflows. See the hub's `agents.yaml` for configuration.

## Customization

### Modify Analysis Criteria

Edit the scoring logic in [`investment_service.py`](egile-mcp-investment/src/egile_mcp_investment/investment_service.py):
- Adjust sell score thresholds in `should_sell()`
- Customize buy score criteria in `find_buy_opportunities()`
- Add new technical indicators or metrics

### Change Agent Instructions

Modify the agent's behavior in [`run_agent.py`](src/egile_agent_investment/run_agent.py) by updating the `instructions` list.

## Troubleshooting

### Connection Issues

If the agent can't connect to the MCP server:
1. Ensure port 8004 is not in use
2. Check firewall settings
3. Try running MCP server separately: `investment-mcp`

### Data Issues

If stock data is not loading:
1. Check internet connection
2. Verify ticker symbols are correct
3. Some stocks may not have all metrics available

## Development

### Project Structure

```
egile-mcp-investment/          # MCP server
  src/egile_mcp_investment/
    server.py                   # MCP server implementation
    investment_service.py       # Core analysis logic

egile-agent-investment/         # Agent wrapper
  src/egile_agent_investment/
    plugin.py                   # Plugin interface
    run_agent.py                # Agent runner
    run_mcp.py                  # MCP server runner
    run_server.py               # Combined runner
```

### Running Tests

```bash
pytest tests/
```

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit pull requests.

## Disclaimer

⚠️ **Important**: This tool is for informational purposes only and does not constitute financial advice. Always do your own research and consult with a qualified financial advisor before making investment decisions. Past performance does not guarantee future results.

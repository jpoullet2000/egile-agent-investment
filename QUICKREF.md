# Quick Reference - Investment Agent

## Installation

```bash
# Windows
install.bat

# Linux/Mac
chmod +x install.sh && ./install.sh
```

## Starting the Agent

```bash
# Full system
investment

# Or use start scripts
start.bat  # Windows
./start.sh # Linux/Mac
```

Access web UI at: `http://localhost:7674`

## Common Commands

### Portfolio Management

```
Add AAPL to my portfolio, 10 shares at $150
Show my portfolio
What's my portfolio worth?
```

### Stock Analysis

```
Analyze Apple stock
Tell me about Microsoft's performance
Compare AAPL and MSFT
```

### Sell Decisions

```
Should I sell TSLA?
Which of my stocks should I consider selling?
Analyze my portfolio for sell opportunities
```

### Buy Opportunities

```
Find tech stocks to buy
Show me undervalued stocks
Find stocks with good dividends
Find growth stocks in healthcare
```

### Reports

```
Generate a portfolio report
Show me my profit and loss
Summarize my investments
```

## Tool Reference

| Tool | Purpose | Example |
|------|---------|---------|
| `add_to_portfolio` | Track a stock | Add 10 shares of AAPL at $150 |
| `get_portfolio` | View holdings | Show my portfolio |
| `analyze_stock` | Stock details | Analyze TSLA |
| `should_sell` | Sell signals | Should I sell AAPL? |
| `find_buy_opportunities` | Find stocks | Find tech stocks to buy |
| `generate_portfolio_report` | Full report | Generate portfolio report |

## Configuration

Environment variables:
```bash
INVESTMENT_MCP_PORT=8004        # MCP server port
INVESTMENT_AGENT_PORT=7674      # Web UI port
```

## Scoring Metrics

### Sell Score (0-10)
- **0-1**: Strong Hold
- **2-3**: Hold/Monitor
- **4-5**: Consider Selling
- **6+**: Strong Sell Signal

### Buy Score (0-10)
- **0-2**: Avoid
- **3-4**: Weak Interest
- **5-6**: Moderate Opportunity
- **7+**: Strong Buy Candidate

## Stock Analysis Metrics

- **P/E Ratio**: Price-to-earnings (lower often better for value)
- **PEG Ratio**: P/E to growth (< 1 is good)
- **Beta**: Volatility vs market (> 1 is more volatile)
- **Dividend Yield**: Annual dividend as % of price
- **Moving Averages**: 50-day and 200-day trends
- **Volatility**: Annualized price fluctuation

## Hub Integration

Add to `egile-agent-hub/agents.yaml`:

```yaml
agents:
  - name: investment
    description: "Monitor portfolios and analyze stocks"
    plugin_type: investment
    mcp_port: 8004
    instructions:
      - "You are a professional investment advisor."
      - "Provide data-driven recommendations."
      - "Always explain the reasoning behind suggestions."
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port already in use | Change INVESTMENT_MCP_PORT or INVESTMENT_AGENT_PORT |
| Can't find stock | Verify ticker symbol (use Yahoo Finance tickers) |
| No data for stock | Stock may be delisted or data unavailable |
| Connection error | Check internet connection and firewall |

## Disclaimer

⚠️ Not financial advice. Do your own research and consult professionals before investing.

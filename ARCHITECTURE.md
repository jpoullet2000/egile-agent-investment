# Investment Agent Architecture

## Overview

The Investment Agent is a conversational AI agent that provides stock portfolio monitoring, analysis, and investment recommendations. It follows the Egile Agent framework pattern with MCP (Model Context Protocol) integration.

## Architecture Components

### 1. MCP Server (`egile-mcp-investment`)

The MCP server provides the core investment analysis functionality.

**Components:**
- `investment_service.py`: Core business logic for portfolio and stock analysis
- `server.py`: MCP server implementation with tool definitions
- `portfolio_utils.py`: CSV import/export utilities

**Key Features:**
- Portfolio tracking with real-time pricing
- Comprehensive stock analysis (fundamental + technical)
- Sell signal detection with scoring
- Buy opportunity screening
- Portfolio report generation

**Data Source:**
- Yahoo Finance via `yfinance` library
- Real-time prices, fundamentals, analyst data

### 2. Agent Plugin (`egile-agent-investment`)

The agent plugin wraps the MCP server for use with Agno/Egile Agent Core.

**Components:**
- `plugin.py`: Plugin interface implementing Egile Agent Core Plugin protocol
- `mcp_client.py`: Client for communicating with MCP server
- `run_agent.py`: Standalone agent runner with web UI
- `run_mcp.py`: Standalone MCP server runner
- `run_server.py`: Combined runner (MCP + Agent)

**Modes:**
- **MCP Mode**: Agent communicates with MCP server (production)
- **Direct Mode**: Agent uses service directly (development/testing)

### 3. Integration Points

#### Hub Integration
- Automatically discovered by Egile Agent Hub via entry points
- Configured in `agents.yaml` with `plugin_type: investment`
- MCP server managed by hub lifecycle

#### Standalone Usage
- Can run independently with web UI
- Interactive portfolio management
- Conversational stock analysis

## Data Flow

```
User Query
    ↓
Agno Agent
    ↓
Investment Plugin
    ↓
MCP Client (if MCP mode) ──→ MCP Server
    ↓                            ↓
Investment Service ←────────────┘
    ↓
Yahoo Finance (yfinance)
    ↓
Analysis Results
    ↓
User Response
```

## Tool Architecture

### Portfolio Management
- `add_to_portfolio`: Track stocks
- `get_portfolio`: View holdings with P/L
- `generate_portfolio_report`: Comprehensive reports

### Stock Analysis
- `analyze_stock`: Full fundamental + technical analysis
- `should_sell`: Sell signal detection with reasoning
- `find_buy_opportunities`: Opportunity screening

## Analysis Algorithms

### Sell Scoring (0-10)
Factors weighted:
1. **Profit/Loss**: -20% loss (+3), +50% gain (+2)
2. **Technical**: Death cross pattern (+2)
3. **Valuation**: High P/E > 40 (+1), High PEG > 2 (+1)
4. **Performance**: 1-month drop > 15% (+2)
5. **Volatility**: > 50% annualized (+1)
6. **Analysts**: Sell/strong sell rating (+2)

**Thresholds:**
- 5+: Strong Sell
- 3-4: Sell
- 1-2: Hold/Monitor
- 0: Hold

### Buy Scoring (0-10)
Factors weighted:
1. **Valuation**: P/E < 20 (+2), PEG < 1 (+2)
2. **Momentum**: 3-month gain > 10% (+1)
3. **Dividend**: Yield > 2% (+1)
4. **Analysts**: Buy/strong buy (+2)
5. **Target Price**: > 15% upside (+2)

**Threshold:** 3+ for inclusion in opportunities

### Technical Indicators
- **Moving Averages**: 50-day, 200-day
- **Death Cross**: 50-MA crosses below 200-MA (bearish)
- **Golden Cross**: 50-MA crosses above 200-MA (bullish)
- **Volatility**: Annualized standard deviation of returns
- **Beta**: Sensitivity to market movements

## Configuration

### Environment Variables
```
INVESTMENT_MCP_PORT=8004
INVESTMENT_AGENT_PORT=7674
OPENAI_API_KEY=...
```

### Portfolio Files
- CSV format: `ticker,shares,purchase_price`
- Auto-load from `portfolio.csv` (optional)
- Save/export functionality

### Agent Instructions
Customizable via `agents.yaml` or agent initialization:
- Risk tolerance guidance
- Investment philosophy
- Reporting preferences

## Extensibility

### Adding New Metrics
Extend `investment_service.py`:
```python
def analyze_stock(self, ticker: str):
    # Add new metrics to analysis dict
    analysis['your_metric'] = calculate_metric()
```

### Custom Scoring
Modify scoring logic:
```python
def should_sell(self, ticker: str):
    # Adjust weights or add new factors
    if custom_condition:
        sell_score += weight
        reasons.append("Custom reason")
```

### New Data Sources
Replace or supplement yfinance:
```python
# Add alternative data provider
from alternative_provider import get_data

def analyze_stock(self, ticker: str):
    # Combine multiple sources
    yf_data = yf.Ticker(ticker).info
    alt_data = get_data(ticker)
```

## Deployment

### Development
```bash
cd egile-agent-investment
pip install -e .
investment
```

### Production (via Hub)
```bash
cd egile-agent-hub
pip install -e .
agent-hub  # Starts all configured agents including investment
```

### Docker (Future)
```dockerfile
FROM python:3.10
COPY . /app
RUN pip install -e /app/egile-mcp-investment
RUN pip install -e /app/egile-agent-investment
CMD ["investment"]
```

## Security Considerations

1. **API Keys**: Never commit keys, use environment variables
2. **Data Privacy**: Portfolio data stored in memory only (not persisted)
3. **Rate Limits**: Yahoo Finance has rate limits, implement caching if needed
4. **Validation**: All user inputs validated before processing

## Performance

### Optimizations
- Caching of stock data (avoid repeated API calls)
- Batch processing for portfolio analysis
- Async operations for parallel stock fetches

### Scalability
- Stateless service design (easy horizontal scaling)
- MCP protocol supports multiple clients
- Hub can manage multiple agent instances

## Testing Strategy

### Unit Tests
- Test analysis algorithms with mock data
- Validate scoring calculations
- Test CSV import/export

### Integration Tests
- Test MCP server tool calls
- Test plugin initialization
- Test Yahoo Finance integration

### End-to-End Tests
- Full workflow testing via agent
- Multi-turn conversations
- Error handling scenarios

## Future Enhancements

1. **Persistent Portfolio**: Database storage for portfolios
2. **Alerts**: Email/SMS alerts for sell signals
3. **Backtesting**: Historical performance analysis
4. **Advanced Charts**: Integration with plotting libraries
5. **Options Analysis**: Support for options strategies
6. **Crypto Support**: Extend to cryptocurrency tracking
7. **News Integration**: Sentiment analysis from news sources
8. **Machine Learning**: Predictive models for price movements

## Dependencies

### Core
- `egile-agent-core`: Agent framework
- `agno`: Multi-agent orchestration
- `mcp`: Model Context Protocol

### Data & Analysis
- `yfinance`: Stock data
- `pandas`: Data manipulation
- `numpy`: Numerical operations

### Infrastructure
- `httpx`: HTTP client
- `uvicorn`: ASGI server
- `python-dotenv`: Environment management

## License

MIT License - See LICENSE file for details.

## Disclaimer

This software is for informational purposes only and does not constitute financial advice. Users should conduct their own research and consult with qualified financial advisors before making investment decisions.

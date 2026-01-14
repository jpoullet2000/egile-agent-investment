# Hub Integration Guide

## Adding Investment Agent to Egile Agent Hub

The Investment agent can be integrated into the Egile Agent Hub for multi-agent workflows.

### Configuration

Add to your `agents.yaml`:

```yaml
agents:
  - name: investment
    description: "Monitor investment portfolios and provide stock analysis"
    plugin_type: investment
    mcp_port: 8004
    instructions:
      - "You are a professional investment advisor."
      - "Provide data-driven recommendations based on market analysis."
      - "Always explain your reasoning clearly."
      - "Remind users this is informational only, not financial advice."
```

### Team Examples

#### Financial Planning Team
Combine investment analysis with other capabilities:

```yaml
teams:
  - name: financial-planning
    description: "Comprehensive financial planning and reporting"
    members:
      - investment
      - slidedeck
    instructions:
      - "Analyze investment portfolio and create presentation."
      - "Use investment agent for analysis, slidedeck for reports."
      - "Create professional investor presentations."
```

#### Market Research Team
Combine with prospect finder for company research:

```yaml
teams:
  - name: market-research
    description: "Research companies and analyze investment potential"
    members:
      - prospectfinder
      - investment
    instructions:
      - "Research companies and analyze as investment opportunities."
      - "Use prospectfinder to discover companies."
      - "Use investment agent to analyze stock potential."
```

### Installation with Hub

1. Install both the hub and investment agent:
```bash
cd egile-agent-hub
pip install -e .

cd ../egile-agent-investment
./install.bat  # or ./install.sh
```

2. The hub will automatically discover the investment plugin

3. Start the hub:
```bash
cd egile-agent-hub
agent-hub
```

### Plugin Discovery

The hub automatically discovers installed egile plugins. The investment agent registers as:
- **Plugin Type**: `investment`
- **Package**: `egile-agent-investment`
- **Entry Point**: `egile_agent_investment:InvestmentPlugin`

### MCP Server Management

When running through the hub:
- MCP server starts automatically on the configured port
- Port can be customized in `agents.yaml` via `mcp_port`
- Server stops when hub shuts down

### Workflow Examples

#### Portfolio Review Workflow
```
User: Analyze my portfolio and create a presentation for my review meeting

Hub: 
1. Uses investment agent to generate portfolio report
2. Uses slidedeck agent to create presentation
3. Returns complete analysis deck
```

#### Company Investment Analysis
```
User: Research fintech companies and tell me which ones are good investments

Hub:
1. Uses prospectfinder to discover fintech companies
2. Uses investment agent to analyze public ones as stocks
3. Returns ranked investment opportunities
```

## Direct Integration (Without Hub)

You can also use the investment agent directly:

```python
from egile_agent_investment.plugin import InvestmentPlugin
from agno import Agent

# Create plugin
plugin = InvestmentPlugin(mcp_port=8004)

# Create agent
agent = Agent(
    name="Investment Advisor",
    plugins=[plugin],
    instructions=[
        "You are a professional investment advisor.",
        "Provide clear, data-driven recommendations."
    ]
)

# Use the agent
response = await agent.run("Show me my portfolio")
```

## Configuration Options

### Agent Configuration
```yaml
- name: investment
  description: "Portfolio monitoring and stock analysis"
  plugin_type: investment
  
  # MCP Server settings
  mcp_port: 8004              # Port for MCP server
  mcp_host: localhost         # Host for MCP server
  
  # Model override (optional)
  model_override:
    provider: openai
    model: gpt-4
  
  # Custom instructions
  instructions:
    - "Custom instruction 1"
    - "Custom instruction 2"
```

### Plugin Settings
The plugin supports these initialization parameters:
- `mcp_port`: MCP server port (default: 8004)
- `mcp_host`: MCP server host (default: localhost)
- `mcp_transport`: Transport mode, "stdio" or "sse" (default: sse)
- `use_mcp`: Use MCP client or direct service (default: True)
- `timeout`: Request timeout in seconds (default: 30)

## Troubleshooting

### Plugin Not Found
If hub can't find the investment plugin:
1. Ensure it's installed: `pip show egile-agent-investment`
2. Check entry points: `pip show -v egile-agent-investment`
3. Reinstall: `pip install -e .` from agent directory

### MCP Server Won't Start
1. Check port availability: `netstat -an | findstr 8004`
2. Try different port in `agents.yaml`
3. Check MCP package: `pip show egile-mcp-investment`

### Tools Not Available
If agent can't access tools:
1. Verify MCP server is running
2. Check plugin initialization in logs
3. Try direct mode: set `use_mcp: false` in config

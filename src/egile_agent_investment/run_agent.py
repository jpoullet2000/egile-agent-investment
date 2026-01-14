"""Run only the Agno agent with web interface."""

import asyncio
import logging
import os
import sys

from agno import Agent, AgentUI
from egile_agent_investment.plugin import InvestmentPlugin

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main():
    """Run the Investment agent with web UI."""
    
    # Get configuration from environment
    mcp_port = int(os.getenv("INVESTMENT_MCP_PORT", "8004"))
    agent_port = int(os.getenv("INVESTMENT_AGENT_PORT", "7674"))
    
    # Create the investment plugin
    plugin = InvestmentPlugin(
        mcp_port=mcp_port,
        use_mcp=True,
    )
    
    # Create the agent
    agent = Agent(
        name="Investment Advisor",
        description="Monitor investments, analyze stocks, and provide buy/sell recommendations",
        instructions=[
            "You are a professional investment advisor and portfolio manager.",
            "You help users monitor their investment portfolios and make informed decisions.",
            "WORKFLOW: Users can add stocks to their portfolio, analyze individual stocks, and get recommendations.",
            "PORTFOLIO MANAGEMENT: Use add_to_portfolio to track stocks, get_portfolio to view holdings.",
            "ANALYSIS: Use analyze_stock for detailed stock analysis, should_sell for sell recommendations.",
            "OPPORTUNITIES: Use find_buy_opportunities to discover new investment opportunities.",
            "REPORTS: Use generate_portfolio_report for comprehensive portfolio summaries.",
            "Always provide clear explanations for your recommendations based on data.",
            "When analyzing stocks, consider valuation metrics, technical indicators, and analyst recommendations.",
            "Be conservative with sell recommendations - explain the reasoning clearly.",
            "For buy opportunities, highlight both potential and risks.",
        ],
        model="gpt-4",
        plugins=[plugin],
        show_tool_calls=True,
        markdown=True,
    )
    
    # Start the agent with UI
    logger.info(f"Starting Investment agent on port {agent_port}...")
    
    agent_ui = AgentUI(agent=agent)
    await agent_ui.start(port=agent_port)


def run_agent_only():
    """Entry point for running only the agent."""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down Investment agent...")
    except Exception as e:
        logger.error(f"Error running Investment agent: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run_agent_only()

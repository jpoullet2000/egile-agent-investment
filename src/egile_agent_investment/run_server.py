"""Run both MCP server and Agno agent."""

import asyncio
import logging
import os
import sys
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def run_mcp_server():
    """Run the MCP server."""
    from egile_mcp_investment.server import main as mcp_main
    logger.info("Starting Investment MCP server...")
    await mcp_main()


async def run_agent_server():
    """Run the Agno agent with web interface."""
    from egile_agent_investment.run_agent import main as agent_main
    logger.info("Starting Investment agent...")
    await agent_main()


async def run_all_async():
    """Run both MCP server and agent concurrently."""
    logger.info("Starting Investment system (MCP + Agent)...")
    
    # Run both servers concurrently
    await asyncio.gather(
        run_mcp_server(),
        run_agent_server(),
    )


def run_all():
    """Entry point for running both servers."""
    try:
        asyncio.run(run_all_async())
    except KeyboardInterrupt:
        logger.info("Shutting down Investment system...")
    except Exception as e:
        logger.error(f"Error running Investment system: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run_all()

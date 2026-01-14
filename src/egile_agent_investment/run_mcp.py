"""Run only the MCP server."""

import asyncio
import logging
import sys

from egile_mcp_investment.server import main

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def run_mcp_only():
    """Entry point for running only the MCP server."""
    try:
        logger.info("Starting Investment MCP server (standalone mode)...")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down Investment MCP server...")
    except Exception as e:
        logger.error(f"Error running Investment MCP server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run_mcp_only()

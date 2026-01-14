"""MCP client for investment service."""

from __future__ import annotations

import asyncio
import logging
from typing import Any, Dict, List, Optional

import httpx

logger = logging.getLogger(__name__)


class InvestmentMCPClient:
    """Client for communicating with the Investment MCP server."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 8004,
        transport: str = "sse",
        command: Optional[str] = None,
        timeout: float = 30.0,
    ):
        """
        Initialize the MCP client.

        Args:
            host: MCP server host
            port: MCP server port
            transport: Transport mode ("stdio" or "sse")
            command: Command to start MCP server (for stdio)
            timeout: Request timeout in seconds
        """
        self.host = host
        self.port = port
        self.transport = transport
        self.command = command
        self.timeout = timeout
        self.base_url = f"http://{host}:{port}"
        self._client: Optional[httpx.AsyncClient] = None
        self._process: Optional[asyncio.subprocess.Process] = None

    async def connect(self) -> None:
        """Connect to the MCP server."""
        if self.transport == "sse":
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=self.timeout,
            )
            logger.info(f"Connected to Investment MCP server at {self.base_url}")
        elif self.transport == "stdio":
            if not self.command:
                raise ValueError("Command required for stdio transport")
            
            # Start the MCP server process
            self._process = await asyncio.create_subprocess_shell(
                self.command,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            logger.info(f"Started Investment MCP server process")
        else:
            raise ValueError(f"Unsupported transport: {self.transport}")

    async def disconnect(self) -> None:
        """Disconnect from the MCP server."""
        if self._client:
            await self._client.aclose()
            self._client = None
        
        if self._process:
            self._process.terminate()
            await self._process.wait()
            self._process = None

    async def list_tools(self) -> List[Dict[str, Any]]:
        """List available tools from the MCP server."""
        if self.transport == "sse":
            response = await self._client.get("/tools")
            response.raise_for_status()
            return response.json()
        else:
            # For stdio, tools are predefined
            return [
                {
                    "name": "add_to_portfolio",
                    "description": "Add a stock to your portfolio",
                    "parameters": {
                        "ticker": {"type": "string", "required": True},
                        "shares": {"type": "number", "required": True},
                        "purchase_price": {"type": "number", "required": False},
                    }
                },
                {
                    "name": "get_portfolio",
                    "description": "Get current portfolio",
                    "parameters": {}
                },
                {
                    "name": "analyze_stock",
                    "description": "Analyze a stock",
                    "parameters": {
                        "ticker": {"type": "string", "required": True}
                    }
                },
                {
                    "name": "should_sell",
                    "description": "Check if you should sell a stock",
                    "parameters": {
                        "ticker": {"type": "string", "required": True}
                    }
                },
                {
                    "name": "find_buy_opportunities",
                    "description": "Find stocks to buy",
                    "parameters": {}
                },
                {
                    "name": "generate_portfolio_report",
                    "description": "Generate portfolio report",
                    "parameters": {}
                }
            ]

    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """
        Call a tool on the MCP server.

        Args:
            name: Tool name
            arguments: Tool arguments

        Returns:
            Tool result
        """
        if self.transport == "sse":
            response = await self._client.post(
                "/call-tool",
                json={"name": name, "arguments": arguments}
            )
            response.raise_for_status()
            return response.json()
        else:
            # For stdio, send JSON-RPC message
            raise NotImplementedError("stdio transport not yet implemented")

"""Egile Agent Investment - Conversational investment monitoring and analysis agent."""

__version__ = "0.1.0"

from egile_agent_investment.plugin import InvestmentPlugin
from egile_agent_investment.run_server import run_all

__all__ = ["InvestmentPlugin", "run_all"]

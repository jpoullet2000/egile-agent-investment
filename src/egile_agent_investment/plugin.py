"""Investment plugin for Egile Agent Core."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Optional

from egile_agent_core.plugins import Plugin

if TYPE_CHECKING:
    from egile_agent_core.agent import Agent

logger = logging.getLogger(__name__)


class InvestmentPlugin(Plugin):
    """
    Plugin that provides investment monitoring and analysis capabilities.
    
    This plugin integrates with the egile-mcp-investment MCP server to enable
    AI agents to monitor portfolios, analyze stocks, and provide buy/sell recommendations.
    """

    def __init__(
        self,
        mcp_host: str = "localhost",
        mcp_port: int = 8004,
        mcp_transport: str = "sse",
        mcp_command: Optional[str] = None,
        timeout: float = 30.0,
        use_mcp: bool = True,
    ):
        """
        Initialize the Investment plugin.

        Args:
            mcp_host: Host where the MCP server is running
            mcp_port: Port where the MCP server is running
            mcp_transport: Transport mode - "stdio" or "sse"
            mcp_command: Command to start MCP server (for stdio transport)
            timeout: Request timeout in seconds
            use_mcp: If True, use MCP client; if False, use direct service
        """
        self.mcp_host = mcp_host
        self.mcp_port = mcp_port
        self.mcp_transport = mcp_transport
        self.mcp_command = mcp_command or "python -m egile_mcp_investment.server"
        self.timeout = timeout
        self.use_mcp = use_mcp
        self._client: Optional[Any] = None
        self._investment_service = None
        self._agent: Optional[Agent] = None

    @property
    def name(self) -> str:
        """Plugin name for registration."""
        return "investment"

    @property
    def description(self) -> str:
        """Plugin description."""
        return (
            "Monitors investment portfolios, analyzes stocks, and provides buy/sell recommendations. "
            "Tracks stock performance, valuation metrics, and generates comprehensive reports."
        )

    @property
    def version(self) -> str:
        """Plugin version."""
        return "0.1.0"

    @property
    def mcp_server_module(self) -> str:
        """MCP server module path."""
        return "egile_mcp_investment.server"

    async def on_agent_start(self, agent: Agent) -> None:
        """Called when the agent starts."""
        self._agent = agent
        
        if self.use_mcp:
            # Use MCP client
            from egile_agent_investment.mcp_client import InvestmentMCPClient
            
            self._client = InvestmentMCPClient(
                host=self.mcp_host,
                port=self.mcp_port,
                transport=self.mcp_transport,
                command=self.mcp_command,
                timeout=self.timeout,
            )
            
            await self._client.connect()
            logger.info(f"Investment MCP client connected on port {self.mcp_port}")
        else:
            # Use direct service
            from egile_mcp_investment.investment_service import InvestmentService
            
            self._investment_service = InvestmentService()
            logger.info("Investment service initialized (direct mode)")

    async def on_agent_stop(self, agent: Agent) -> None:
        """Called when the agent stops."""
        if self._client:
            await self._client.disconnect()
            logger.info("Investment MCP client disconnected")

    def get_tool_functions(self) -> dict:
        """
        Get tool functions for the agent.
        
        Returns:
            Dictionary mapping tool names to tool functions
        """
        if self.use_mcp:
            # MCP mode - tools will be provided via MCP client
            return {}
        else:
            # Direct mode - provide service methods as tools
            return {
                "add_to_portfolio": self._add_to_portfolio,
                "get_portfolio": self._get_portfolio,
                "analyze_stock": self._analyze_stock,
                "should_sell": self._should_sell,
                "find_buy_opportunities": self._find_buy_opportunities,
                "generate_portfolio_report": self._generate_portfolio_report,
                "format_portfolio_as_markdown": self._format_portfolio_as_markdown,
            }

    async def _add_to_portfolio(self, ticker: str, shares: float, purchase_price: Optional[float] = None):
        """Add a stock to the portfolio."""
        result = self._investment_service.add_to_portfolio(ticker, shares, purchase_price)
        return f"Added {result['ticker']} ({result['company_name']}) to portfolio: {result['shares']} shares at ${result['purchase_price']:.2f}"
    
    async def _get_portfolio(self):
        """Get current portfolio with real-time values."""
        result = self._investment_service.get_portfolio()
        if not result:
            return "Portfolio is empty."
        
        output = "📊 **Current Portfolio**\n\n"
        total_value = 0
        total_cost = 0
        
        for holding in result:
            output += f"**{holding['ticker']}** - {holding['company_name']}\n"
            output += f"  • Shares: {holding['shares']}\n"
            output += f"  • Purchase Price: ${holding['purchase_price']:.2f}\n"
            output += f"  • Current Price: ${holding['current_price']:.2f}\n"
            output += f"  • Current Value: ${holding['current_value']:,.2f}\n"
            output += f"  • Profit/Loss: ${holding['profit_loss']:,.2f} ({holding['profit_loss_pct']:+.2f}%)\n\n"
            total_value += holding['current_value']
            total_cost += holding['purchase_value']
        
        total_pl = total_value - total_cost
        total_pl_pct = (total_pl / total_cost * 100) if total_cost > 0 else 0
        output += f"**Total Portfolio Value:** ${total_value:,.2f}\n"
        output += f"**Total Profit/Loss:** ${total_pl:,.2f} ({total_pl_pct:+.2f}%)"
        
        return output
    
    async def _analyze_stock(self, ticker: str):
        """Analyze a stock comprehensively."""
        result = self._investment_service.analyze_stock(ticker)
        
        output = f"📈 **Analysis: {result['ticker']} - {result['company_name']}**\n\n"
        output += f"**Sector:** {result['sector']} | **Industry:** {result['industry']}\n\n"
        output += f"**Price Information:**\n"
        output += f"  • Current Price: ${result['current_price']:.2f}\n"
        output += f"  • 52-Week High: ${result['price_52w_high']:.2f}\n"
        output += f"  • 52-Week Low: ${result['price_52w_low']:.2f}\n"
        output += f"  • 1-Month Change: {result['change_1m_pct']:+.2f}%\n"
        output += f"  • 3-Month Change: {result['change_3m_pct']:+.2f}%\n\n"
        
        output += f"**Valuation Metrics:**\n"
        output += f"  • Market Cap: ${result['market_cap']:,.0f}\n"
        pe_ratio_str = f"{result['pe_ratio']:.2f}" if result['pe_ratio'] is not None else 'N/A'
        fwd_pe_str = f"{result['forward_pe']:.2f}" if result['forward_pe'] is not None else 'N/A'
        peg_ratio_str = f"{result['peg_ratio']:.2f}" if result['peg_ratio'] is not None else 'N/A'
        ptb_str = f"{result['price_to_book']:.2f}" if result['price_to_book'] is not None else 'N/A'
        output += f"  • P/E Ratio: {pe_ratio_str}\n"
        output += f"  • Forward P/E: {fwd_pe_str}\n"
        output += f"  • PEG Ratio: {peg_ratio_str}\n"
        output += f"  • Price/Book: {ptb_str}\n"
        output += f"  • Dividend Yield: {result['dividend_yield']:.2f}%\n\n"
        
        output += f"**Technical Indicators:**\n"
        ma_50_str = f"${result['moving_avg_50d']:.2f}" if result['moving_avg_50d'] is not None else 'N/A'
        ma_200_str = f"${result['moving_avg_200d']:.2f}" if result['moving_avg_200d'] is not None else 'N/A'
        beta_str = f"{result['beta']:.2f}" if result['beta'] is not None else 'N/A'
        output += f"  • 50-Day MA: {ma_50_str}\n"
        output += f"  • 200-Day MA: {ma_200_str}\n"
        output += f"  • Volatility: {result['volatility']:.2f}%\n"
        output += f"  • Beta: {beta_str}\n\n"
        
        output += f"**Analyst Data:**\n"
        output += f"  • Recommendation: {result['analyst_recommendation'].upper()}\n"
        target_price_str = f"${result['target_price']:.2f}" if result['target_price'] is not None else 'N/A'
        output += f"  • Target Price: {target_price_str}\n"
        
        return output
    
    async def _should_sell(self, ticker: str):
        """Determine if a stock should be sold."""
        result = self._investment_service.should_sell(ticker)
        
        output = f"🎯 **Sell Analysis: {result['ticker']}**\n\n"
        output += f"**Recommendation: {result['recommendation']}**\n"
        output += f"**Sell Score: {result['sell_score']}/10**\n\n"
        output += f"**Analysis:**\n"
        for reason in result['reasons']:
            output += f"  • {reason}\n"
        
        return output
    
    async def _find_buy_opportunities(
        self,
        sectors: Optional[list] = None,
        min_market_cap: float = 1e9,
        max_pe: Optional[float] = 25,
        min_dividend_yield: float = 0,
        limit: int = 10
    ):
        """Find potential stocks to buy."""
        result = self._investment_service.find_buy_opportunities(
            sectors, min_market_cap, max_pe, min_dividend_yield, limit
        )
        
        if not result:
            return "No buy opportunities found matching your criteria."
        
        output = f"💡 **Buy Opportunities** (Found {len(result)} stocks)\n\n"
        
        for i, opp in enumerate(result, 1):
            output += f"**{i}. {opp['ticker']}** - {opp['company_name']}\n"
            output += f"   Sector: {opp['sector']} | Price: ${opp['current_price']:.2f}\n"
            output += f"   Buy Score: {opp['buy_score']}/10\n"
            output += f"   **Reasons:**\n"
            for reason in opp['reasons']:
                output += f"     • {reason}\n"
            output += "\n"
        
        return output
    
    async def _generate_portfolio_report(self):
        """Generate comprehensive portfolio report."""
        result = self._investment_service.generate_portfolio_report()
        
        if result['status'] == 'empty':
            return result['message']
        
        output = f"📊 **Portfolio Report**\n\n"
        output += f"**Summary:**\n"
        output += f"  • Total Holdings: {result['holdings_count']}\n"
        output += f"  • Total Investment: ${result['total_purchase_value']:,.2f}\n"
        output += f"  • Current Value: ${result['total_current_value']:,.2f}\n"
        output += f"  • Total P/L: ${result['total_profit_loss']:,.2f} ({result['total_profit_loss_pct']:+.2f}%)\n\n"
        
        if result['sell_recommendations']:
            output += f"**⚠️ Sell Recommendations ({len(result['sell_recommendations'])}):**\n\n"
            for rec in result['sell_recommendations']:
                output += f"**{rec['ticker']}** - {rec['recommendation']}\n"
                output += f"  Sell Score: {rec['sell_score']}/10\n"
                for reason in rec['reasons']:
                    output += f"    • {reason}\n"
                output += "\n"
        else:
            output += "✅ No immediate sell recommendations.\n"
        
        return output
    
    async def _format_portfolio_as_markdown(
        self, 
        include_buy_opportunities: bool = False, 
        sectors_for_opportunities: Optional[list] = None
    ):
        """Format portfolio data as markdown suitable for PDF generation."""
        from datetime import datetime
        
        # Get portfolio data
        portfolio = self._investment_service.get_portfolio()
        if not portfolio:
            return "Portfolio is empty. Cannot generate report."
        
        # Build markdown report
        markdown = "# Investment Portfolio Report\n\n"
        markdown += f"*Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}*\n\n"
        
        # Calculate totals
        total_value = sum(h['current_value'] for h in portfolio)
        total_cost = sum(h['purchase_value'] for h in portfolio)
        total_pl = total_value - total_cost
        total_pl_pct = (total_pl / total_cost * 100) if total_cost > 0 else 0
        
        # Summary section
        markdown += "## Portfolio Summary\n\n"
        markdown += f"- **Total Holdings:** {len(portfolio)} stocks\n"
        markdown += f"- **Total Investment:** ${total_cost:,.2f}\n"
        markdown += f"- **Current Value:** ${total_value:,.2f}\n"
        markdown += f"- **Total Profit/Loss:** ${total_pl:,.2f} ({total_pl_pct:+.2f}%)\n\n"
        
        # Holdings section (as list instead of table for PDF compatibility)
        markdown += "## Current Holdings\n\n"
        
        for h in portfolio:
            markdown += f"### {h['ticker']} - {h['company_name']}\n\n"
            markdown += f"- Shares: **{h['shares']}**\n"
            markdown += f"- Purchase Price: **${h['purchase_price']:.2f}**\n"
            markdown += f"- Current Price: **${h['current_price']:.2f}**\n"
            markdown += f"- Current Value: **${h['current_value']:,.2f}**\n"
            markdown += f"- Profit/Loss: **${h['profit_loss']:,.2f}** ({h['profit_loss_pct']:+.2f}%)\n"
            markdown += "\n"
        
        # Sell recommendations
        markdown += "## ⚠️ Sell Recommendations\n\n"
        has_sell_recs = False
        
        for holding in portfolio:
            try:
                sell_analysis = self._investment_service.should_sell(holding['ticker'])
                if sell_analysis['sell_score'] >= 6:  # Only include high-confidence sells
                    has_sell_recs = True
                    markdown += f"### {sell_analysis['ticker']} - {sell_analysis['recommendation']}\n\n"
                    markdown += f"**Sell Score:** {sell_analysis['sell_score']}/10\n\n"
                    markdown += "**Reasons:**\n"
                    for reason in sell_analysis['reasons']:
                        markdown += f"- {reason}\n"
                    markdown += "\n"
            except Exception as e:
                # Skip stocks that can't be analyzed (e.g., delisted)
                logger.warning(f"Skipping sell analysis for {holding['ticker']}: {e}")
                continue
        
        if not has_sell_recs:
            markdown += "*No immediate sell recommendations at this time.*\n\n"
        
        # Buy opportunities (optional)
        if include_buy_opportunities:
            opportunities = self._investment_service.find_buy_opportunities(
                sectors=sectors_for_opportunities,
                limit=5
            )
            
            if opportunities:
                markdown += "## 💡 Buy Opportunities\n\n"
                for opp in opportunities:
                    markdown += f"### {opp['ticker']} - {opp['company_name']}\n\n"
                    markdown += f"- **Sector:** {opp['sector']}\n"
                    markdown += f"- **Current Price:** ${opp['current_price']:.2f}\n"
                    markdown += f"- **Buy Score:** {opp['buy_score']}/10\n\n"
                    markdown += "**Reasons:**\n"
                    for reason in opp['reasons']:
                        markdown += f"- {reason}\n"
                    markdown += "\n"
        
        return markdown
    
    async def _generate_professional_report(self, format: str = "pdf", output_path: Optional[str] = None):
        """
        Generate a professional portfolio report using the Reporter agent.
        
        Args:
            format: Output format (pdf, pptx, html, markdown)
            output_path: Optional custom output path
            
        Returns:
            Result message with file path
        """
        # Get portfolio data
        result = self._investment_service.generate_portfolio_report()
        
        if result['status'] == 'empty':
            return "Cannot create report: Portfolio is empty."
        
        # Prepare data for reporter
        portfolio_data = {
            "summary": {
                "total_value": result['total_current_value'],
                "total_cost": result['total_purchase_value'],
                "profit_loss": result['total_profit_loss'],
                "profit_loss_pct": result['total_profit_loss_pct'],
            },
            "holdings": result['holdings'],
            "sell_recommendations": result['sell_recommendations'],
        }
        
        # Try to use reporter agent via hub if available
        if self._agent and hasattr(self._agent, 'hub'):
            try:
                logger.info(f"Calling reporter agent to create {format} report...")
                reporter_result = await self._agent.hub.call_agent(
                    "reporter",
                    action="create_investment_report",
                    portfolio_data=portfolio_data,
                    output_format=format,
                    output_path=output_path,
                )
                return f"✅ Professional {format.upper()} report created via Reporter agent:\n{reporter_result}"
            except Exception as e:
                logger.warning(f"Could not use reporter agent: {e}")
                return f"⚠️ Reporter agent not available. Use markdown report:\n{await self._generate_portfolio_report()}"
        else:
            return f"⚠️ Hub integration not available. Use markdown report:\n{await self._generate_portfolio_report()}"    
    async def execute_task_direct(self, task: str) -> str:
        """
        Execute task using direct tool calling, bypassing the agent framework.
        
        This is a workaround for framework limitations with async tool results.
        Directly invokes plugin methods to generate a complete investment report.
        
        Args:
            task: Task description containing portfolio information
            
        Returns:
            Complete investment report as markdown string
        """
        logger.info("Executing investment analysis using direct tool calling...")
        
        import re
        from datetime import datetime
        
        report_parts = []
        report_parts.append("# Investment Portfolio Analysis Report\n")
        report_parts.append(f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        
        try:
            # Parse task to extract portfolio information
            # Pattern: "23 Tesla (TSLA) shares @ €187.60 ($218.55)"
            stock_pattern = r'(\d+)\s+([A-Za-z\s]+)\s+\(([A-Z]+)\)\s+shares?\s+@\s+€[\d.]+\s+\(\$([\d.]+)\)'
            matches = re.findall(stock_pattern, task)
            
            if not matches:
                # Fallback: try EUR-only pattern
                stock_pattern_eur = r'(\d+)\s+([A-Za-z\s]+)\s+\(([A-Z]+)\)\s+shares?\s+@\s+€([\d.]+)'
                matches = re.findall(stock_pattern_eur, task)
                logger.warning("USD prices not found, using EUR prices")
            
            # Add stocks to portfolio
            logger.info("Adding stocks to portfolio...")
            for shares, company, ticker, price in matches:
                try:
                    result = await self._add_to_portfolio(ticker, float(shares), float(price))
                    logger.info(f"Added {ticker}: {result}")
                except Exception as e:
                    logger.warning(f"Failed to add {ticker}: {e}")
            
            # Get current portfolio
            logger.info("Fetching current portfolio...")
            portfolio_info = await self._get_portfolio()
            report_parts.append("## Current Portfolio\n\n")
            report_parts.append(portfolio_info)
            report_parts.append("\n\n")
            
            # Analyze each stock
            report_parts.append("## Individual Stock Analysis\n\n")
            for _, _, ticker, _ in matches:
                try:
                    logger.info(f"Analyzing {ticker}...")
                    analysis = await self._analyze_stock(ticker)
                    report_parts.append(analysis)
                    report_parts.append("\n\n")
                except Exception as e:
                    logger.warning(f"Failed to analyze {ticker}: {e}")
            
            # Get sell recommendations
            report_parts.append("## Sell Recommendations\n\n")
            for _, _, ticker, _ in matches:
                try:
                    logger.info(f"Checking sell recommendation for {ticker}...")
                    sell_rec = await self._should_sell(ticker)
                    report_parts.append(f"### {ticker}\n{sell_rec}\n\n")
                except Exception as e:
                    logger.warning(f"Failed to get sell recommendation for {ticker}: {e}")
            
            # Find buy opportunities
            logger.info("Finding buy opportunities...")
            try:
                buy_opps = await self._find_buy_opportunities()
                report_parts.append("## Buy Opportunities\n\n")
                report_parts.append(buy_opps)
                report_parts.append("\n\n")
            except Exception as e:
                logger.warning(f"Failed to find buy opportunities: {e}")
            
            # Generate overall portfolio report
            logger.info("Generating portfolio summary...")
            try:
                summary = await self._generate_portfolio_report()
                report_parts.append("## Portfolio Summary\n\n")
                report_parts.append(summary)
            except Exception as e:
                logger.warning(f"Failed to generate portfolio report: {e}")
            
            final_report = "".join(report_parts)
            logger.info(f"Direct execution completed, report length: {len(final_report)} characters")
            return final_report
            
        except Exception as e:
            logger.error(f"Direct execution failed: {e}", exc_info=True)
            raise RuntimeError(f"Direct investment execution failed: {e}")
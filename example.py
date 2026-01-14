"""Example usage of the Investment agent."""

import asyncio
import os
from agno import Agent
from egile_agent_investment.plugin import InvestmentPlugin


async def main():
    """Run example interactions with the Investment agent."""
    
    # Create the investment plugin
    plugin = InvestmentPlugin(
        mcp_port=8004,
        use_mcp=False,  # Use direct mode for this example
    )
    
    # Create the agent
    agent = Agent(
        name="Investment Advisor",
        description="Monitor investments, analyze stocks, and provide buy/sell recommendations",
        instructions=[
            "You are a professional investment advisor.",
            "Help users make informed investment decisions based on data.",
            "Always explain your recommendations clearly.",
        ],
        model="gpt-4",
        plugins=[plugin],
        show_tool_calls=True,
        markdown=True,
    )
    
    print("=" * 60)
    print("Investment Agent Example")
    print("=" * 60)
    print()
    
    # Example 1: Add stocks to portfolio
    print("📊 Adding stocks to portfolio...")
    response = await agent.run(
        "Add AAPL to my portfolio with 10 shares at $150, "
        "and add MSFT with 5 shares at $300"
    )
    print(response)
    print()
    
    # Example 2: View portfolio
    print("📈 Viewing portfolio...")
    response = await agent.run("Show me my current portfolio with values")
    print(response)
    print()
    
    # Example 3: Analyze a stock
    print("🔍 Analyzing Tesla stock...")
    response = await agent.run("Give me a detailed analysis of Tesla (TSLA)")
    print(response)
    print()
    
    # Example 4: Check if should sell
    print("🎯 Checking sell recommendation...")
    response = await agent.run("Should I sell my AAPL stock? Why or why not?")
    print(response)
    print()
    
    # Example 5: Find buy opportunities
    print("💡 Finding buy opportunities...")
    response = await agent.run(
        "Find me 5 tech stocks to buy with good value and growth potential"
    )
    print(response)
    print()
    
    # Example 6: Generate report
    print("📋 Generating portfolio report...")
    response = await agent.run("Generate a comprehensive portfolio report")
    print(response)
    print()
    
    print("=" * 60)
    print("Example completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

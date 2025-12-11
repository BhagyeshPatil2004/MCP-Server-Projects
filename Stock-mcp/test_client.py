import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run():
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
        env=None
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # List available tools
            tools = await session.list_tools()
            print("Connected to server. Available tools:")
            for tool in tools.tools:
                print(f"- {tool.name}: {tool.description}")

            # Test get_stock_price
            print("\n--- Testing get_stock_price('AAPL') ---")
            try:
                result = await session.call_tool("get_stock_price", arguments={"symbol": "AAPL"})
                with open("result.txt", "w") as f:
                    f.write(f"Stock Price Result: {result.content}\n")
            except Exception as e:
                with open("result.txt", "w") as f:
                    f.write(f"Stock Price Failed: {e}\n")

            # Test get_company_info
            print("\n--- Testing get_company_info('MSFT') ---")
            try:
                result = await session.call_tool("get_company_info", arguments={"symbol": "MSFT"})
                with open("result.txt", "a") as f:
                     f.write(f"Company Info Result: {str(result.content)[:200]}...\n")
            except Exception as e:
                with open("result.txt", "a") as f:
                    f.write(f"Company Info Failed: {e}\n")

if __name__ == "__main__":
    asyncio.run(run())

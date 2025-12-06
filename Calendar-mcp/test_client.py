import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run():
    print("Starting Calendar MCP Test...")
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
        env=None
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # List available tools
            tools = await session.list_tools()
            print("\nAvailable tools:")
            for tool in tools.tools:
                print(f"- {tool.name}: {tool.description}")

            # Test list_events
            print("\n--- Testing list_events ---")
            print("Note: If this is the first run, a browser window should open for you to log in.")
            try:
                # Setting a timeout because the first run blocks on browser login
                result = await asyncio.wait_for(
                    session.call_tool("list_events", arguments={"max_results": 5}),
                    timeout=60 # Give user 60 seconds to log in
                )
                print(f"Result: {result.content}")
            except asyncio.TimeoutError:
                print("Timed out waiting for login! Please check your browser window.")
            except Exception as e:
                print(f"Call failed: {e}")

if __name__ == "__main__":
    asyncio.run(run())

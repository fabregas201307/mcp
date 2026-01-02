import asyncio
from mcp.client.sse import sse_client
from mcp.client.session import ClientSession

async def main():
    print("Connecting to MCP server...")
    try:
        async with sse_client("http://localhost:8001/sse") as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                print("Connected!")
                
                # List tools
                tools = await session.list_tools()
                print("\nAvailable Tools:")
                for tool in tools.tools:
                    print(f"- {tool.name}: {tool.description}")
                
                # Call list_git_repos
                print("\nCalling list_git_repos...")
                result = await session.call_tool("list_git_repos", {})
                print("Result:", result)

                # Call search_code
                print("\nCalling search_code with keyword 'mean reversion'...")
                result = await session.call_tool("search_code", {"keyword": "mean reversion"})
                print("Result:", result)

                # --- NEW SKILLS TEST CASES ---

                # 1. Test the "Thick Tool" (Backtest)
                # This demonstrates running a complex task on the server and getting a small JSON result
                print("\n--- Testing Skill: Backtest Alpha (Thick Tool) ---")
                print("Calling backtest_alpha...")
                result = await session.call_tool("backtest_alpha", {
                    "alpha_name": "alpha_142", 
                    "start_date": "2024-01-01"
                })
                print("Backtest Result (JSON):", result.content[0].text)

                # 2. Test the "Prompt" (Standardized Instruction)
                # This demonstrates fetching a pre-defined "Skill" context to send to an LLM
                print("\n--- Testing Skill: Review Alpha Code (Prompt) ---")
                
                # First, list available prompts
                print("Available Prompts:")
                prompts = await session.list_prompts()
                for p in prompts.prompts:
                    print(f"- {p.name}: {p.description}")

                # Then, get the specific prompt context
                print("\nFetching 'review_alpha_code' prompt...")
                dummy_code = """
def alpha_strategy(df):
    # Potential look-ahead bias here
    return df['close'].shift(-1) / df['open']
"""
                prompt_result = await session.get_prompt("review_alpha_code", arguments={"code_snippet": dummy_code})
                
                print("Prompt Content (What gets sent to the LLM):")
                for message in prompt_result.messages:
                    print(f"\n[Role: {message.role}]")
                    if hasattr(message.content, 'text'):
                        print(f"Content: {message.content.text}")
                    else:
                        print(f"Content: {message.content}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
